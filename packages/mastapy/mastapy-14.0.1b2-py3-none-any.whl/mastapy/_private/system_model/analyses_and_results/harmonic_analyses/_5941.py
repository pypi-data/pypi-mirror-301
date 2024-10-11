"""RootAssemblyHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2742
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5820

_ROOT_ASSEMBLY_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "RootAssemblyHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5812,
        _5895,
        _5901,
        _5924,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6012,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2889,
    )
    from mastapy._private.system_model.part_model import _2533

    Self = TypeVar("Self", bound="RootAssemblyHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyHarmonicAnalysis._Cast_RootAssemblyHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyHarmonicAnalysis:
    """Special nested class for casting RootAssemblyHarmonicAnalysis to subclasses."""

    __parent__: "RootAssemblyHarmonicAnalysis"

    @property
    def assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5820.AssemblyHarmonicAnalysis":
        return self.__parent__._cast(_5820.AssemblyHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5812.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5812,
        )

        return self.__parent__._cast(_5812.AbstractAssemblyHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5924.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5924,
        )

        return self.__parent__._cast(_5924.PartHarmonicAnalysis)

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
    def root_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "RootAssemblyHarmonicAnalysis":
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
class RootAssemblyHarmonicAnalysis(
    _5820.AssemblyHarmonicAnalysis, _2742.IHaveRootHarmonicAnalysisResults
):
    """RootAssemblyHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2533.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def export(self: "Self") -> "_5901.HarmonicAnalysisRootAssemblyExportOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisRootAssemblyExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Export")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis_inputs(self: "Self") -> "_5895.HarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisInputs")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results(
        self: "Self",
    ) -> "_6012.RootAssemblyHarmonicAnalysisResultsPropertyAccessor":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.RootAssemblyHarmonicAnalysisResultsPropertyAccessor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2889.RootAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyHarmonicAnalysis
        """
        return _Cast_RootAssemblyHarmonicAnalysis(self)
