"""RootAssemblyCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5379,
)

_ROOT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "RootAssemblyCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5337,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5372,
        _5453,
    )

    Self = TypeVar("Self", bound="RootAssemblyCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundModalAnalysisAtASpeed._Cast_RootAssemblyCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundModalAnalysisAtASpeed:
    """Special nested class for casting RootAssemblyCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "RootAssemblyCompoundModalAnalysisAtASpeed"

    @property
    def assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5379.AssemblyCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(_5379.AssemblyCompoundModalAnalysisAtASpeed)

    @property
    def abstract_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5372.AbstractAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5372,
        )

        return self.__parent__._cast(
            _5372.AbstractAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5453,
        )

        return self.__parent__._cast(_5453.PartCompoundModalAnalysisAtASpeed)

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
    def root_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundModalAnalysisAtASpeed":
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
class RootAssemblyCompoundModalAnalysisAtASpeed(
    _5379.AssemblyCompoundModalAnalysisAtASpeed
):
    """RootAssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5337.RootAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.RootAssemblyModalAnalysisAtASpeed]

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
    ) -> "List[_5337.RootAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.RootAssemblyModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_RootAssemblyCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundModalAnalysisAtASpeed
        """
        return _Cast_RootAssemblyCompoundModalAnalysisAtASpeed(self)
