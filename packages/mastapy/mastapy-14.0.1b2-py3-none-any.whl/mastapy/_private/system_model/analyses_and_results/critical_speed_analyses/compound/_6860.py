"""CouplingCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6923,
)

_COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "CouplingCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6727,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6823,
        _6844,
        _6849,
        _6904,
        _6905,
        _6927,
        _6942,
    )

    Self = TypeVar("Self", bound="CouplingCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundCriticalSpeedAnalysis._Cast_CouplingCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundCriticalSpeedAnalysis:
    """Special nested class for casting CouplingCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "CouplingCompoundCriticalSpeedAnalysis"

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
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
    def clutch_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6844.ClutchCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6844,
        )

        return self.__parent__._cast(_6844.ClutchCompoundCriticalSpeedAnalysis)

    @property
    def concept_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6849.ConceptCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6849,
        )

        return self.__parent__._cast(_6849.ConceptCouplingCompoundCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6905.PartToPartShearCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6905,
        )

        return self.__parent__._cast(
            _6905.PartToPartShearCouplingCompoundCriticalSpeedAnalysis
        )

    @property
    def spring_damper_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.SpringDamperCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6927,
        )

        return self.__parent__._cast(_6927.SpringDamperCompoundCriticalSpeedAnalysis)

    @property
    def torque_converter_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6942.TorqueConverterCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6942,
        )

        return self.__parent__._cast(_6942.TorqueConverterCompoundCriticalSpeedAnalysis)

    @property
    def coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "CouplingCompoundCriticalSpeedAnalysis":
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
class CouplingCompoundCriticalSpeedAnalysis(
    _6923.SpecialisedAssemblyCompoundCriticalSpeedAnalysis
):
    """CouplingCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6727.CouplingCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.CouplingCriticalSpeedAnalysis]

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6727.CouplingCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.CouplingCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundCriticalSpeedAnalysis
        """
        return _Cast_CouplingCompoundCriticalSpeedAnalysis(self)
