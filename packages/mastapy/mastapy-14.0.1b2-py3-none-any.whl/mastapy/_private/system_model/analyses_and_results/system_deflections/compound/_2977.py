"""CouplingCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3042,
)

_COUPLING_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "CouplingCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2818,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2940,
        _2961,
        _2966,
        _3022,
        _3023,
        _3046,
        _3061,
    )

    Self = TypeVar("Self", bound="CouplingCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingCompoundSystemDeflection._Cast_CouplingCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundSystemDeflection:
    """Special nested class for casting CouplingCompoundSystemDeflection to subclasses."""

    __parent__: "CouplingCompoundSystemDeflection"

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3042.SpecialisedAssemblyCompoundSystemDeflection":
        return self.__parent__._cast(_3042.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2940.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2940,
        )

        return self.__parent__._cast(_2940.AbstractAssemblyCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3022.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3022,
        )

        return self.__parent__._cast(_3022.PartCompoundSystemDeflection)

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
    def clutch_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2961.ClutchCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2961,
        )

        return self.__parent__._cast(_2961.ClutchCompoundSystemDeflection)

    @property
    def concept_coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2966.ConceptCouplingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2966,
        )

        return self.__parent__._cast(_2966.ConceptCouplingCompoundSystemDeflection)

    @property
    def part_to_part_shear_coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3023.PartToPartShearCouplingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3023,
        )

        return self.__parent__._cast(
            _3023.PartToPartShearCouplingCompoundSystemDeflection
        )

    @property
    def spring_damper_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3046.SpringDamperCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3046,
        )

        return self.__parent__._cast(_3046.SpringDamperCompoundSystemDeflection)

    @property
    def torque_converter_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3061.TorqueConverterCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3061,
        )

        return self.__parent__._cast(_3061.TorqueConverterCompoundSystemDeflection)

    @property
    def coupling_compound_system_deflection(
        self: "CastSelf",
    ) -> "CouplingCompoundSystemDeflection":
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
class CouplingCompoundSystemDeflection(
    _3042.SpecialisedAssemblyCompoundSystemDeflection
):
    """CouplingCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_2818.CouplingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingSystemDeflection]

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
    ) -> "List[_2818.CouplingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundSystemDeflection
        """
        return _Cast_CouplingCompoundSystemDeflection(self)
