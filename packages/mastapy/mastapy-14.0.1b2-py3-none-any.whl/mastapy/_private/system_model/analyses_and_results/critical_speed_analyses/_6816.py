"""VirtualComponentCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6771,
)

_VIRTUAL_COMPONENT_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "VirtualComponentCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6714,
        _6767,
        _6768,
        _6773,
        _6780,
        _6781,
        _6815,
    )
    from mastapy._private.system_model.part_model import _2538

    Self = TypeVar("Self", bound="VirtualComponentCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCriticalSpeedAnalysis._Cast_VirtualComponentCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCriticalSpeedAnalysis:
    """Special nested class for casting VirtualComponentCriticalSpeedAnalysis to subclasses."""

    __parent__: "VirtualComponentCriticalSpeedAnalysis"

    @property
    def mountable_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6771.MountableComponentCriticalSpeedAnalysis":
        return self.__parent__._cast(_6771.MountableComponentCriticalSpeedAnalysis)

    @property
    def component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6714.ComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6714,
        )

        return self.__parent__._cast(_6714.ComponentCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6773.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6773,
        )

        return self.__parent__._cast(_6773.PartCriticalSpeedAnalysis)

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
    def mass_disc_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6767.MassDiscCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6767,
        )

        return self.__parent__._cast(_6767.MassDiscCriticalSpeedAnalysis)

    @property
    def measurement_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6768.MeasurementComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6768,
        )

        return self.__parent__._cast(_6768.MeasurementComponentCriticalSpeedAnalysis)

    @property
    def point_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6780.PointLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6780,
        )

        return self.__parent__._cast(_6780.PointLoadCriticalSpeedAnalysis)

    @property
    def power_load_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6781.PowerLoadCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6781,
        )

        return self.__parent__._cast(_6781.PowerLoadCriticalSpeedAnalysis)

    @property
    def unbalanced_mass_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6815.UnbalancedMassCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6815,
        )

        return self.__parent__._cast(_6815.UnbalancedMassCriticalSpeedAnalysis)

    @property
    def virtual_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentCriticalSpeedAnalysis":
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
class VirtualComponentCriticalSpeedAnalysis(
    _6771.MountableComponentCriticalSpeedAnalysis
):
    """VirtualComponentCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2538.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCriticalSpeedAnalysis
        """
        return _Cast_VirtualComponentCriticalSpeedAnalysis(self)
