"""TorqueConverterCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5146,
)

_TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "TorqueConverterCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5098,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5109,
        _5190,
        _5209,
    )
    from mastapy._private.system_model.part_model.couplings import _2672

    Self = TypeVar("Self", bound="TorqueConverterCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterCompoundModalAnalysisAtAStiffness._Cast_TorqueConverterCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting TorqueConverterCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "TorqueConverterCompoundModalAnalysisAtAStiffness"

    @property
    def coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.CouplingCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5146.CouplingCompoundModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5209.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5209,
        )

        return self.__parent__._cast(
            _5209.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5109.AbstractAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5109,
        )

        return self.__parent__._cast(
            _5109.AbstractAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5190,
        )

        return self.__parent__._cast(_5190.PartCompoundModalAnalysisAtAStiffness)

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
    def torque_converter_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "TorqueConverterCompoundModalAnalysisAtAStiffness":
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
class TorqueConverterCompoundModalAnalysisAtAStiffness(
    _5146.CouplingCompoundModalAnalysisAtAStiffness
):
    """TorqueConverterCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2672.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2672.TorqueConverter":
        """mastapy.system_model.part_model.couplings.TorqueConverter

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
    ) -> "List[_5098.TorqueConverterModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.TorqueConverterModalAnalysisAtAStiffness]

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
    ) -> "List[_5098.TorqueConverterModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.TorqueConverterModalAnalysisAtAStiffness]

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
    ) -> "_Cast_TorqueConverterCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterCompoundModalAnalysisAtAStiffness
        """
        return _Cast_TorqueConverterCompoundModalAnalysisAtAStiffness(self)
