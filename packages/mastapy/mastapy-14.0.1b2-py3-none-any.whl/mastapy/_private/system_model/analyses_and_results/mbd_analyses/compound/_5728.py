"""KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5694,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
        "KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5578
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5696,
        _5720,
        _5726,
        _5731,
        _5734,
    )

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis._Cast_KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: (
        "KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"
    )

    @property
    def conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5694.ConicalGearMeshCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5694.ConicalGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5720.GearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5720,
        )

        return self.__parent__._cast(_5720.GearMeshCompoundMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5726.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5726,
        )

        return self.__parent__._cast(
            _5726.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5731.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5731,
        )

        return self.__parent__._cast(
            _5731.KlingelnbergCycloPalloidHypoidGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5734.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5734,
        )

        return self.__parent__._cast(
            _5734.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis":
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
class KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis(
    _5694.ConicalGearMeshCompoundMultibodyDynamicsAnalysis
):
    """KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5578.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis]

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
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5578.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.KlingelnbergCycloPalloidConicalGearMeshMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> (
        "_Cast_KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis"
    ):
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshCompoundMultibodyDynamicsAnalysis(
            self
        )
