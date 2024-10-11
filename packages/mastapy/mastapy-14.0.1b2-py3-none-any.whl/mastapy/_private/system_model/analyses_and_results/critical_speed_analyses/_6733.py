"""CVTCriticalSpeedAnalysis"""

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
    _6699,
)

_CVT_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CVTCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6689,
        _6773,
        _6792,
    )
    from mastapy._private.system_model.part_model.couplings import _2647

    Self = TypeVar("Self", bound="CVTCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTCriticalSpeedAnalysis._Cast_CVTCriticalSpeedAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTCriticalSpeedAnalysis:
    """Special nested class for casting CVTCriticalSpeedAnalysis to subclasses."""

    __parent__: "CVTCriticalSpeedAnalysis"

    @property
    def belt_drive_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6699.BeltDriveCriticalSpeedAnalysis":
        return self.__parent__._cast(_6699.BeltDriveCriticalSpeedAnalysis)

    @property
    def specialised_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6792.SpecialisedAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6792,
        )

        return self.__parent__._cast(_6792.SpecialisedAssemblyCriticalSpeedAnalysis)

    @property
    def abstract_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6689.AbstractAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6689,
        )

        return self.__parent__._cast(_6689.AbstractAssemblyCriticalSpeedAnalysis)

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
    def cvt_critical_speed_analysis(self: "CastSelf") -> "CVTCriticalSpeedAnalysis":
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
class CVTCriticalSpeedAnalysis(_6699.BeltDriveCriticalSpeedAnalysis):
    """CVTCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2647.CVT":
        """mastapy.system_model.part_model.couplings.CVT

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTCriticalSpeedAnalysis
        """
        return _Cast_CVTCriticalSpeedAnalysis(self)
