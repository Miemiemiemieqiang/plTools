from datetime import datetime


def run_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        print(start_time.strftime("%Y-%m-%d %H:%M:%S"))
        result = func(*args, **kwargs)
        end_time = datetime.now()
        print(end_time.strftime("%Y-%m-%d %H:%M:%S"))
        print("Cost time %s " % (end_time - start_time))
        return result
    return wrapper
