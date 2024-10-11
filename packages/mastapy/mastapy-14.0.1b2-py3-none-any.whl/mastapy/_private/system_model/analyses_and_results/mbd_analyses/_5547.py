"""CVTBeltConnectionMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5515

_CVT_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "CVTBeltConnectionMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7714,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5542,
        _5577,
    )
    from mastapy._private.system_model.connections_and_sockets import _2328

    Self = TypeVar("Self", bound="CVTBeltConnectionMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTBeltConnectionMultibodyDynamicsAnalysis._Cast_CVTBeltConnectionMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTBeltConnectionMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTBeltConnectionMultibodyDynamicsAnalysis:
    """Special nested class for casting CVTBeltConnectionMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CVTBeltConnectionMultibodyDynamicsAnalysis"

    @property
    def belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5515.BeltConnectionMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5515.BeltConnectionMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5577.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5577,
        )

        return self.__parent__._cast(
            _5577.InterMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5542.ConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5542,
        )

        return self.__parent__._cast(_5542.ConnectionMultibodyDynamicsAnalysis)

    @property
    def connection_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7714.ConnectionTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.ConnectionTimeSeriesLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7710.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2736.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.ConnectionAnalysis)

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
    def cvt_belt_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CVTBeltConnectionMultibodyDynamicsAnalysis":
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
class CVTBeltConnectionMultibodyDynamicsAnalysis(
    _5515.BeltConnectionMultibodyDynamicsAnalysis
):
    """CVTBeltConnectionMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_BELT_CONNECTION_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2328.CVTBeltConnection":
        """mastapy.system_model.connections_and_sockets.CVTBeltConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTBeltConnectionMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTBeltConnectionMultibodyDynamicsAnalysis
        """
        return _Cast_CVTBeltConnectionMultibodyDynamicsAnalysis(self)
