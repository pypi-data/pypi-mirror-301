import tempfile
from typing import Optional, Tuple, Any
from contextlib import contextmanager
import multiprocessing
import math
import os
import shutil
import psutil

import pyarrow.parquet as pq
from pyspark.sql import SparkSession


_DEFAULT_HEAP_SIZE_EXTRA_ROOM = 2 * 512 * 1024 * 1024


def _get_cgroup_memory() -> int:
    max_memory_str = None
    if os.path.isfile("/sys/fs/cgroup/memory.max"):
        with open("/sys/fs/cgroup/memory.max", "r") as f:
            max_memory_str = f.read().strip()
    elif os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes", "r") as f:
            max_memory_str = f.read().strip()

    max_memory = None
    if max_memory_str == "max":
        # Fallback to available virtual memory size
        max_memory = psutil.virtual_memory().available
    elif max_memory_str is not None:
        try:
            max_memory = int(max_memory_str)
        except ValueError:
            pass

    if max_memory is not None:
        return max_memory
    else:
        print("Unable to determine available memory from cgroup, assuming 4G")
        return 4 * 1024 * 1024 * 1024


def _get_uncompressed_parquet_size(path: str):
    def is_parquet(filename: str):
        return filename.endswith(".parquet")
    def get_uncompressed_size(file_path: str):
        parquet_file = pq.ParquetFile(file_path)
        metadata = parquet_file.metadata
        uncompressed_size = 0
        for i in range(metadata.num_row_groups):
            row_group = metadata.row_group(i)
            for j in range(row_group.num_columns):
                column = row_group.column(j)
                uncompressed_size += column.total_uncompressed_size
        return uncompressed_size
    if os.path.isfile(path) and is_parquet(path):
        uncompressed_size = get_uncompressed_size(path)
        return uncompressed_size
    # Path might be a subdir as obtained by `partitionBy`
    elif os.path.isdir(path):
        total_uncompressed_size = 0
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            total_uncompressed_size += _get_uncompressed_parquet_size(file_path)
        return total_uncompressed_size
    else:
        return 0


