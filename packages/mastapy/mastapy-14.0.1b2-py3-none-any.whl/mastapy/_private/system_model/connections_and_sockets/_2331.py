"""CylindricalSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2351

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2321,
        _2322,
        _2329,
        _2334,
        _2335,
        _2337,
        _2338,
        _2339,
        _2340,
        _2341,
        _2343,
        _2344,
        _2345,
        _2348,
        _2349,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2398,
        _2400,
        _2402,
        _2404,
        _2406,
        _2408,
        _2409,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2388,
        _2389,
        _2391,
        _2392,
        _2394,
        _2395,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2365

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2351.Socket":
        return self.__parent__._cast(_2351.Socket)

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2321.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2321

        return self.__parent__._cast(_2321.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2322.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2322

        return self.__parent__._cast(_2322.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2329.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2329

        return self.__parent__._cast(_2329.CVTPulleySocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2334.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2334

        return self.__parent__._cast(_2334.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2335.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2337.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2338.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2339.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2339

        return self.__parent__._cast(_2339.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2340.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2340

        return self.__parent__._cast(_2340.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2341.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2343.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2344.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2344

        return self.__parent__._cast(_2344.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2345.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2345

        return self.__parent__._cast(_2345.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2348.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2348

        return self.__parent__._cast(_2348.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2349.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.ShaftSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2365.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2365

        return self.__parent__._cast(_2365.CylindricalGearTeethSocket)

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
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2392.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2392,
        )

        return self.__parent__._cast(_2392.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2394.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2394,
        )

        return self.__parent__._cast(_2394.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2395.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2395,
        )

        return self.__parent__._cast(_2395.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2398.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2398,
        )

        return self.__parent__._cast(_2398.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2400.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2400,
        )

        return self.__parent__._cast(_2400.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2402.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2402,
        )

        return self.__parent__._cast(_2402.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2404.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2404,
        )

        return self.__parent__._cast(_2404.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2406.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2406,
        )

        return self.__parent__._cast(_2406.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2408.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2408,
        )

        return self.__parent__._cast(_2408.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2409.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2409,
        )

        return self.__parent__._cast(_2409.TorqueConverterTurbineSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
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
class CylindricalSocket(_2351.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
