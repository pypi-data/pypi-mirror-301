from ctypes import CFUNCTYPE
from logging import getLogger
from typing import Any, Optional

import pymhf.core._internal as _internal
from pymhf.core._types import FUNCDEF
from pymhf.core.memutils import find_pattern_in_binary
from pymhf.core.module_data import module_data

calling_logger = getLogger("CallingManager")


def call_function(
    name: str,
    *args,
    overload: Optional[str] = None,
    pattern: Optional[str] = None,
    func_def: Optional[FUNCDEF] = None,
) -> Any:
    """Call a named function.

    Parameters
    ----------
    name
        The name of the function to be called.
        For now the function signature will be looked up from the known signatures by name.
    *args
        The args to pass to the function call.
    overload
        The overload name to be called if required.
    pattern
        The pattern which can be used to find where the function is.
        If provided this will be used instead of the offset as determined by the name.
    """
    if func_def is not None:
        _sig = func_def
    else:
        _sig = module_data.FUNC_CALL_SIGS[name]
    if pattern:
        offset = find_pattern_in_binary(pattern, False)
    else:
        if (_pattern := module_data.FUNC_PATTERNS.get(name)) is not None:
            if isinstance(_pattern, str):
                offset = find_pattern_in_binary(_pattern, False)
            else:
                if (opattern := _pattern.get(overload)) is not None:
                    offset = find_pattern_in_binary(opattern, False)
                else:
                    first = list(_pattern.items())[0]
                    calling_logger.warning(f"No pattern overload was provided for {name}. ")
                    calling_logger.warning(f"Falling back to the first overload ({first[0]})")
                    offset = find_pattern_in_binary(first[1], False)
        else:
            offset = module_data.FUNC_OFFSETS.get(name)
        if offset is None:
            raise NameError(f"Cannot find function {name}")
    if isinstance(_sig, FUNCDEF):
        sig = CFUNCTYPE(_sig.restype, *_sig.argtypes)
    else:
        # Look up the overload:
        if (osig := _sig.get(overload)) is not None:  # type: ignore
            sig = CFUNCTYPE(osig.restype, *osig.argtypes)
        else:
            # Need to fallback on something. Raise a warning that no
            # overload was defined and that it will fallback to the
            # first entry in the dict.
            first = list(_sig.items())[0]
            calling_logger.warning(f"No function arguments overload was provided for {name}. ")
            calling_logger.warning(f"Falling back to the first overload ({first[0]})")
            sig = CFUNCTYPE(first[1].restype, *first[1].argtypes)
    if isinstance(offset, dict):
        # Handle overloads
        if (_offset := offset.get(overload)) is not None:  # type: ignore
            offset = _offset
        else:
            _offset = list(offset.items())[0]
            calling_logger.warning(f"No function arguments overload was provided for {name}. ")
            calling_logger.warning(f"Falling back to the first overload ({_offset[0]})")
            offset = _offset[1]

    cfunc = sig(_internal.BASE_ADDRESS + offset)
    return cfunc(*args)
