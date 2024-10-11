"""CouplingCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4945,
)

_COUPLING_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "CouplingCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4727
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4845,
        _4866,
        _4871,
        _4926,
        _4927,
        _4949,
        _4964,
    )

    Self = TypeVar("Self", bound="CouplingCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundModalAnalysis._Cast_CouplingCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundModalAnalysis:
    """Special nested class for casting CouplingCompoundModalAnalysis to subclasses."""

    __parent__: "CouplingCompoundModalAnalysis"

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4945.SpecialisedAssemblyCompoundModalAnalysis":
        return self.__parent__._cast(_4945.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4845.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4845,
        )

        return self.__parent__._cast(_4845.AbstractAssemblyCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.PartCompoundModalAnalysis)

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
    def clutch_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4866.ClutchCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4866,
        )

        return self.__parent__._cast(_4866.ClutchCompoundModalAnalysis)

    @property
    def concept_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4871.ConceptCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4871,
        )

        return self.__parent__._cast(_4871.ConceptCouplingCompoundModalAnalysis)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4927.PartToPartShearCouplingCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4927,
        )

        return self.__parent__._cast(_4927.PartToPartShearCouplingCompoundModalAnalysis)

    @property
    def spring_damper_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4949.SpringDamperCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4949,
        )

        return self.__parent__._cast(_4949.SpringDamperCompoundModalAnalysis)

    @property
    def torque_converter_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4964.TorqueConverterCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4964,
        )

        return self.__parent__._cast(_4964.TorqueConverterCompoundModalAnalysis)

    @property
    def coupling_compound_modal_analysis(
        self: "CastSelf",
    ) -> "CouplingCompoundModalAnalysis":
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
class CouplingCompoundModalAnalysis(_4945.SpecialisedAssemblyCompoundModalAnalysis):
    """CouplingCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4727.CouplingModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis]

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
    ) -> "List[_4727.CouplingModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CouplingModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundModalAnalysis
        """
        return _Cast_CouplingCompoundModalAnalysis(self)
