"""SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6396,
)

_SYNCHRONISER_HALF_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6263,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6304,
        _6318,
        _6358,
        _6360,
    )
    from mastapy._private.system_model.part_model.couplings import _2669

    Self = TypeVar(
        "Self", bound="SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation._Cast_SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def synchroniser_part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6396.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6396.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6318.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6318,
        )

        return self.__parent__._cast(
            _6318.CouplingHalfCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mountable_component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6358.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6358,
        )

        return self.__parent__._cast(
            _6358.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6304.ComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6304,
        )

        return self.__parent__._cast(
            _6304.ComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6360.PartCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6360,
        )

        return self.__parent__._cast(
            _6360.PartCompoundHarmonicAnalysisOfSingleExcitation
        )

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
    def synchroniser_half_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation":
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
class SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation(
    _6396.SynchroniserPartCompoundHarmonicAnalysisOfSingleExcitation
):
    """SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SYNCHRONISER_HALF_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2669.SynchroniserHalf":
        """mastapy.system_model.part_model.couplings.SynchroniserHalf

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
    ) -> "List[_6263.SynchroniserHalfHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.SynchroniserHalfHarmonicAnalysisOfSingleExcitation]

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
    ) -> "List[_6263.SynchroniserHalfHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.SynchroniserHalfHarmonicAnalysisOfSingleExcitation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_SynchroniserHalfCompoundHarmonicAnalysisOfSingleExcitation(self)
