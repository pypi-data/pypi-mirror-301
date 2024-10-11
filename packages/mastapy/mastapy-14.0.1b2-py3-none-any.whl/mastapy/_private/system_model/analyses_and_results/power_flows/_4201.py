"""GearPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4221

_GEAR_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "GearPowerFlow"
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
        _4151,
        _4153,
        _4154,
        _4156,
        _4164,
        _4169,
        _4172,
        _4188,
        _4190,
        _4194,
        _4205,
        _4209,
        _4212,
        _4215,
        _4223,
        _4246,
        _4252,
        _4255,
        _4257,
        _4258,
        _4271,
        _4274,
    )
    from mastapy._private.system_model.part_model.gears import _2589

    Self = TypeVar("Self", bound="GearPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="GearPowerFlow._Cast_GearPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("GearPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearPowerFlow:
    """Special nested class for casting GearPowerFlow to subclasses."""

    __parent__: "GearPowerFlow"

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4221.MountableComponentPowerFlow":
        return self.__parent__._cast(_4221.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4164.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

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
    def concept_gear_power_flow(self: "CastSelf") -> "_4169.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConceptGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4172.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConicalGearPowerFlow)

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
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpiralBevelGearPowerFlow)

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
    def gear_power_flow(self: "CastSelf") -> "GearPowerFlow":
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
class GearPowerFlow(_4221.MountableComponentPowerFlow):
    """GearPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoaded")

        if temp is None:
            return False

        return temp

    @property
    def component_design(self: "Self") -> "_2589.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_GearPowerFlow
        """
        return _Cast_GearPowerFlow(self)
