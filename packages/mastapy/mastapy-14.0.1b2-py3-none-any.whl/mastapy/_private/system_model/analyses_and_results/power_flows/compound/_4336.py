"""GearSetCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4376,
)

_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "GearSetCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating import _375
    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4202
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4276,
        _4282,
        _4289,
        _4294,
        _4307,
        _4310,
        _4325,
        _4331,
        _4340,
        _4344,
        _4347,
        _4350,
        _4357,
        _4362,
        _4379,
        _4385,
        _4388,
        _4403,
        _4406,
    )

    Self = TypeVar("Self", bound="GearSetCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetCompoundPowerFlow._Cast_GearSetCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundPowerFlow:
    """Special nested class for casting GearSetCompoundPowerFlow to subclasses."""

    __parent__: "GearSetCompoundPowerFlow"

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4376.SpecialisedAssemblyCompoundPowerFlow":
        return self.__parent__._cast(_4376.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4276.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4276,
        )

        return self.__parent__._cast(_4276.AbstractAssemblyCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4357.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4357,
        )

        return self.__parent__._cast(_4357.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7715.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def agma_gleason_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4282.AGMAGleasonConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4282,
        )

        return self.__parent__._cast(_4282.AGMAGleasonConicalGearSetCompoundPowerFlow)

    @property
    def bevel_differential_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4289.BevelDifferentialGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4289,
        )

        return self.__parent__._cast(_4289.BevelDifferentialGearSetCompoundPowerFlow)

    @property
    def bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4294.BevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4294,
        )

        return self.__parent__._cast(_4294.BevelGearSetCompoundPowerFlow)

    @property
    def concept_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4307.ConceptGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4307,
        )

        return self.__parent__._cast(_4307.ConceptGearSetCompoundPowerFlow)

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4310.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4310,
        )

        return self.__parent__._cast(_4310.ConicalGearSetCompoundPowerFlow)

    @property
    def cylindrical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4325.CylindricalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4325,
        )

        return self.__parent__._cast(_4325.CylindricalGearSetCompoundPowerFlow)

    @property
    def face_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4331.FaceGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4331,
        )

        return self.__parent__._cast(_4331.FaceGearSetCompoundPowerFlow)

    @property
    def hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4340.HypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4340,
        )

        return self.__parent__._cast(_4340.HypoidGearSetCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4344.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4344,
        )

        return self.__parent__._cast(
            _4344.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4347.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4347,
        )

        return self.__parent__._cast(
            _4347.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4350.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4350,
        )

        return self.__parent__._cast(
            _4350.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
        )

    @property
    def planetary_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4362.PlanetaryGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4362,
        )

        return self.__parent__._cast(_4362.PlanetaryGearSetCompoundPowerFlow)

    @property
    def spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4379.SpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4379,
        )

        return self.__parent__._cast(_4379.SpiralBevelGearSetCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4385.StraightBevelDiffGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4385,
        )

        return self.__parent__._cast(_4385.StraightBevelDiffGearSetCompoundPowerFlow)

    @property
    def straight_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4388.StraightBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4388,
        )

        return self.__parent__._cast(_4388.StraightBevelGearSetCompoundPowerFlow)

    @property
    def worm_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4403.WormGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4403,
        )

        return self.__parent__._cast(_4403.WormGearSetCompoundPowerFlow)

    @property
    def zerol_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4406.ZerolBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4406,
        )

        return self.__parent__._cast(_4406.ZerolBevelGearSetCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(self: "CastSelf") -> "GearSetCompoundPowerFlow":
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
class GearSetCompoundPowerFlow(_4376.SpecialisedAssemblyCompoundPowerFlow):
    """GearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_set_duty_cycle_rating(self: "Self") -> "_375.GearSetDutyCycleRating":
        """mastapy.gears.rating.GearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4202.GearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(self: "Self") -> "List[_4202.GearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundPowerFlow
        """
        return _Cast_GearSetCompoundPowerFlow(self)
