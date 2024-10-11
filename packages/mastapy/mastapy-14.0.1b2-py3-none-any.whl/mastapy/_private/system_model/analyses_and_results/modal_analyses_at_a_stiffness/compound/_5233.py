"""VirtualComponentCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5188,
)

_VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "VirtualComponentCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5102,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5134,
        _5184,
        _5185,
        _5190,
        _5197,
        _5198,
        _5232,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundModalAnalysisAtAStiffness._Cast_VirtualComponentCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting VirtualComponentCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "VirtualComponentCompoundModalAnalysisAtAStiffness"

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5188.MountableComponentCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5188.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5134.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5134,
        )

        return self.__parent__._cast(_5134.ComponentCompoundModalAnalysisAtAStiffness)

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
    def mass_disc_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5184.MassDiscCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5184,
        )

        return self.__parent__._cast(_5184.MassDiscCompoundModalAnalysisAtAStiffness)

    @property
    def measurement_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5185.MeasurementComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5185,
        )

        return self.__parent__._cast(
            _5185.MeasurementComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def point_load_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5197.PointLoadCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5197,
        )

        return self.__parent__._cast(_5197.PointLoadCompoundModalAnalysisAtAStiffness)

    @property
    def power_load_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5198.PowerLoadCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5198,
        )

        return self.__parent__._cast(_5198.PowerLoadCompoundModalAnalysisAtAStiffness)

    @property
    def unbalanced_mass_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5232.UnbalancedMassCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5232,
        )

        return self.__parent__._cast(
            _5232.UnbalancedMassCompoundModalAnalysisAtAStiffness
        )

    @property
    def virtual_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundModalAnalysisAtAStiffness":
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
class VirtualComponentCompoundModalAnalysisAtAStiffness(
    _5188.MountableComponentCompoundModalAnalysisAtAStiffness
):
    """VirtualComponentCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5102.VirtualComponentModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.VirtualComponentModalAnalysisAtAStiffness]

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
    ) -> "List[_5102.VirtualComponentModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.VirtualComponentModalAnalysisAtAStiffness]

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
    ) -> "_Cast_VirtualComponentCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundModalAnalysisAtAStiffness
        """
        return _Cast_VirtualComponentCompoundModalAnalysisAtAStiffness(self)
