"""GuideDxfModelCompoundCriticalSpeedAnalysis"""

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
    _6848,
)

_GUIDE_DXF_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "GuideDxfModelCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6753,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6904,
    )
    from mastapy._private.system_model.part_model import _2511

    Self = TypeVar("Self", bound="GuideDxfModelCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GuideDxfModelCompoundCriticalSpeedAnalysis._Cast_GuideDxfModelCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GuideDxfModelCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideDxfModelCompoundCriticalSpeedAnalysis:
    """Special nested class for casting GuideDxfModelCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "GuideDxfModelCompoundCriticalSpeedAnalysis"

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6848.ComponentCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6848.ComponentCompoundCriticalSpeedAnalysis)

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
    def guide_dxf_model_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "GuideDxfModelCompoundCriticalSpeedAnalysis":
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
class GuideDxfModelCompoundCriticalSpeedAnalysis(
    _6848.ComponentCompoundCriticalSpeedAnalysis
):
    """GuideDxfModelCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_DXF_MODEL_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2511.GuideDxfModel":
        """mastapy.system_model.part_model.GuideDxfModel

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
    ) -> "List[_6753.GuideDxfModelCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GuideDxfModelCriticalSpeedAnalysis]

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
    ) -> "List[_6753.GuideDxfModelCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GuideDxfModelCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GuideDxfModelCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GuideDxfModelCompoundCriticalSpeedAnalysis
        """
        return _Cast_GuideDxfModelCompoundCriticalSpeedAnalysis(self)
