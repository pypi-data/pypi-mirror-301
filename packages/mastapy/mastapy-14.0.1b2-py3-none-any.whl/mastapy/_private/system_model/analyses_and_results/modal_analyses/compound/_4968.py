"""UnbalancedMassCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4969,
)

_UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "UnbalancedMassCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4822
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4870,
        _4924,
        _4926,
    )
    from mastapy._private.system_model.part_model import _2536

    Self = TypeVar("Self", bound="UnbalancedMassCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UnbalancedMassCompoundModalAnalysis._Cast_UnbalancedMassCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UnbalancedMassCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_UnbalancedMassCompoundModalAnalysis:
    """Special nested class for casting UnbalancedMassCompoundModalAnalysis to subclasses."""

    __parent__: "UnbalancedMassCompoundModalAnalysis"

    @property
    def virtual_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4969.VirtualComponentCompoundModalAnalysis":
        return self.__parent__._cast(_4969.VirtualComponentCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4924,
        )

        return self.__parent__._cast(_4924.MountableComponentCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4870,
        )

        return self.__parent__._cast(_4870.ComponentCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.PartCompoundModalAnalysis)

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
    def unbalanced_mass_compound_modal_analysis(
        self: "CastSelf",
    ) -> "UnbalancedMassCompoundModalAnalysis":
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
class UnbalancedMassCompoundModalAnalysis(_4969.VirtualComponentCompoundModalAnalysis):
    """UnbalancedMassCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _UNBALANCED_MASS_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2536.UnbalancedMass":
        """mastapy.system_model.part_model.UnbalancedMass

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4822.UnbalancedMassModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4822.UnbalancedMassModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.UnbalancedMassModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_UnbalancedMassCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_UnbalancedMassCompoundModalAnalysis
        """
        return _Cast_UnbalancedMassCompoundModalAnalysis(self)
