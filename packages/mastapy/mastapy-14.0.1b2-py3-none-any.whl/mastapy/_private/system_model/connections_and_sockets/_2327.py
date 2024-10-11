"""Connection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2258

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2320,
        _2323,
        _2324,
        _2328,
        _2336,
        _2342,
        _2347,
        _2350,
        _2351,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2397,
        _2399,
        _2401,
        _2403,
        _2405,
        _2407,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2390,
        _2393,
        _2396,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2354,
        _2356,
        _2358,
        _2360,
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2373,
        _2374,
        _2375,
        _2378,
        _2380,
        _2382,
        _2384,
        _2386,
    )
    from mastapy._private.system_model.part_model import _2500

    Self = TypeVar("Self", bound="Connection")
    CastSelf = TypeVar("CastSelf", bound="Connection._Cast_Connection")


__docformat__ = "restructuredtext en"
__all__ = ("Connection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Connection:
    """Special nested class for casting Connection to subclasses."""

    __parent__: "Connection"

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2320.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2320

        return self.__parent__._cast(_2320.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2323.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2323

        return self.__parent__._cast(_2323.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2324.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2324

        return self.__parent__._cast(_2324.CoaxialConnection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2328.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2328

        return self.__parent__._cast(_2328.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2336.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2342.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2347.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2347

        return self.__parent__._cast(_2347.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2350.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2354.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2354

        return self.__parent__._cast(_2354.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2356.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2358.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2358

        return self.__parent__._cast(_2358.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2360.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2360

        return self.__parent__._cast(_2360.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2362.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2364.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2366.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2368.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2370.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2373.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2373

        return self.__parent__._cast(_2373.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2374.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2375.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2375

        return self.__parent__._cast(_2375.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2378.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2380.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2382.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2384.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2386.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2386

        return self.__parent__._cast(_2386.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2393.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2393,
        )

        return self.__parent__._cast(_2393.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2396.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2396,
        )

        return self.__parent__._cast(_2396.RingPinsToDiscConnection)

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
    def coupling_connection(self: "CastSelf") -> "_2401.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2401,
        )

        return self.__parent__._cast(_2401.CouplingConnection)

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
    def connection(self: "CastSelf") -> "Connection":
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
class Connection(_2258.DesignEntity):
    """Connection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionID")

        if temp is None:
            return ""

        return temp

    @property
    def drawing_position(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "DrawingPosition")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @drawing_position.setter
    @enforce_parameter_types
    def drawing_position(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "DrawingPosition", value)

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def speed_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_from_a_to_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioFromAToB")

        if temp is None:
            return 0.0

        return temp

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def owner_a(self: "Self") -> "_2500.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def owner_b(self: "Self") -> "_2500.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OwnerB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_a(self: "Self") -> "_2351.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def socket_b(self: "Self") -> "_2351.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SocketB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def other_owner(self: "Self", component: "_2500.Component") -> "_2500.Component":
        """mastapy.system_model.part_model.Component

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "OtherOwner", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket_for_component(
        self: "Self", component: "_2500.Component"
    ) -> "_2351.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "OtherSocket",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def other_socket(self: "Self", socket: "_2351.Socket") -> "_2351.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "OtherSocket", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def socket_for(self: "Self", component: "_2500.Component") -> "_2351.Socket":
        """mastapy.system_model.connections_and_sockets.Socket

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "SocketFor", component.wrapped if component else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Connection":
        """Cast to another type.

        Returns:
            _Cast_Connection
        """
        return _Cast_Connection(self)
