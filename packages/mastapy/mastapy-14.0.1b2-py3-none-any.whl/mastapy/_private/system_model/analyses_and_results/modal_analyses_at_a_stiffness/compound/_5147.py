"""CouplingConnectionCompoundModalAnalysisAtAStiffness"""

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
    _5174,
)

_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "CouplingConnectionCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5013,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5131,
        _5136,
        _5144,
        _5192,
        _5214,
        _5229,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundModalAnalysisAtAStiffness._Cast_CouplingConnectionCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting CouplingConnectionCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "CouplingConnectionCompoundModalAnalysisAtAStiffness"

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5174.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5174.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5144.ConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5144,
        )

        return self.__parent__._cast(_5144.ConnectionCompoundModalAnalysisAtAStiffness)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def clutch_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5131.ClutchConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5131,
        )

        return self.__parent__._cast(
            _5131.ClutchConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5136.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5136,
        )

        return self.__parent__._cast(
            _5136.ConceptCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5192.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5192,
        )

        return self.__parent__._cast(
            _5192.PartToPartShearCouplingConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def spring_damper_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5214.SpringDamperConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5214,
        )

        return self.__parent__._cast(
            _5214.SpringDamperConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5229.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5229,
        )

        return self.__parent__._cast(
            _5229.TorqueConverterConnectionCompoundModalAnalysisAtAStiffness
        )

    @property
    def coupling_connection_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundModalAnalysisAtAStiffness":
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
class CouplingConnectionCompoundModalAnalysisAtAStiffness(
    _5174.InterMountableComponentConnectionCompoundModalAnalysisAtAStiffness
):
    """CouplingConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5013.CouplingConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CouplingConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5013.CouplingConnectionModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.CouplingConnectionModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CouplingConnectionCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundModalAnalysisAtAStiffness
        """
        return _Cast_CouplingConnectionCompoundModalAnalysisAtAStiffness(self)
