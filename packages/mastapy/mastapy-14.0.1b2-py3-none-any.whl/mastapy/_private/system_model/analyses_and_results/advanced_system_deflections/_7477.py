"""CylindricalGearAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7489,
)

_CYLINDRICAL_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CylindricalGearAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _473
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7454,
        _7478,
        _7480,
        _7481,
        _7511,
        _7513,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7012
    from mastapy._private.system_model.part_model.gears import _2584

    Self = TypeVar("Self", bound="CylindricalGearAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearAdvancedSystemDeflection._Cast_CylindricalGearAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearAdvancedSystemDeflection:
    """Special nested class for casting CylindricalGearAdvancedSystemDeflection to subclasses."""

    __parent__: "CylindricalGearAdvancedSystemDeflection"

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7489.GearAdvancedSystemDeflection":
        return self.__parent__._cast(_7489.GearAdvancedSystemDeflection)

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7511.MountableComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7511,
        )

        return self.__parent__._cast(_7511.MountableComponentAdvancedSystemDeflection)

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7454.ComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7454,
        )

        return self.__parent__._cast(_7454.ComponentAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7513.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7513,
        )

        return self.__parent__._cast(_7513.PartAdvancedSystemDeflection)

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
    def cylindrical_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7481.CylindricalPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7481,
        )

        return self.__parent__._cast(
            _7481.CylindricalPlanetGearAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CylindricalGearAdvancedSystemDeflection":
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
class CylindricalGearAdvancedSystemDeflection(_7489.GearAdvancedSystemDeflection):
    """CylindricalGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def maximum_principal_root_stress_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPrincipalRootStressCompression"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_principal_root_stress_tension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPrincipalRootStressTension")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_von_mises_root_stress_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumVonMisesRootStressCompression"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_von_mises_root_stress_tension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumVonMisesRootStressTension")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2584.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_473.CylindricalGearRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7012.CylindricalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cylindrical_gear_advanced_system_deflection_meshes(
        self: "Self",
    ) -> "List[_7478.CylindricalGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearAdvancedSystemDeflectionMeshes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gear_advanced_system_deflections_in_meshes(
        self: "Self",
    ) -> "List[_7480.CylindricalMeshedGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalMeshedGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearAdvancedSystemDeflectionsInMeshes"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_meshed_gear_advanced_system_deflections(
        self: "Self",
    ) -> "List[_7480.CylindricalMeshedGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalMeshedGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalMeshedGearAdvancedSystemDeflections"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planetaries(self: "Self") -> "List[CylindricalGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearAdvancedSystemDeflection
        """
        return _Cast_CylindricalGearAdvancedSystemDeflection(self)
