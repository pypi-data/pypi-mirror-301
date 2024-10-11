"""ShaftSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2331

_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2334,
        _2335,
        _2340,
        _2341,
        _2351,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2388,
        _2389,
        _2391,
    )

    Self = TypeVar("Self", bound="ShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="ShaftSocket._Cast_ShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSocket:
    """Special nested class for casting ShaftSocket to subclasses."""

    __parent__: "ShaftSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2331.CylindricalSocket":
        return self.__parent__._cast(_2331.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2351.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2351

        return self.__parent__._cast(_2351.Socket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2334.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2334

        return self.__parent__._cast(_2334.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2335.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.InnerShaftSocketBase)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2340.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2340

        return self.__parent__._cast(_2340.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2341.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.OuterShaftSocketBase)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2388.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2388,
        )

        return self.__parent__._cast(_2388.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2389.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2389,
        )

        return self.__parent__._cast(_2389.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2391.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2391,
        )

        return self.__parent__._cast(_2391.CycloidalDiscInnerSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "ShaftSocket":
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
class ShaftSocket(_2331.CylindricalSocket):
    """ShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_ShaftSocket
        """
        return _Cast_ShaftSocket(self)
