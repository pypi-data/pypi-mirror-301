"""ConceptCouplingCompoundCriticalSpeedAnalysis"""

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
    _6860,
)

_CONCEPT_COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "ConceptCouplingCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6716,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6823,
        _6904,
        _6923,
    )
    from mastapy._private.system_model.part_model.couplings import _2641

    Self = TypeVar("Self", bound="ConceptCouplingCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConceptCouplingCompoundCriticalSpeedAnalysis._Cast_ConceptCouplingCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConceptCouplingCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConceptCouplingCompoundCriticalSpeedAnalysis:
    """Special nested class for casting ConceptCouplingCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "ConceptCouplingCompoundCriticalSpeedAnalysis"

    @property
    def coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6860.CouplingCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(_6860.CouplingCompoundCriticalSpeedAnalysis)

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6923,
        )

        return self.__parent__._cast(
            _6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def abstract_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6823.AbstractAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6823,
        )

        return self.__parent__._cast(
            _6823.AbstractAssemblyCompoundCriticalSpeedAnalysis
        )

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
    def concept_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ConceptCouplingCompoundCriticalSpeedAnalysis":
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
class ConceptCouplingCompoundCriticalSpeedAnalysis(
    _6860.CouplingCompoundCriticalSpeedAnalysis
):
    """ConceptCouplingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONCEPT_COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2641.ConceptCoupling":
        """mastapy.system_model.part_model.couplings.ConceptCoupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2641.ConceptCoupling":
        """mastapy.system_model.part_model.couplings.ConceptCoupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6716.ConceptCouplingCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConceptCouplingCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6716.ConceptCouplingCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConceptCouplingCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConceptCouplingCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConceptCouplingCompoundCriticalSpeedAnalysis
        """
        return _Cast_ConceptCouplingCompoundCriticalSpeedAnalysis(self)
