"""StraightBevelDiffGearSetCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4020,
)

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "StraightBevelDiffGearSetCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3979,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4002,
        _4008,
        _4036,
        _4062,
        _4083,
        _4102,
        _4109,
        _4110,
    )
    from mastapy._private.system_model.part_model.gears import _2605

    Self = TypeVar("Self", bound="StraightBevelDiffGearSetCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetCompoundStabilityAnalysis._Cast_StraightBevelDiffGearSetCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetCompoundStabilityAnalysis:
    """Special nested class for casting StraightBevelDiffGearSetCompoundStabilityAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearSetCompoundStabilityAnalysis"

    @property
    def bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.BevelGearSetCompoundStabilityAnalysis":
        return self.__parent__._cast(_4020.BevelGearSetCompoundStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4008.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4008,
        )

        return self.__parent__._cast(
            _4008.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.ConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4036,
        )

        return self.__parent__._cast(_4036.ConicalGearSetCompoundStabilityAnalysis)

    @property
    def gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.GearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4062,
        )

        return self.__parent__._cast(_4062.GearSetCompoundStabilityAnalysis)

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4102.SpecialisedAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4102,
        )

        return self.__parent__._cast(_4102.SpecialisedAssemblyCompoundStabilityAnalysis)

    @property
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4002.AbstractAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4002,
        )

        return self.__parent__._cast(_4002.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4083.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4083,
        )

        return self.__parent__._cast(_4083.PartCompoundStabilityAnalysis)

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
    def straight_bevel_diff_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetCompoundStabilityAnalysis":
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
class StraightBevelDiffGearSetCompoundStabilityAnalysis(
    _4020.BevelGearSetCompoundStabilityAnalysis
):
    """StraightBevelDiffGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

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
    ) -> "List[_3979.StraightBevelDiffGearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.StraightBevelDiffGearSetStabilityAnalysis]

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
    def straight_bevel_diff_gears_compound_stability_analysis(
        self: "Self",
    ) -> "List[_4109.StraightBevelDiffGearCompoundStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.compound.StraightBevelDiffGearCompoundStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffGearsCompoundStabilityAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_meshes_compound_stability_analysis(
        self: "Self",
    ) -> "List[_4110.StraightBevelDiffGearMeshCompoundStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.compound.StraightBevelDiffGearMeshCompoundStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffMeshesCompoundStabilityAnalysis"
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
    ) -> "List[_3979.StraightBevelDiffGearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.StraightBevelDiffGearSetStabilityAnalysis]

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
    ) -> "_Cast_StraightBevelDiffGearSetCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetCompoundStabilityAnalysis
        """
        return _Cast_StraightBevelDiffGearSetCompoundStabilityAnalysis(self)