def _get_num_partitions(
        paths: list[str],
        available_memory: int,
        cpu_count: int,
) -> int:
    """Determine the number of partitions s.t. each partition is as big as possible
    while still making sure all cores are occupied."""
    def get_file_or_dir_size(path):
        if path.endswith(".parquet"):
            return _get_uncompressed_parquet_size(path)
        else:
            if os.path.isfile(path):
                size = os.path.getsize(path)
            elif os.path.isdir(path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                size = total_size
            else:
                raise ValueError(f"The path {path} is neither a file nor a directory.")
        return size

    file_size = max([get_file_or_dir_size(path) for path in paths])
    if file_size == 0:
        return 200  # default number of partitions in spark

    # Don't make the partitions smaller than 36MiB
    megabyte_in_bytes = 1024 * 1024
    min_partition_size = 32 * megabyte_in_bytes

    # Try to make partitions as big as possible s.t. each CPU is saturated,
    # while accounting for 50% overhead in spark.
    task_per_cpu = 3  # try to get at least this many tasks/partitions per CPU
    max_target_partition_size = max(
        int(0.5 * available_memory / (task_per_cpu * cpu_count)) // megabyte_in_bytes * megabyte_in_bytes,
        min_partition_size
    )

    target_partition_size = max_target_partition_size
    while (
        # If the file is small enough that it cannot be split across all cores,
        # divide the partition size further.
        int(file_size / target_partition_size) < (task_per_cpu * cpu_count)
    ):
        # Don't go smaller than the minimum parition size
        if target_partition_size / 2 < min_partition_size:
            break
        target_partition_size = target_partition_size / 2

    print(f"File size: {file_size}")
    print(f"Max target partition size: {max_target_partition_size}")
    print(f"Target partition size: {target_partition_size}")

    num_partitions = int(math.ceil(file_size / target_partition_size))

    return num_partitions


def _determine_optimal_spark_settings(
        files: list[str],
        heap_size_extra_room = _DEFAULT_HEAP_SIZE_EXTRA_ROOM
) -> list[Tuple[str, str]]:
    def get_spark_memory() -> int:
        """Determine the amount of memory available to spark"""
        cgroup_memory = _get_cgroup_memory()
        spark_memory = cgroup_memory - heap_size_extra_room
        return spark_memory

    cpu_count = multiprocessing.cpu_count()
    spark_memory = get_spark_memory()
    spark_memory_4096 = (spark_memory // 4096) * 4096
    num_partitions = _get_num_partitions(files, spark_memory, cpu_count)

    settings = [
        ("spark.sql.shuffle.partitions", str(num_partitions)),
        ("spark.default.parallelism", str(num_partitions)),
        ("spark.driver.cores", str(cpu_count)),
        ("spark.driver.memory", str(spark_memory_4096)),
    ]

    return settings


def _create_spark_session(
        name: str = "local_spark_session",
        parallelism: int = 8,
        heap_size: Optional[int] = None,
        heap_size_extra_room: int = _DEFAULT_HEAP_SIZE_EXTRA_ROOM,
        config: list[Tuple[str, Any]] = [],
        java_tmp_dir = "/output",
) -> SparkSession:
    """
    :param name: The name of the spark session.
    :param parallelism: The size of the executor pool computing internal spark tasks.
    :param heap_size: If set then this determines the JVM heap size. Note that not all the heap size is used by spark.
    :param heap_size_extra_room: If heap_size is unset then it is determined by the available memory in the current
        cgroup. Then heap_size_extra_room is subtracted to arrive at the final heap size. This number should account for
        the python runtime itself as well as other structures that may be needed during spark compute.
    :param config: Additional config settings to set on the spark config.
    :param java_tmp_dir: Location for the JVM to store temp files.
    :return: The spark session.
    """
    os.environ["SPARK_EXECUTOR_POOL_SIZE"] = str(parallelism)
    os.environ["JDK_JAVA_OPTIONS"] = f'-Duser.home=/output -Djava.io.tmpdir="{java_tmp_dir}"'
    spark_memory = None
    if heap_size is None:
        cgroup_memory = _get_cgroup_memory()
        spark_memory = cgroup_memory - heap_size_extra_room
    else:
        spark_memory = heap_size

    spark_memory_4096 = (spark_memory // 4096) * 4096
    if "spark.driver.memory" not in dict(config):
        config.append(("spark.driver.memory", str(spark_memory_4096)))

    ss = (
        SparkSession.builder
        .appName(name)
        .master("local[*]")
    )
    for (key, value) in config:
        ss = ss.config(key, value)

    print("Spark settings:\n" + f"\n".join([str(x) for x in config]))

    return ss.getOrCreate()


@contextmanager
def spark_session(temp_dir: str = "/scratch", input_files: list[str] = None, **kwargs):
    """
    Create a spark session and configure it according to the enclave environment.

    **Parameters**:
    - `temp_dir`: Where to store temporary data such as persisted data frames
      or shuffle data.
    - `input_files`: A list of input files on the basis of which the partition
      size is determined.

    **Example**:

    ```python
    import decentriq_util as dq

    # Path to a potentially very large file
    input_csv_path = "/input/my_file.csv"

    # Automatically create and configure a spark session and
    # make sure it's being stopped at the end.
    with dq.spark.spark_session(input_files=[input_csv_path]) as ss:
        # Read from a CSV file
        df = ss.read.csv(input_csv_path, header=False).cache()

        # Perform any pyspark transformations
        print(f"Original number of rows: {df.count()}")
        result_df = df.limit(100)

        # Write the result to an output file
        result_df.write.parquet("/output/my_file.parquet")
    ```
    """
    with tempfile.TemporaryDirectory(dir=temp_dir, prefix="java-") as java_tmp:
        with tempfile.TemporaryDirectory(dir=temp_dir, prefix="spark-") as spark_tmp:
            config = kwargs.get("config", [])
            config_dict = dict(config)
            if input_files is not None and input_files:
                optimal_settings = _determine_optimal_spark_settings(
                    input_files,
                    heap_size_extra_room=kwargs.get(
                        "heap_size_extra_room", _DEFAULT_HEAP_SIZE_EXTRA_ROOM
                    )
                )
                for key, value in optimal_settings:
                    if key not in config_dict:
                        config.append((key, value))
            if "spark.local.dir" not in config_dict:
                config.append(
                    ("spark.local.dir", spark_tmp)
                )
            kwargs["config"] = config
            if "java_tmp_dir" not in kwargs:
                kwargs["java_tmp_dir"] = java_tmp
            ss = _create_spark_session(**kwargs)
            try:
                yield ss
            finally:
                try:
                    ss.stop()
                except:
                    pass
