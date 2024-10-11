"""CoaxialConnection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2350

_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets import _2320, _2327
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2390

    Self = TypeVar("Self", bound="CoaxialConnection")
    CastSelf = TypeVar("CastSelf", bound="CoaxialConnection._Cast_CoaxialConnection")


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnection:
    """Special nested class for casting CoaxialConnection to subclasses."""

    __parent__: "CoaxialConnection"

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2350.ShaftToMountableComponentConnection":
        return self.__parent__._cast(_2350.ShaftToMountableComponentConnection)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2320.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2320

        return self.__parent__._cast(_2320.AbstractShaftToMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2327.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2327

        return self.__parent__._cast(_2327.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscCentralBearingConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "CoaxialConnection":
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
class CoaxialConnection(_2350.ShaftToMountableComponentConnection):
    """CoaxialConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CoaxialConnection":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnection
        """
        return _Cast_CoaxialConnection(self)
