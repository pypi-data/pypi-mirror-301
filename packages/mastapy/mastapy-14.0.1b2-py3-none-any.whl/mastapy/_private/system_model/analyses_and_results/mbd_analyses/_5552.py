"""CycloidalDiscMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5504

_CYCLOIDAL_DISC_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "CycloidalDiscMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7721,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5505,
        _5532,
        _5597,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7010
    from mastapy._private.system_model.part_model.cycloidal import _2628

    Self = TypeVar("Self", bound="CycloidalDiscMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscMultibodyDynamicsAnalysis._Cast_CycloidalDiscMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscMultibodyDynamicsAnalysis:
    """Special nested class for casting CycloidalDiscMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CycloidalDiscMultibodyDynamicsAnalysis"

    @property
    def abstract_shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5504.AbstractShaftMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5504.AbstractShaftMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_or_housing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5505.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5505,
        )

        return self.__parent__._cast(
            _5505.AbstractShaftOrHousingMultibodyDynamicsAnalysis
        )

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(_5597.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7721.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartTimeSeriesLoadAnalysisCase)

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
    def cycloidal_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CycloidalDiscMultibodyDynamicsAnalysis":
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
class CycloidalDiscMultibodyDynamicsAnalysis(
    _5504.AbstractShaftMultibodyDynamicsAnalysis
):
    """CycloidalDiscMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2628.CycloidalDisc":
        """mastapy.system_model.part_model.cycloidal.CycloidalDisc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7010.CycloidalDiscLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscMultibodyDynamicsAnalysis
        """
        return _Cast_CycloidalDiscMultibodyDynamicsAnalysis(self)
