"""ConicalGearTeethSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2369

_CONICAL_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearTeethSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2351
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2355,
        _2357,
        _2359,
        _2371,
        _2372,
        _2376,
        _2377,
        _2379,
        _2381,
        _2383,
        _2387,
    )

    Self = TypeVar("Self", bound="ConicalGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearTeethSocket._Cast_ConicalGearTeethSocket"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearTeethSocket:
    """Special nested class for casting ConicalGearTeethSocket to subclasses."""

    __parent__: "ConicalGearTeethSocket"

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2369.GearTeethSocket":
        return self.__parent__._cast(_2369.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2351.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2351

        return self.__parent__._cast(_2351.Socket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2355.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2355

        return self.__parent__._cast(_2355.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2357.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2357

        return self.__parent__._cast(_2357.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2359.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2359

        return self.__parent__._cast(_2359.BevelGearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2371.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2371

        return self.__parent__._cast(_2371.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2372.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2376.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2376

        return self.__parent__._cast(_2376.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2377.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2377

        return self.__parent__._cast(_2377.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2379.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2379

        return self.__parent__._cast(_2379.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2381.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2381

        return self.__parent__._cast(_2381.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2383.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2383

        return self.__parent__._cast(_2383.StraightBevelGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2387.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2387

        return self.__parent__._cast(_2387.ZerolBevelGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "ConicalGearTeethSocket":
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
class ConicalGearTeethSocket(_2369.GearTeethSocket):
    """ConicalGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearTeethSocket
        """
        return _Cast_ConicalGearTeethSocket(self)
