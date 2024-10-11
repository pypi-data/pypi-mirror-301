"""MountableComponentPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4164

_MOUNTABLE_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "MountableComponentPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4144,
        _4147,
        _4151,
        _4153,
        _4154,
        _4156,
        _4161,
        _4166,
        _4169,
        _4172,
        _4175,
        _4177,
        _4181,
        _4188,
        _4190,
        _4194,
        _4201,
        _4205,
        _4209,
        _4212,
        _4215,
        _4217,
        _4218,
        _4222,
        _4223,
        _4225,
        _4229,
        _4230,
        _4233,
        _4234,
        _4235,
        _4239,
        _4241,
        _4246,
        _4249,
        _4252,
        _4255,
        _4257,
        _4258,
        _4259,
        _4260,
        _4262,
        _4266,
        _4267,
        _4268,
        _4269,
        _4271,
        _4274,
    )
    from mastapy._private.system_model.part_model import _2522

    Self = TypeVar("Self", bound="MountableComponentPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentPowerFlow._Cast_MountableComponentPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentPowerFlow:
    """Special nested class for casting MountableComponentPowerFlow to subclasses."""

    __parent__: "MountableComponentPowerFlow"

    @property
    def component_power_flow(self: "CastSelf") -> "_4164.ComponentPowerFlow":
        return self.__parent__._cast(_4164.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4223.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartPowerFlow)

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
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4144.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(_4144.AGMAGleasonConicalGearPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4147.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4147

        return self.__parent__._cast(_4147.BearingPowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4151.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4153.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4154.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4156.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BevelGearPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4161.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ClutchHalfPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4166.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptCouplingHalfPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4169.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConceptGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4172.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConicalGearPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4175.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4177.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.CouplingHalfPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4181.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4181

        return self.__parent__._cast(_4181.CVTPulleyPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4188.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4188

        return self.__parent__._cast(_4188.CylindricalGearPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4190.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4190

        return self.__parent__._cast(_4190.CylindricalPlanetGearPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4194.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4194

        return self.__parent__._cast(_4194.FaceGearPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4201.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4201

        return self.__parent__._cast(_4201.GearPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4205.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4205

        return self.__parent__._cast(_4205.HypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(_4212.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4215.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(
            _4215.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4217.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(_4217.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MeasurementComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4222.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4222

        return self.__parent__._cast(_4222.OilSealPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4225.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PartToPartShearCouplingHalfPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4229.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4229

        return self.__parent__._cast(_4229.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4230.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4230

        return self.__parent__._cast(_4230.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4233.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4233

        return self.__parent__._cast(_4233.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4234.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4235.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4235

        return self.__parent__._cast(_4235.RingPinsPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4239.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.RollingRingPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4241.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.ShaftHubConnectionPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpiralBevelGearPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4249.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.SpringDamperHalfPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4257.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4258.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4260.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4260

        return self.__parent__._cast(_4260.SynchroniserPartPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4262.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4266.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4267.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4268.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4268

        return self.__parent__._cast(_4268.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4269.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4271.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.WormGearPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4274.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4274

        return self.__parent__._cast(_4274.ZerolBevelGearPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "MountableComponentPowerFlow":
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
class MountableComponentPowerFlow(_4164.ComponentPowerFlow):
    """MountableComponentPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_MountableComponentPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentPowerFlow
        """
        return _Cast_MountableComponentPowerFlow(self)
