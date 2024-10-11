"""GearSetCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6923,
)

_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "GearSetCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6752,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6823,
        _6829,
        _6836,
        _6841,
        _6854,
        _6857,
        _6872,
        _6878,
        _6887,
        _6891,
        _6894,
        _6897,
        _6904,
        _6909,
        _6926,
        _6932,
        _6935,
        _6950,
        _6953,
    )

    Self = TypeVar("Self", bound="GearSetCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetCompoundCriticalSpeedAnalysis._Cast_GearSetCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundCriticalSpeedAnalysis:
    """Special nested class for casting GearSetCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "GearSetCompoundCriticalSpeedAnalysis"

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def abstract_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6823.AbstractAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6823,
        )

        return self.__parent__._cast(
            _6823.AbstractAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6904.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6904,
        )

        return self.__parent__._cast(_6904.PartCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6829.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6829,
        )

        return self.__parent__._cast(
            _6829.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6836.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6836,
        )

        return self.__parent__._cast(
            _6836.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6841.BevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6841,
        )

        return self.__parent__._cast(_6841.BevelGearSetCompoundCriticalSpeedAnalysis)

    @property
    def concept_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6854.ConceptGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6854,
        )

        return self.__parent__._cast(_6854.ConceptGearSetCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6857,
        )

        return self.__parent__._cast(_6857.ConicalGearSetCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6872.CylindricalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6872,
        )

        return self.__parent__._cast(
            _6872.CylindricalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6878.FaceGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6878,
        )

        return self.__parent__._cast(_6878.FaceGearSetCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.HypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6887,
        )

        return self.__parent__._cast(_6887.HypoidGearSetCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6891.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6891,
        )

        return self.__parent__._cast(
            _6891.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6894,
        )

        return self.__parent__._cast(
            _6894.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6897.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6897,
        )

        return self.__parent__._cast(
            _6897.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def planetary_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6909.PlanetaryGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6909,
        )

        return self.__parent__._cast(
            _6909.PlanetaryGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6926.SpiralBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6926,
        )

        return self.__parent__._cast(
            _6926.SpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6932.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6932,
        )

        return self.__parent__._cast(
            _6932.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6935.StraightBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6935,
        )

        return self.__parent__._cast(
            _6935.StraightBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6950.WormGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6950,
        )

        return self.__parent__._cast(_6950.WormGearSetCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6953.ZerolBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6953,
        )

        return self.__parent__._cast(
            _6953.ZerolBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "GearSetCompoundCriticalSpeedAnalysis":
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
class GearSetCompoundCriticalSpeedAnalysis(
    _6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis
):
    """GearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6752.GearSetCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GearSetCriticalSpeedAnalysis]

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6752.GearSetCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GearSetCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundCriticalSpeedAnalysis
        """
        return _Cast_GearSetCompoundCriticalSpeedAnalysis(self)
