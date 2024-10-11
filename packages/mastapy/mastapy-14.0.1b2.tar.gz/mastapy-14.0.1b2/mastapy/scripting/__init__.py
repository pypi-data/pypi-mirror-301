"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7734 import ApiEnumForAttribute
    from mastapy._private.scripting._7735 import ApiVersion
    from mastapy._private.scripting._7736 import SMTBitmap
    from mastapy._private.scripting._7738 import MastaPropertyAttribute
    from mastapy._private.scripting._7739 import PythonCommand
    from mastapy._private.scripting._7740 import ScriptingCommand
    from mastapy._private.scripting._7741 import ScriptingExecutionCommand
    from mastapy._private.scripting._7742 import ScriptingObjectCommand
    from mastapy._private.scripting._7743 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7734": ["ApiEnumForAttribute"],
        "_private.scripting._7735": ["ApiVersion"],
        "_private.scripting._7736": ["SMTBitmap"],
        "_private.scripting._7738": ["MastaPropertyAttribute"],
        "_private.scripting._7739": ["PythonCommand"],
        "_private.scripting._7740": ["ScriptingCommand"],
        "_private.scripting._7741": ["ScriptingExecutionCommand"],
        "_private.scripting._7742": ["ScriptingObjectCommand"],
        "_private.scripting._7743": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
