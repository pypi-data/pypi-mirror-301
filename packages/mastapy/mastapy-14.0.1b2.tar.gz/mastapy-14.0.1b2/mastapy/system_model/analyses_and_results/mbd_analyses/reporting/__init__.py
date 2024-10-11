"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5654 import (
        AbstractMeasuredDynamicResponseAtTime,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5655 import (
        DynamicForceResultAtTime,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5656 import (
        DynamicForceVector3DResult,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5657 import (
        DynamicTorqueResultAtTime,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5658 import (
        DynamicTorqueVector3DResult,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.reporting._5659 import (
        NodeInformation,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5654": [
            "AbstractMeasuredDynamicResponseAtTime"
        ],
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5655": [
            "DynamicForceResultAtTime"
        ],
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5656": [
            "DynamicForceVector3DResult"
        ],
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5657": [
            "DynamicTorqueResultAtTime"
        ],
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5658": [
            "DynamicTorqueVector3DResult"
        ],
        "_private.system_model.analyses_and_results.mbd_analyses.reporting._5659": [
            "NodeInformation"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractMeasuredDynamicResponseAtTime",
    "DynamicForceResultAtTime",
    "DynamicForceVector3DResult",
    "DynamicTorqueResultAtTime",
    "DynamicTorqueVector3DResult",
    "NodeInformation",
)
