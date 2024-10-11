"""BevelDifferentialGearAdvancedSystemDeflection"""

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
    _7445,
)

_BEVEL_DIFFERENTIAL_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "BevelDifferentialGearAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.bevel import _568
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7433,
        _7443,
        _7444,
        _7454,
        _7461,
        _7489,
        _7511,
        _7513,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6973
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2790,
    )
    from mastapy._private.system_model.part_model.gears import _2574

    Self = TypeVar("Self", bound="BevelDifferentialGearAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearAdvancedSystemDeflection._Cast_BevelDifferentialGearAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearAdvancedSystemDeflection:
    """Special nested class for casting BevelDifferentialGearAdvancedSystemDeflection to subclasses."""

    __parent__: "BevelDifferentialGearAdvancedSystemDeflection"

    @property
    def bevel_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7445.BevelGearAdvancedSystemDeflection":
        return self.__parent__._cast(_7445.BevelGearAdvancedSystemDeflection)

    @property
    def agma_gleason_conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7433.AGMAGleasonConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7433,
        )

        return self.__parent__._cast(
            _7433.AGMAGleasonConicalGearAdvancedSystemDeflection
        )

    @property
    def conical_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7461.ConicalGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7461,
        )

        return self.__parent__._cast(_7461.ConicalGearAdvancedSystemDeflection)

    @property
    def gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7489.GearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7489,
        )

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
    def bevel_differential_planet_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7443.BevelDifferentialPlanetGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7443,
        )

        return self.__parent__._cast(
            _7443.BevelDifferentialPlanetGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7444.BevelDifferentialSunGearAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7444,
        )

        return self.__parent__._cast(
            _7444.BevelDifferentialSunGearAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_advanced_system_deflection(
        self: "CastSelf",
    ) -> "BevelDifferentialGearAdvancedSystemDeflection":
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
class BevelDifferentialGearAdvancedSystemDeflection(
    _7445.BevelGearAdvancedSystemDeflection
):
    """BevelDifferentialGearAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2574.BevelDifferentialGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_568.BevelGearRating":
        """mastapy.gears.rating.bevel.BevelGearRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_6973.BevelDifferentialGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_system_deflection_results(
        self: "Self",
    ) -> "List[_2790.BevelDifferentialGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearAdvancedSystemDeflection
        """
        return _Cast_BevelDifferentialGearAdvancedSystemDeflection(self)
