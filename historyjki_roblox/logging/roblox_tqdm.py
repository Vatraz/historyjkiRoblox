from proglog import TqdmProgressBarLogger
from tqdm import tqdm

from historyjki_roblox.logging.log_interceptor import LogInterceptorBase


class _RobloxTqdm(tqdm):
    log_interceptor: LogInterceptorBase | None = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, n: float | None = ...) -> bool | None:
        update = super().update(n)
        self.intercept_log(self.__str__())
        return update

    @classmethod
    def write(cls, s: str, *args, **kwargs) -> None:
        cls.intercept_log(s)
        super().write(s, *args, **kwargs)

    @classmethod
    def intercept_log(cls, msg: str):
        if cls.log_interceptor:
            cls.log_interceptor.intercept(msg)


def roblox_tqdm(log_interceptor: LogInterceptorBase | None = None):
    class RobloxTqdm(_RobloxTqdm):
        pass

    RobloxTqdm.log_interceptor = log_interceptor

    return RobloxTqdm


class RobloxTqdmProgressBarLogger(TqdmProgressBarLogger):
    def __init__(self, *args, tqdm: _RobloxTqdm, **kwargs):
        super().__init__(*args, **kwargs)
        self.tqdm = tqdm
