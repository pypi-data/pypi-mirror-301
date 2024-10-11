"""FlexiblePinAssemblyDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6521

_FLEXIBLE_PIN_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "FlexiblePinAssemblyDynamicAnalysis",
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
        _6419,
        _6502,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7039
    from mastapy._private.system_model.part_model import _2510

    Self = TypeVar("Self", bound="FlexiblePinAssemblyDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAssemblyDynamicAnalysis._Cast_FlexiblePinAssemblyDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAssemblyDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAssemblyDynamicAnalysis:
    """Special nested class for casting FlexiblePinAssemblyDynamicAnalysis to subclasses."""

    __parent__: "FlexiblePinAssemblyDynamicAnalysis"

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6521.SpecialisedAssemblyDynamicAnalysis":
        return self.__parent__._cast(_6521.SpecialisedAssemblyDynamicAnalysis)

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6419.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6419,
        )

        return self.__parent__._cast(_6419.AbstractAssemblyDynamicAnalysis)

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
    def flexible_pin_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "FlexiblePinAssemblyDynamicAnalysis":
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
class FlexiblePinAssemblyDynamicAnalysis(_6521.SpecialisedAssemblyDynamicAnalysis):
    """FlexiblePinAssemblyDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ASSEMBLY_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2510.FlexiblePinAssembly":
        """mastapy.system_model.part_model.FlexiblePinAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7039.FlexiblePinAssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAssemblyDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAssemblyDynamicAnalysis
        """
        return _Cast_FlexiblePinAssemblyDynamicAnalysis(self)
