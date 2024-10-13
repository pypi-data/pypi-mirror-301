def run_background_task(func):
    """
    Decorator to run a function as a background task.
    This is a placeholder implementation.
    """
    def wrapper(*args, **kwargs):
        # Placeholder for actual background task logic
        print(f"Running {func.__name__} as a background task")
        return func(*args, **kwargs)
    return wrapper