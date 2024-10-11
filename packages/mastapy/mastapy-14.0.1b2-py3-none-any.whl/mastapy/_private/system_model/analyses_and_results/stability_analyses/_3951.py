"""PartToPartShearCouplingHalfStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3904

_PART_TO_PART_SHEAR_COUPLING_HALF_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "PartToPartShearCouplingHalfStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3891,
        _3947,
        _3949,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7083
    from mastapy._private.system_model.part_model.couplings import _2650

    Self = TypeVar("Self", bound="PartToPartShearCouplingHalfStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingHalfStabilityAnalysis._Cast_PartToPartShearCouplingHalfStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingHalfStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingHalfStabilityAnalysis:
    """Special nested class for casting PartToPartShearCouplingHalfStabilityAnalysis to subclasses."""

    __parent__: "PartToPartShearCouplingHalfStabilityAnalysis"

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3904.CouplingHalfStabilityAnalysis":
        return self.__parent__._cast(_3904.CouplingHalfStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3947.MountableComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3947,
        )

        return self.__parent__._cast(_3947.MountableComponentStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_3891.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3891,
        )

        return self.__parent__._cast(_3891.ComponentStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_3949.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3949,
        )

        return self.__parent__._cast(_3949.PartStabilityAnalysis)

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
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingHalfStabilityAnalysis":
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
class PartToPartShearCouplingHalfStabilityAnalysis(_3904.CouplingHalfStabilityAnalysis):
    """PartToPartShearCouplingHalfStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_TO_PART_SHEAR_COUPLING_HALF_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2650.PartToPartShearCouplingHalf":
        """mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(
        self: "Self",
    ) -> "_7083.PartToPartShearCouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartToPartShearCouplingHalfStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingHalfStabilityAnalysis
        """
        return _Cast_PartToPartShearCouplingHalfStabilityAnalysis(self)
