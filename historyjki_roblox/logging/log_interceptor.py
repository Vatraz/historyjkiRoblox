class LogInterceptorBase:
    def intercept(self, log: str):
        raise NotImplementedError


class LogInterceptionError(Exception):
    pass
