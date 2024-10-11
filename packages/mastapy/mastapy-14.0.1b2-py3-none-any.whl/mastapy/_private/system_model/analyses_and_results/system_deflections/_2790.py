"""BevelDifferentialGearSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2795

_BEVEL_DIFFERENTIAL_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "BevelDifferentialGearSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.bevel import _568
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4151
    from mastapy._private.system_model.analyses_and_results.static_loads import _6973
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2778,
        _2791,
        _2792,
        _2802,
        _2813,
        _2848,
        _2871,
        _2874,
    )
    from mastapy._private.system_model.part_model.gears import _2574

    Self = TypeVar("Self", bound="BevelDifferentialGearSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearSystemDeflection._Cast_BevelDifferentialGearSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearSystemDeflection:
    """Special nested class for casting BevelDifferentialGearSystemDeflection to subclasses."""

    __parent__: "BevelDifferentialGearSystemDeflection"

    @property
    def bevel_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2795.BevelGearSystemDeflection":
        return self.__parent__._cast(_2795.BevelGearSystemDeflection)

    @property
    def agma_gleason_conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2778.AGMAGleasonConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2778,
        )

        return self.__parent__._cast(_2778.AGMAGleasonConicalGearSystemDeflection)

    @property
    def conical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2813.ConicalGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2813,
        )

        return self.__parent__._cast(_2813.ConicalGearSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_2848.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2848,
        )

        return self.__parent__._cast(_2848.GearSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2871.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2871,
        )

        return self.__parent__._cast(_2871.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2802.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2802,
        )

        return self.__parent__._cast(_2802.ComponentSystemDeflection)

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
    def bevel_differential_planet_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2791.BevelDifferentialPlanetGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2791,
        )

        return self.__parent__._cast(_2791.BevelDifferentialPlanetGearSystemDeflection)

    @property
    def bevel_differential_sun_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2792.BevelDifferentialSunGearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2792,
        )

        return self.__parent__._cast(_2792.BevelDifferentialSunGearSystemDeflection)

    @property
    def bevel_differential_gear_system_deflection(
        self: "CastSelf",
    ) -> "BevelDifferentialGearSystemDeflection":
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
class BevelDifferentialGearSystemDeflection(_2795.BevelGearSystemDeflection):
    """BevelDifferentialGearSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_SYSTEM_DEFLECTION

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
    def power_flow_results(self: "Self") -> "_4151.BevelDifferentialGearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearSystemDeflection
        """
        return _Cast_BevelDifferentialGearSystemDeflection(self)
