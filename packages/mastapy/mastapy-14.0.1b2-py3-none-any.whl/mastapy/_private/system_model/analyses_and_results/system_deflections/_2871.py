"""MountableComponentSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2802

_MOUNTABLE_COMPONENT_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "MountableComponentSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4221
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2778,
        _2785,
        _2790,
        _2791,
        _2792,
        _2795,
        _2799,
        _2805,
        _2809,
        _2813,
        _2815,
        _2817,
        _2820,
        _2832,
        _2833,
        _2834,
        _2837,
        _2843,
        _2844,
        _2848,
        _2852,
        _2857,
        _2860,
        _2863,
        _2866,
        _2867,
        _2873,
        _2874,
        _2876,
        _2879,
        _2880,
        _2881,
        _2882,
        _2883,
        _2888,
        _2890,
        _2898,
        _2900,
        _2904,
        _2907,
        _2908,
        _2909,
        _2910,
        _2911,
        _2912,
        _2918,
        _2920,
        _2923,
        _2924,
        _2927,
        _2930,
    )
    from mastapy._private.system_model.fe import _2441
    from mastapy._private.system_model.part_model import _2522

    Self = TypeVar("Self", bound="MountableComponentSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentSystemDeflection._Cast_MountableComponentSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentSystemDeflection:
    """Special nested class for casting MountableComponentSystemDeflection to subclasses."""

    __parent__: "MountableComponentSystemDeflection"

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2802.ComponentSystemDeflection":
        return self.__parent__._cast(_2802.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2740.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2778.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2778,
        )

        return self.__parent__._cast(_2778.AGMAGleasonConicalGearSystemDeflection)

    @property
    def bearing_system_deflection(self: "CastSelf") -> "_2785.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2785,
        )

        return self.__parent__._cast(_2785.BearingSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2790.BevelDifferentialGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2790,
        )

        return self.__parent__._cast(_2790.BevelDifferentialGearSystemDeflection)

    @property
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2791.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2791,
        )

        return self.__parent__._cast(_2791.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2792.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2792,
        )

        return self.__parent__._cast(_2792.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2795.BevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2795,
        )

        return self.__parent__._cast(_2795.BevelGearSystemDeflection)

    @property
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2799.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2799,
        )

        return self.__parent__._cast(_2799.ClutchHalfSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2805.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2805,
        )

        return self.__parent__._cast(_2805.ConceptCouplingHalfSystemDeflection)

    @property
    def concept_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2809.ConceptGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2809,
        )

        return self.__parent__._cast(_2809.ConceptGearSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2813.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2813,
        )

        return self.__parent__._cast(_2813.ConicalGearSystemDeflection)

    @property
    def connector_system_deflection(
        self: "CastSelf",
    ) -> "_2815.ConnectorSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2815,
        )

        return self.__parent__._cast(_2815.ConnectorSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2817.CouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2817,
        )

        return self.__parent__._cast(_2817.CouplingHalfSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2820.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2820,
        )

        return self.__parent__._cast(_2820.CVTPulleySystemDeflection)

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2832.CylindricalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2832,
        )

        return self.__parent__._cast(_2832.CylindricalGearSystemDeflection)

    @property
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2833.CylindricalGearSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2833,
        )

        return self.__parent__._cast(_2833.CylindricalGearSystemDeflectionTimestep)

    @property
    def cylindrical_gear_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2834.CylindricalGearSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2834,
        )

        return self.__parent__._cast(
            _2834.CylindricalGearSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2837.CylindricalPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2837,
        )

        return self.__parent__._cast(_2837.CylindricalPlanetGearSystemDeflection)

    @property
    def face_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2843.FaceGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2843,
        )

        return self.__parent__._cast(_2843.FaceGearSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_2848.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2848,
        )

        return self.__parent__._cast(_2848.GearSystemDeflection)

    @property
    def hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2852.HypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2852,
        )

        return self.__parent__._cast(_2852.HypoidGearSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2857.KlingelnbergCycloPalloidConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2857,
        )

        return self.__parent__._cast(
            _2857.KlingelnbergCycloPalloidConicalGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2860.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2860,
        )

        return self.__parent__._cast(
            _2860.KlingelnbergCycloPalloidHypoidGearSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2863.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2863,
        )

        return self.__parent__._cast(
            _2863.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
        )

    @property
    def mass_disc_system_deflection(
        self: "CastSelf",
    ) -> "_2866.MassDiscSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2866,
        )

        return self.__parent__._cast(_2866.MassDiscSystemDeflection)

    @property
    def measurement_component_system_deflection(
        self: "CastSelf",
    ) -> "_2867.MeasurementComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2867,
        )

        return self.__parent__._cast(_2867.MeasurementComponentSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_2873.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2873,
        )

        return self.__parent__._cast(_2873.OilSealSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2876.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2876,
        )

        return self.__parent__._cast(_2876.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def planet_carrier_system_deflection(
        self: "CastSelf",
    ) -> "_2879.PlanetCarrierSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2879,
        )

        return self.__parent__._cast(_2879.PlanetCarrierSystemDeflection)

    @property
    def point_load_system_deflection(
        self: "CastSelf",
    ) -> "_2880.PointLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2880,
        )

        return self.__parent__._cast(_2880.PointLoadSystemDeflection)

    @property
    def power_load_system_deflection(
        self: "CastSelf",
    ) -> "_2881.PowerLoadSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2881,
        )

        return self.__parent__._cast(_2881.PowerLoadSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_2882.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2882,
        )

        return self.__parent__._cast(_2882.PulleySystemDeflection)

    @property
    def ring_pins_system_deflection(
        self: "CastSelf",
    ) -> "_2883.RingPinsSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2883,
        )

        return self.__parent__._cast(_2883.RingPinsSystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_2888.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2888,
        )

        return self.__parent__._cast(_2888.RollingRingSystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2890.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2890,
        )

        return self.__parent__._cast(_2890.ShaftHubConnectionSystemDeflection)

    @property
    def spiral_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2898.SpiralBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2898,
        )

        return self.__parent__._cast(_2898.SpiralBevelGearSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_2900.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2900,
        )

        return self.__parent__._cast(_2900.SpringDamperHalfSystemDeflection)

    @property
    def straight_bevel_diff_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2904.StraightBevelDiffGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2904,
        )

        return self.__parent__._cast(_2904.StraightBevelDiffGearSystemDeflection)

    @property
    def straight_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2907.StraightBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2907,
        )

        return self.__parent__._cast(_2907.StraightBevelGearSystemDeflection)

    @property
    def straight_bevel_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2908.StraightBevelPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2908,
        )

        return self.__parent__._cast(_2908.StraightBevelPlanetGearSystemDeflection)

    @property
    def straight_bevel_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2909.StraightBevelSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2909,
        )

        return self.__parent__._cast(_2909.StraightBevelSunGearSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_2910.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2910,
        )

        return self.__parent__._cast(_2910.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_2911.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2911,
        )

        return self.__parent__._cast(_2911.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_2912.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2912,
        )

        return self.__parent__._cast(_2912.SynchroniserSleeveSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_2918.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2918,
        )

        return self.__parent__._cast(_2918.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_2920.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2920,
        )

        return self.__parent__._cast(_2920.TorqueConverterTurbineSystemDeflection)

    @property
    def unbalanced_mass_system_deflection(
        self: "CastSelf",
    ) -> "_2923.UnbalancedMassSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2923,
        )

        return self.__parent__._cast(_2923.UnbalancedMassSystemDeflection)

    @property
    def virtual_component_system_deflection(
        self: "CastSelf",
    ) -> "_2924.VirtualComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2924,
        )

        return self.__parent__._cast(_2924.VirtualComponentSystemDeflection)

    @property
    def worm_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2927.WormGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2927,
        )

        return self.__parent__._cast(_2927.WormGearSystemDeflection)

    @property
    def zerol_bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2930.ZerolBevelGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2930,
        )

        return self.__parent__._cast(_2930.ZerolBevelGearSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "MountableComponentSystemDeflection":
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
class MountableComponentSystemDeflection(_2802.ComponentSystemDeflection):
    """MountableComponentSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def dip_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DipFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2522.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_fe_part(self: "Self") -> "_2844.FEPartSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.FEPartSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerFEPart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_fe_substructure_nodes(self: "Self") -> "List[_2441.FESubstructureNode]":
        """List[mastapy.system_model.fe.FESubstructureNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerFESubstructureNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_flow_results(self: "Self") -> "_4221.MountableComponentPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentSystemDeflection
        """
        return _Cast_MountableComponentSystemDeflection(self)
