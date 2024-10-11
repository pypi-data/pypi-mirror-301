"""BevelDifferentialPlanetGearHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5824

_BEVEL_DIFFERENTIAL_PLANET_GEAR_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "BevelDifferentialPlanetGearHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5817,
        _5829,
        _5839,
        _5846,
        _5887,
        _5922,
        _5924,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2791,
    )
    from mastapy._private.system_model.part_model.gears import _2576

    Self = TypeVar("Self", bound="BevelDifferentialPlanetGearHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGearHarmonicAnalysis._Cast_BevelDifferentialPlanetGearHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGearHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGearHarmonicAnalysis:
    """Special nested class for casting BevelDifferentialPlanetGearHarmonicAnalysis to subclasses."""

    __parent__: "BevelDifferentialPlanetGearHarmonicAnalysis"

    @property
    def bevel_differential_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5824.BevelDifferentialGearHarmonicAnalysis":
        return self.__parent__._cast(_5824.BevelDifferentialGearHarmonicAnalysis)

    @property
    def bevel_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5829.BevelGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5829,
        )

        return self.__parent__._cast(_5829.BevelGearHarmonicAnalysis)

    @property
    def agma_gleason_conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5817.AGMAGleasonConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5817,
        )

        return self.__parent__._cast(_5817.AGMAGleasonConicalGearHarmonicAnalysis)

    @property
    def conical_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5846.ConicalGearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5846,
        )

        return self.__parent__._cast(_5846.ConicalGearHarmonicAnalysis)

    @property
    def gear_harmonic_analysis(self: "CastSelf") -> "_5887.GearHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5887,
        )

        return self.__parent__._cast(_5887.GearHarmonicAnalysis)

    @property
    def mountable_component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5922.MountableComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5922,
        )

        return self.__parent__._cast(_5922.MountableComponentHarmonicAnalysis)

    @property
    def component_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5839.ComponentHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5839,
        )

        return self.__parent__._cast(_5839.ComponentHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5924.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5924,
        )

        return self.__parent__._cast(_5924.PartHarmonicAnalysis)

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
    def bevel_differential_planet_gear_harmonic_analysis(
        self: "CastSelf",
    ) -> "BevelDifferentialPlanetGearHarmonicAnalysis":
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
class BevelDifferentialPlanetGearHarmonicAnalysis(
    _5824.BevelDifferentialGearHarmonicAnalysis
):
    """BevelDifferentialPlanetGearHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_PLANET_GEAR_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2576.BevelDifferentialPlanetGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2791.BevelDifferentialPlanetGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialPlanetGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialPlanetGearHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGearHarmonicAnalysis
        """
        return _Cast_BevelDifferentialPlanetGearHarmonicAnalysis(self)
