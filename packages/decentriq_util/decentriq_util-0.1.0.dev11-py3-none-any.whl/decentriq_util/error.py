from typing import Callable, List

import traceback
import sys
import os


def _strip_away_nix_store(path: str) -> str:
    """
    Replace '/nix/store/hash-derivation-name' with '/system/' for better
    readability of the stack trace.
    """
    if path.startswith("/nix/store"):
        return "/system/" + "/".join(path.split("/")[4:])
    else:
        return path


class SafeError(Exception):
    """
    Base class for errors that can be turned into safe error messages
    that can be displayed to the user without risking the leakage of
    sensitive information.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def safe_str(self) -> str:
        """
        Return a safe string representation of this exception
        that does not include any sensitive data.

        This method must be implemented explicitly.
        """
        raise Exception("Not implemented")


class CatchSafeErrorContext:
    """
    Context manager to handle error messages and writing them to a pre-defined
    location on the file system.
    The constructed stack track is optionally cleaned from any sensitive
    information that might be contained in the error message.
    """
    def __init__(
            self,
            should_clean_traceback: bool,
            output_file: str,
            should_exit: bool,
            transform_library_path: List[Callable[[str], str]],
    ):
        self.should_clean_traceback = should_clean_traceback
        self.output_file = output_file
        self.should_exit = should_exit
        self.transform_library_path = transform_library_path + [_strip_away_nix_store]


    def __enter__(self):
        return self


    def __exit__(self, exception_type, exception, tb_):
        if exception:
            if exception_type == SystemExit and exception.code == 0:
                # Don't produce a traceback when sys.exit(0) is used.
                return

            should_capture_local_variables = not self.should_clean_traceback
            error_class_module = exception.__class__.__module__
            ignored_modules = set(["builtins", "__main__"])
            if error_class_module and error_class_module not in ignored_modules:
                error_qualified_class_name =\
                    error_class_module + "." + exception.__class__.__name__

            else:
                error_qualified_class_name = exception.__class__.__name__

            # Skip the first frame as it is the one in the wrapper script
            tbe = traceback.TracebackException.from_exception(
                exception, capture_locals=should_capture_local_variables
            )
            lines = ["Traceback (most recent call last):"]
            for frame in tbe.stack[1:]:
                filename = frame.filename
                # Apply all configured transformer functions to the file paths
                # to make them more readable.
                for transform_fn in self.transform_library_path:
                    filename = transform_fn(filename)
                lines.append(
                    f"  File \"{filename}\","
                    f" line {frame.lineno}, in {frame.name}\n    {frame.line}"
                )

            if self.should_clean_traceback:
                # Even if we are supposed to provide a safe error, if it's one of our
                # own errors, we can still construct an (informative) safe error
                # message.
                if isinstance(exception, SafeError):
                    stringified_error =\
                            error_qualified_class_name + ": " + exception.safe_str()
                else:
                    stringified_error = error_qualified_class_name +\
                        ": (error message removed due to data privacy)"
            else:
                stringified_error = error_qualified_class_name + ": " + str(exception)

            lines.append(stringified_error)
            safe_traceback = "\n".join(lines)

            with open(self.output_file, "w") as f:
                f.write(safe_traceback)

            if self.should_exit:
                sys.exit(1)
            else:
                # Do not propagate error
                return True


def catch_safe_error(
        transform_library_path: List[Callable[[str], str]] = []
) -> CatchSafeErrorContext:
    """Construct a CatchSafeErrorContext with default values"""
    should_clean_traceback = \
        "INCLUDE_CONTAINER_LOGS_ON_ERROR" not in os.environ or os.environ["INCLUDE_CONTAINER_LOGS_ON_ERROR"] != "true"
    return CatchSafeErrorContext(
        should_clean_traceback=should_clean_traceback,
        should_exit=True,
        output_file="/internal/safe_error",
        transform_library_path=transform_library_path
    )
