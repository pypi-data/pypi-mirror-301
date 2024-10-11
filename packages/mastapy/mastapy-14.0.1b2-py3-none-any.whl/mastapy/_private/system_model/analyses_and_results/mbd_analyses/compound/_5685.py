"""CoaxialConnectionCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5760,
)

_COAXIAL_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CoaxialConnectionCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5531
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5664,
        _5696,
        _5705,
    )
    from mastapy._private.system_model.connections_and_sockets import _2324

    Self = TypeVar("Self", bound="CoaxialConnectionCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoaxialConnectionCompoundMultibodyDynamicsAnalysis._Cast_CoaxialConnectionCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnectionCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting CoaxialConnectionCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CoaxialConnectionCompoundMultibodyDynamicsAnalysis"

    @property
    def shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5760.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5760.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5664.AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5664,
        )

        return self.__parent__._cast(
            _5664.AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5696.ConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5696,
        )

        return self.__parent__._cast(_5696.ConnectionCompoundMultibodyDynamicsAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def cycloidal_disc_central_bearing_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5705.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5705,
        )

        return self.__parent__._cast(
            _5705.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def coaxial_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CoaxialConnectionCompoundMultibodyDynamicsAnalysis":
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
class CoaxialConnectionCompoundMultibodyDynamicsAnalysis(
    _5760.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
):
    """CoaxialConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2324.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2324.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5531.CoaxialConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CoaxialConnectionMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5531.CoaxialConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CoaxialConnectionMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CoaxialConnectionCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnectionCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_CoaxialConnectionCompoundMultibodyDynamicsAnalysis(self)
