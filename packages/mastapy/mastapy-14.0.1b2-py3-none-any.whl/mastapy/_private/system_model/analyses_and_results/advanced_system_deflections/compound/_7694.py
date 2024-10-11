"""ZerolBevelGearSetCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7582,
)

_ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ZerolBevelGearSetCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7563,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7564,
        _7570,
        _7598,
        _7624,
        _7645,
        _7664,
        _7692,
        _7693,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.part_model.gears import _2613

    Self = TypeVar("Self", bound="ZerolBevelGearSetCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearSetCompoundAdvancedSystemDeflection._Cast_ZerolBevelGearSetCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSetCompoundAdvancedSystemDeflection:
    """Special nested class for casting ZerolBevelGearSetCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "ZerolBevelGearSetCompoundAdvancedSystemDeflection"

    @property
    def bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7582.BevelGearSetCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7582.BevelGearSetCompoundAdvancedSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7570.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7570,
        )

        return self.__parent__._cast(
            _7570.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(
            _7598.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7624.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7624,
        )

        return self.__parent__._cast(_7624.GearSetCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7664.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7664,
        )

        return self.__parent__._cast(
            _7664.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7564.AbstractAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7564,
        )

        return self.__parent__._cast(
            _7564.AbstractAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7645,
        )

        return self.__parent__._cast(_7645.PartCompoundAdvancedSystemDeflection)

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
    def zerol_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ZerolBevelGearSetCompoundAdvancedSystemDeflection":
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
class ZerolBevelGearSetCompoundAdvancedSystemDeflection(
    _7582.BevelGearSetCompoundAdvancedSystemDeflection
):
    """ZerolBevelGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2613.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2613.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

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
    ) -> "List[_7563.ZerolBevelGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection]

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
    def zerol_bevel_gears_compound_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7692.ZerolBevelGearCompoundAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearCompoundAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelGearsCompoundAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes_compound_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7693.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelMeshesCompoundAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7563.ZerolBevelGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ZerolBevelGearSetCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSetCompoundAdvancedSystemDeflection
        """
        return _Cast_ZerolBevelGearSetCompoundAdvancedSystemDeflection(self)
