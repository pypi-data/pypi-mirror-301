"""CylindricalGearSetSystemDeflectionWithLTCAResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2829

_CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CylindricalGearSetSystemDeflectionWithLTCAResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca.cylindrical import _885
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
        _2847,
        _2874,
        _2895,
    )

    Self = TypeVar("Self", bound="CylindricalGearSetSystemDeflectionWithLTCAResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetSystemDeflectionWithLTCAResults._Cast_CylindricalGearSetSystemDeflectionWithLTCAResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetSystemDeflectionWithLTCAResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetSystemDeflectionWithLTCAResults:
    """Special nested class for casting CylindricalGearSetSystemDeflectionWithLTCAResults to subclasses."""

    __parent__: "CylindricalGearSetSystemDeflectionWithLTCAResults"

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2829.CylindricalGearSetSystemDeflection":
        return self.__parent__._cast(_2829.CylindricalGearSetSystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "_2847.GearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2847,
        )

        return self.__parent__._cast(_2847.GearSetSystemDeflection)

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2895.SpecialisedAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2895,
        )

        return self.__parent__._cast(_2895.SpecialisedAssemblySystemDeflection)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2772.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2772,
        )

        return self.__parent__._cast(_2772.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

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
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "CylindricalGearSetSystemDeflectionWithLTCAResults":
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
class CylindricalGearSetSystemDeflectionWithLTCAResults(
    _2829.CylindricalGearSetSystemDeflection
):
    """CylindricalGearSetSystemDeflectionWithLTCAResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_SYSTEM_DEFLECTION_WITH_LTCA_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def advanced_ltca_results(
        self: "Self",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdvancedLTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def advanced_ltca_results_only_first_planetary_mesh(
        self: "Self",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AdvancedLTCAResultsOnlyFirstPlanetaryMesh"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def basic_ltca_results(
        self: "Self",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicLTCAResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def basic_ltca_results_only_first_planetary_mesh(
        self: "Self",
    ) -> "_885.CylindricalGearSetLoadDistributionAnalysis":
        """mastapy.gears.ltca.cylindrical.CylindricalGearSetLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicLTCAResultsOnlyFirstPlanetaryMesh"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearSetSystemDeflectionWithLTCAResults":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetSystemDeflectionWithLTCAResults
        """
        return _Cast_CylindricalGearSetSystemDeflectionWithLTCAResults(self)
