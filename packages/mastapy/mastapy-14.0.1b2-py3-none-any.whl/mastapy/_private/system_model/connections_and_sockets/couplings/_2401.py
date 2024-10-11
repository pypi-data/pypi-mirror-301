"""CouplingConnection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2336

_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets import _2327
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2397,
        _2399,
        _2403,
        _2405,
        _2407,
    )

    Self = TypeVar("Self", bound="CouplingConnection")
    CastSelf = TypeVar("CastSelf", bound="CouplingConnection._Cast_CouplingConnection")


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnection:
    """Special nested class for casting CouplingConnection to subclasses."""

    __parent__: "CouplingConnection"

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2336.InterMountableComponentConnection":
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
    def clutch_connection(self: "CastSelf") -> "_2397.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2397,
        )

        return self.__parent__._cast(_2397.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2399.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2399,
        )

        return self.__parent__._cast(_2399.ConceptCouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2403.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2403,
        )

        return self.__parent__._cast(_2403.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2405.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2405,
        )

        return self.__parent__._cast(_2405.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2407.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2407,
        )

        return self.__parent__._cast(_2407.TorqueConverterConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "CouplingConnection":
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
class CouplingConnection(_2336.InterMountableComponentConnection):
    """CouplingConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnection
        """
        return _Cast_CouplingConnection(self)
