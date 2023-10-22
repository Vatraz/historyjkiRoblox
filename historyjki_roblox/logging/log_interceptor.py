class LogInterceptorBase:
    def intercept(self, log: str, log_time: float):
        raise NotImplementedError


class LogInterceptionError(Exception):
    pass
