"""RootAssemblyCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4563,
)

_ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "RootAssemblyCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5793,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4502,
        _4503,
        _4521,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4556,
        _4637,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7101
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2992,
    )

    Self = TypeVar("Self", bound="RootAssemblyCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundParametricStudyTool._Cast_RootAssemblyCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundParametricStudyTool:
    """Special nested class for casting RootAssemblyCompoundParametricStudyTool to subclasses."""

    __parent__: "RootAssemblyCompoundParametricStudyTool"

    @property
    def assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4563.AssemblyCompoundParametricStudyTool":
        return self.__parent__._cast(_4563.AssemblyCompoundParametricStudyTool)

    @property
    def abstract_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4556.AbstractAssemblyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4556,
        )

        return self.__parent__._cast(_4556.AbstractAssemblyCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4637,
        )

        return self.__parent__._cast(_4637.PartCompoundParametricStudyTool)

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
    def root_assembly_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundParametricStudyTool":
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
class RootAssemblyCompoundParametricStudyTool(
    _4563.AssemblyCompoundParametricStudyTool
):
    """RootAssemblyCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def compound_load_case(self: "Self") -> "_5793.AbstractLoadCaseGroup":
        """mastapy.system_model.analyses_and_results.load_case_groups.AbstractLoadCaseGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CompoundLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def parametric_analysis_options(self: "Self") -> "_4502.ParametricStudyToolOptions":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7101.RootAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results_for_reporting(
        self: "Self",
    ) -> "_4503.ParametricStudyToolResultsForReporting":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolResultsForReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForReporting")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def root_assembly_duty_cycle_results(
        self: "Self",
    ) -> "_2992.DutyCycleEfficiencyResults":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.DutyCycleEfficiencyResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootAssemblyDutyCycleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4521.RootAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool]

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
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4521.RootAssemblyParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_RootAssemblyCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundParametricStudyTool
        """
        return _Cast_RootAssemblyCompoundParametricStudyTool(self)
