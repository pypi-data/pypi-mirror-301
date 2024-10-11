"""StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6841,
)

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6801,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6823,
        _6829,
        _6857,
        _6883,
        _6904,
        _6923,
        _6930,
        _6931,
    )
    from mastapy._private.system_model.part_model.gears import _2605

    Self = TypeVar(
        "Self", bound="StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis._Cast_StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis:
    """Special nested class for casting StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis"

    @property
    def bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6841.BevelGearSetCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6841.BevelGearSetCompoundCriticalSpeedAnalysis)

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
    def conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6857,
        )

        return self.__parent__._cast(_6857.ConicalGearSetCompoundCriticalSpeedAnalysis)

    @property
    def gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6883.GearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6883,
        )

        return self.__parent__._cast(_6883.GearSetCompoundCriticalSpeedAnalysis)

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6923,
        )

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
    def straight_bevel_diff_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
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
class StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis(
    _6841.BevelGearSetCompoundCriticalSpeedAnalysis
):
    """StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2605.StraightBevelDiffGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2605.StraightBevelDiffGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6801.StraightBevelDiffGearSetCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearSetCriticalSpeedAnalysis]

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
    def straight_bevel_diff_gears_compound_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6930.StraightBevelDiffGearCompoundCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.compound.StraightBevelDiffGearCompoundCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffGearsCompoundCriticalSpeedAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_meshes_compound_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6931.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.compound.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffMeshesCompoundCriticalSpeedAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6801.StraightBevelDiffGearSetCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearSetCriticalSpeedAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
        """
        return _Cast_StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis(self)
