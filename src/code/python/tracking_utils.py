import os
import psutil
import tracemalloc


def get_process_memory(convert_to_mb=False):
    """
    Get the memory usage of the current process.

    This function retrieves the Resident Set Size (RSS) memory usage of the
    current process, which represents the portion of memory occupied by the
    process that is held in RAM.
    """
    process = psutil.Process(os.getpid())
    mem_usage = process.memory_info().rss  # in bytes
    if convert_to_mb:
        mem_usage = mem_usage / (1024 * 1024)

    return mem_usage


def analyze_memory_usage(func, *args, **kwargs):
    """
    Analyzes the memory usage of a given function by tracking memory allocations
    and displaying the top 10 memory-consuming lines of code.

    Args:
        func (callable): The function to analyze.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        Any: The result of the executed function.

    Side Effects:
        Prints the top 10 memory-consuming lines of code to the console.

    Example:
        >>> def example_function():
        ...     a = [i for i in range(100000)]
        ...     return sum(a)
        ...
        >>> analyze_memory_usage(example_function)
        [ Top 10 ]
        /path/to/file.py:line_number: memory usage details
        ...
    """
    tracemalloc.start()

    # Execute the passed function
    result = func(*args, **kwargs)

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:  # Print the top 10 memory-consuming lines
        print(stat)

    return result
