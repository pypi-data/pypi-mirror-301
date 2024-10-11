"""RingPinsHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6227,
)

_RING_PINS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "RingPinsHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6171,
        _6229,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7096
    from mastapy._private.system_model.part_model.cycloidal import _2629

    Self = TypeVar("Self", bound="RingPinsHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RingPinsHarmonicAnalysisOfSingleExcitation._Cast_RingPinsHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinsHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinsHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting RingPinsHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "RingPinsHarmonicAnalysisOfSingleExcitation"

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6227.MountableComponentHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6227.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6171.ComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6171,
        )

        return self.__parent__._cast(_6171.ComponentHarmonicAnalysisOfSingleExcitation)

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6229.PartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6229,
        )

        return self.__parent__._cast(_6229.PartHarmonicAnalysisOfSingleExcitation)

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
    def ring_pins_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "RingPinsHarmonicAnalysisOfSingleExcitation":
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
class RingPinsHarmonicAnalysisOfSingleExcitation(
    _6227.MountableComponentHarmonicAnalysisOfSingleExcitation
):
    """RingPinsHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PINS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2629.RingPins":
        """mastapy.system_model.part_model.cycloidal.RingPins

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7096.RingPinsLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.RingPinsLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RingPinsHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_RingPinsHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_RingPinsHarmonicAnalysisOfSingleExcitation(self)
