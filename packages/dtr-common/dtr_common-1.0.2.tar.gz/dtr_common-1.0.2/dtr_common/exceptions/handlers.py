
def error_handler(error: type[Exception]):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            try:
                res = fn(*args, **kwargs)
                return res
            except Exception as e:
                raise error(e)

        return wrapper

    return decorator