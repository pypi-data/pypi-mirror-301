"""AbstractShaftOrHousingHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5839

_ABSTRACT_SHAFT_OR_HOUSING_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "AbstractShaftOrHousingHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5814,
        _5859,
        _5884,
        _5924,
        _5942,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2773,
    )
    from mastapy._private.system_model.part_model import _2492

    Self = TypeVar("Self", bound="AbstractShaftOrHousingHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingHarmonicAnalysis._Cast_AbstractShaftOrHousingHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingHarmonicAnalysis:
    """Special nested class for casting AbstractShaftOrHousingHarmonicAnalysis to subclasses."""

    __parent__: "AbstractShaftOrHousingHarmonicAnalysis"

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5839.ComponentHarmonicAnalysis":
        return self.__parent__._cast(_5839.ComponentHarmonicAnalysis)

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
    def abstract_shaft_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5814.AbstractShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5814,
        )

        return self.__parent__._cast(_5814.AbstractShaftHarmonicAnalysis)

    @property
    def cycloidal_disc_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5859.CycloidalDiscHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5859,
        )

        return self.__parent__._cast(_5859.CycloidalDiscHarmonicAnalysis)

    @property
    def fe_part_harmonic_analysis(self: "CastSelf") -> "_5884.FEPartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5884,
        )

        return self.__parent__._cast(_5884.FEPartHarmonicAnalysis)

    @property
    def shaft_harmonic_analysis(self: "CastSelf") -> "_5942.ShaftHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5942,
        )

        return self.__parent__._cast(_5942.ShaftHarmonicAnalysis)

    @property
    def abstract_shaft_or_housing_harmonic_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingHarmonicAnalysis":
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
class AbstractShaftOrHousingHarmonicAnalysis(_5839.ComponentHarmonicAnalysis):
    """AbstractShaftOrHousingHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2492.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2773.AbstractShaftOrHousingSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingHarmonicAnalysis
        """
        return _Cast_AbstractShaftOrHousingHarmonicAnalysis(self)
