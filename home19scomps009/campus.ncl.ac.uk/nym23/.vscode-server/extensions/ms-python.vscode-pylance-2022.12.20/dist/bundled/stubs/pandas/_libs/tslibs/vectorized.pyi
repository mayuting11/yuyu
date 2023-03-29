from typing import Sequence

import numpy as np

from .dtypes import Resolution

def normalize_i8_timestamps(
    stamps: Sequence[int], tz: str | None = ...
) -> list[int]: ...
def is_date_array_normalized(stamps: Sequence[int], tz: str | None = ...) -> bool: ...
def dt64arr_to_periodarr(
    stamps: Sequence[int], freq: int, tz: str | None = ...
) -> list[int]: ...
def ints_to_pydatetime(
    arr: Sequence[int], tz: str = ..., freq: str = ..., fold: bool = ..., box: str = ...
) -> np.ndarray: ...
def get_resolution(stamps: Sequence[int], tz: str | None = ...) -> Resolution: ...
