"""AbstractShaftOrHousingCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4581,
)

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "AbstractShaftOrHousingCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4408,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4557,
        _4601,
        _4612,
        _4637,
        _4653,
    )

    Self = TypeVar("Self", bound="AbstractShaftOrHousingCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingCompoundParametricStudyTool._Cast_AbstractShaftOrHousingCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingCompoundParametricStudyTool:
    """Special nested class for casting AbstractShaftOrHousingCompoundParametricStudyTool to subclasses."""

    __parent__: "AbstractShaftOrHousingCompoundParametricStudyTool"

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4581.ComponentCompoundParametricStudyTool":
        return self.__parent__._cast(_4581.ComponentCompoundParametricStudyTool)

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
    def abstract_shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4557.AbstractShaftCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4557,
        )

        return self.__parent__._cast(_4557.AbstractShaftCompoundParametricStudyTool)

    @property
    def cycloidal_disc_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4601.CycloidalDiscCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4601,
        )

        return self.__parent__._cast(_4601.CycloidalDiscCompoundParametricStudyTool)

    @property
    def fe_part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4612.FEPartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4612,
        )

        return self.__parent__._cast(_4612.FEPartCompoundParametricStudyTool)

    @property
    def shaft_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4653.ShaftCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4653,
        )

        return self.__parent__._cast(_4653.ShaftCompoundParametricStudyTool)

    @property
    def abstract_shaft_or_housing_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingCompoundParametricStudyTool":
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
class AbstractShaftOrHousingCompoundParametricStudyTool(
    _4581.ComponentCompoundParametricStudyTool
):
    """AbstractShaftOrHousingCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4408.AbstractShaftOrHousingParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4408.AbstractShaftOrHousingParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftOrHousingCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingCompoundParametricStudyTool
        """
        return _Cast_AbstractShaftOrHousingCompoundParametricStudyTool(self)
