"""PulleyDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6458

_PULLEY_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "PulleyDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6444,
        _6461,
        _6500,
        _6502,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7093
    from mastapy._private.system_model.part_model.couplings import _2652

    Self = TypeVar("Self", bound="PulleyDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="PulleyDynamicAnalysis._Cast_PulleyDynamicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PulleyDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PulleyDynamicAnalysis:
    """Special nested class for casting PulleyDynamicAnalysis to subclasses."""

    __parent__: "PulleyDynamicAnalysis"

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6458.CouplingHalfDynamicAnalysis":
        return self.__parent__._cast(_6458.CouplingHalfDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6500.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6500,
        )

        return self.__parent__._cast(_6500.MountableComponentDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6444.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6444,
        )

        return self.__parent__._cast(_6444.ComponentDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6502.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6502,
        )

        return self.__parent__._cast(_6502.PartDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2740.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def cvt_pulley_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6461.CVTPulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6461,
        )

        return self.__parent__._cast(_6461.CVTPulleyDynamicAnalysis)

    @property
    def pulley_dynamic_analysis(self: "CastSelf") -> "PulleyDynamicAnalysis":
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
class PulleyDynamicAnalysis(_6458.CouplingHalfDynamicAnalysis):
    """PulleyDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PULLEY_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2652.Pulley":
        """mastapy.system_model.part_model.couplings.Pulley

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7093.PulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PulleyDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PulleyDynamicAnalysis
        """
        return _Cast_PulleyDynamicAnalysis(self)
