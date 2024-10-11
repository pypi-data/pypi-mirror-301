"""ExternalCADModelCompoundStabilityAnalysis"""

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
    _4027,
)

_EXTERNAL_CAD_MODEL_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ExternalCADModelCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3920,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4083,
    )
    from mastapy._private.system_model.part_model import _2508

    Self = TypeVar("Self", bound="ExternalCADModelCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalCADModelCompoundStabilityAnalysis._Cast_ExternalCADModelCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelCompoundStabilityAnalysis:
    """Special nested class for casting ExternalCADModelCompoundStabilityAnalysis to subclasses."""

    __parent__: "ExternalCADModelCompoundStabilityAnalysis"

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4027.ComponentCompoundStabilityAnalysis":
        return self.__parent__._cast(_4027.ComponentCompoundStabilityAnalysis)

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
    def external_cad_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "ExternalCADModelCompoundStabilityAnalysis":
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
class ExternalCADModelCompoundStabilityAnalysis(
    _4027.ComponentCompoundStabilityAnalysis
):
    """ExternalCADModelCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_CAD_MODEL_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2508.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

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
    ) -> "List[_3920.ExternalCADModelStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ExternalCADModelStabilityAnalysis]

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
    ) -> "List[_3920.ExternalCADModelStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ExternalCADModelStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ExternalCADModelCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelCompoundStabilityAnalysis
        """
        return _Cast_ExternalCADModelCompoundStabilityAnalysis(self)
