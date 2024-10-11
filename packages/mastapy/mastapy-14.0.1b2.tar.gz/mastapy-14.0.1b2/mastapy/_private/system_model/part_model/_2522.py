"""MountableComponent"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2500

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets import (
        _2324,
        _2327,
        _2331,
    )
    from mastapy._private.system_model.part_model import (
        _2491,
        _2495,
        _2501,
        _2503,
        _2518,
        _2519,
        _2524,
        _2526,
        _2527,
        _2529,
        _2530,
        _2536,
        _2538,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2639,
        _2642,
        _2645,
        _2648,
        _2650,
        _2652,
        _2658,
        _2660,
        _2666,
        _2669,
        _2670,
        _2671,
        _2673,
        _2675,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2629
    from mastapy._private.system_model.part_model.gears import (
        _2572,
        _2574,
        _2576,
        _2577,
        _2578,
        _2580,
        _2582,
        _2584,
        _2586,
        _2587,
        _2589,
        _2593,
        _2595,
        _2597,
        _2599,
        _2602,
        _2604,
        _2606,
        _2608,
        _2609,
        _2610,
        _2612,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2500.Component":
        return self.__parent__._cast(_2500.Component)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2495.Bearing":
        from mastapy._private.system_model.part_model import _2495

        return self.__parent__._cast(_2495.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2503.Connector":
        from mastapy._private.system_model.part_model import _2503

        return self.__parent__._cast(_2503.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2518.MassDisc":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2519.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2519

        return self.__parent__._cast(_2519.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2524.OilSeal":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2527.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2527

        return self.__parent__._cast(_2527.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2529.PointLoad":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2530.PowerLoad":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2536.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2538.VirtualComponent":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2572.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2572

        return self.__parent__._cast(_2572.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2574.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2576.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2577.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2578.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2580.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2582.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2584.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2586.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2587.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2589.Gear":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2593.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2595.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2599.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2602.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2604.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2606.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2608.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2609.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2610.WormGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2612.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2629.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2629

        return self.__parent__._cast(_2629.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2639.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2639

        return self.__parent__._cast(_2639.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2642.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2642

        return self.__parent__._cast(_2642.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2645.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2645

        return self.__parent__._cast(_2645.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2648.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2648

        return self.__parent__._cast(_2648.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2650.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2650

        return self.__parent__._cast(_2650.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2652.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2658.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2660.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2666.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2666

        return self.__parent__._cast(_2666.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2669.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2670.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2670

        return self.__parent__._cast(_2670.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2671.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2673.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2673

        return self.__parent__._cast(_2673.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2675.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2675

        return self.__parent__._cast(_2675.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2500.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2491.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2327.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2331.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2491.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2324.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2491.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2501.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
