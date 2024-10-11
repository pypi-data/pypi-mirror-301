"""InnerShaftSocketBase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2349

_INNER_SHAFT_SOCKET_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "InnerShaftSocketBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2331,
        _2334,
        _2351,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2388,
        _2391,
    )

    Self = TypeVar("Self", bound="InnerShaftSocketBase")
    CastSelf = TypeVar(
        "CastSelf", bound="InnerShaftSocketBase._Cast_InnerShaftSocketBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InnerShaftSocketBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InnerShaftSocketBase:
    """Special nested class for casting InnerShaftSocketBase to subclasses."""

    __parent__: "InnerShaftSocketBase"

    @property
    def shaft_socket(self: "CastSelf") -> "_2349.ShaftSocket":
        return self.__parent__._cast(_2349.ShaftSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2331.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2331

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
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2388.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2388,
        )

        return self.__parent__._cast(_2388.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2391.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2391,
        )

        return self.__parent__._cast(_2391.CycloidalDiscInnerSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "InnerShaftSocketBase":
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
class InnerShaftSocketBase(_2349.ShaftSocket):
    """InnerShaftSocketBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INNER_SHAFT_SOCKET_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_InnerShaftSocketBase":
        """Cast to another type.

        Returns:
            _Cast_InnerShaftSocketBase
        """
        return _Cast_InnerShaftSocketBase(self)
