import traceback
import datetime

def log_entry(record: str):
    """
    Logs an entry in the user log file to be displayed at the end of the execution.
    """
    current_time = datetime.datetime.now(datetime.timezone.utc)
    with open("/internal/logs", "a+") as f:
        f.write(f"LOG {current_time}: {record}\n")
        
def log_stack_trace(e: Exception):
    """
    Allows to add a striped stack strace for an Exception e in the user log file.
    The striped stack trace will not contain any environment variable or secrets
    in it.
    """
    tb = traceback.TracebackException.from_exception(e, capture_locals=False)
    safe_traceback = "".join([s for s in tb.format()][:-1])
    error_qualified_class_name = e.__class__.__module__ + "." + e.__class__.__name__
    log_entry(f"Encountered error: {error_qualified_class_name}, Traceback:\n{safe_traceback}")