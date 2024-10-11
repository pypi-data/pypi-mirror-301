"""PartToPartShearCouplingConnection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.couplings import _2401

_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets import _2327, _2336

    Self = TypeVar("Self", bound="PartToPartShearCouplingConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingConnection._Cast_PartToPartShearCouplingConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingConnection:
    """Special nested class for casting PartToPartShearCouplingConnection to subclasses."""

    __parent__: "PartToPartShearCouplingConnection"

    @property
    def coupling_connection(self: "CastSelf") -> "_2401.CouplingConnection":
        return self.__parent__._cast(_2401.CouplingConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2336.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2327.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2327

        return self.__parent__._cast(_2327.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingConnection":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class PartToPartShearCouplingConnection(_2401.CouplingConnection):
    """PartToPartShearCouplingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_TO_PART_SHEAR_COUPLING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PartToPartShearCouplingConnection":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingConnection
        """
        return _Cast_PartToPartShearCouplingConnection(self)
