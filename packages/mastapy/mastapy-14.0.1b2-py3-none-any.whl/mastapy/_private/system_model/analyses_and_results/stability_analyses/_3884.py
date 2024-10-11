"""BevelGearStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3872

_BEVEL_GEAR_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "BevelGearStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3879,
        _3880,
        _3881,
        _3891,
        _3900,
        _3928,
        _3947,
        _3949,
        _3971,
        _3980,
        _3983,
        _3984,
        _3985,
        _4001,
    )
    from mastapy._private.system_model.part_model.gears import _2578

    Self = TypeVar("Self", bound="BevelGearStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelGearStabilityAnalysis._Cast_BevelGearStabilityAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearStabilityAnalysis:
    """Special nested class for casting BevelGearStabilityAnalysis to subclasses."""

    __parent__: "BevelGearStabilityAnalysis"

    @property
    def agma_gleason_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3872.AGMAGleasonConicalGearStabilityAnalysis":
        return self.__parent__._cast(_3872.AGMAGleasonConicalGearStabilityAnalysis)

    @property
    def conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3900.ConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3900,
        )

        return self.__parent__._cast(_3900.ConicalGearStabilityAnalysis)

    @property
    def gear_stability_analysis(self: "CastSelf") -> "_3928.GearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3928,
        )

        return self.__parent__._cast(_3928.GearStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3947.MountableComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3947,
        )

        return self.__parent__._cast(_3947.MountableComponentStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_3891.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3891,
        )

        return self.__parent__._cast(_3891.ComponentStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_3949.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3949,
        )

        return self.__parent__._cast(_3949.PartStabilityAnalysis)

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
    def bevel_differential_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3879.BevelDifferentialGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3879,
        )

        return self.__parent__._cast(_3879.BevelDifferentialGearStabilityAnalysis)

    @property
    def bevel_differential_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3880.BevelDifferentialPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3880,
        )

        return self.__parent__._cast(_3880.BevelDifferentialPlanetGearStabilityAnalysis)

    @property
    def bevel_differential_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3881.BevelDifferentialSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3881,
        )

        return self.__parent__._cast(_3881.BevelDifferentialSunGearStabilityAnalysis)

    @property
    def spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3971.SpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3971,
        )

        return self.__parent__._cast(_3971.SpiralBevelGearStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3980.StraightBevelDiffGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3980,
        )

        return self.__parent__._cast(_3980.StraightBevelDiffGearStabilityAnalysis)

    @property
    def straight_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3983.StraightBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3983,
        )

        return self.__parent__._cast(_3983.StraightBevelGearStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3984.StraightBevelPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3984,
        )

        return self.__parent__._cast(_3984.StraightBevelPlanetGearStabilityAnalysis)

    @property
    def straight_bevel_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3985.StraightBevelSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3985,
        )

        return self.__parent__._cast(_3985.StraightBevelSunGearStabilityAnalysis)

    @property
    def zerol_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_4001.ZerolBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4001,
        )

        return self.__parent__._cast(_4001.ZerolBevelGearStabilityAnalysis)

    @property
    def bevel_gear_stability_analysis(self: "CastSelf") -> "BevelGearStabilityAnalysis":
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
class BevelGearStabilityAnalysis(_3872.AGMAGleasonConicalGearStabilityAnalysis):
    """BevelGearStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2578.BevelGear":
        """mastapy.system_model.part_model.gears.BevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearStabilityAnalysis
        """
        return _Cast_BevelGearStabilityAnalysis(self)
