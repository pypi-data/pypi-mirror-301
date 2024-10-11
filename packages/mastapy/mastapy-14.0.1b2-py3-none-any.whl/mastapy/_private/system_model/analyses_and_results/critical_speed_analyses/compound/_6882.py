"""GearMeshCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6888,
)

_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "GearMeshCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6751,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6828,
        _6835,
        _6840,
        _6853,
        _6856,
        _6858,
        _6871,
        _6877,
        _6886,
        _6890,
        _6893,
        _6896,
        _6925,
        _6931,
        _6934,
        _6949,
        _6952,
    )

    Self = TypeVar("Self", bound="GearMeshCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshCompoundCriticalSpeedAnalysis._Cast_GearMeshCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshCompoundCriticalSpeedAnalysis:
    """Special nested class for casting GearMeshCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "GearMeshCompoundCriticalSpeedAnalysis"

    @property
    def inter_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6888.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6888.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6858.ConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6858,
        )

        return self.__parent__._cast(_6858.ConnectionCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6828.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6828,
        )

        return self.__parent__._cast(
            _6828.AGMAGleasonConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6835.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6835,
        )

        return self.__parent__._cast(
            _6835.BevelDifferentialGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6840.BevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6840,
        )

        return self.__parent__._cast(_6840.BevelGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def concept_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6853.ConceptGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6853,
        )

        return self.__parent__._cast(_6853.ConceptGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6856.ConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6856,
        )

        return self.__parent__._cast(_6856.ConicalGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6871.CylindricalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6871,
        )

        return self.__parent__._cast(
            _6871.CylindricalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6877.FaceGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6877,
        )

        return self.__parent__._cast(_6877.FaceGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6886.HypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6886,
        )

        return self.__parent__._cast(_6886.HypoidGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6890.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6890,
        )

        return self.__parent__._cast(
            _6890.KlingelnbergCycloPalloidConicalGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6893.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6893,
        )

        return self.__parent__._cast(
            _6893.KlingelnbergCycloPalloidHypoidGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6896.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6896,
        )

        return self.__parent__._cast(
            _6896.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6925.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6925,
        )

        return self.__parent__._cast(
            _6925.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6931.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6931,
        )

        return self.__parent__._cast(
            _6931.StraightBevelDiffGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6934.StraightBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6934,
        )

        return self.__parent__._cast(
            _6934.StraightBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6949.WormGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6949,
        )

        return self.__parent__._cast(_6949.WormGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6952.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6952,
        )

        return self.__parent__._cast(
            _6952.ZerolBevelGearMeshCompoundCriticalSpeedAnalysis
        )

    @property
    def gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "GearMeshCompoundCriticalSpeedAnalysis":
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
class GearMeshCompoundCriticalSpeedAnalysis(
    _6888.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
):
    """GearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6751.GearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GearMeshCriticalSpeedAnalysis]

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
    ) -> "List[_6751.GearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.GearMeshCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearMeshCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshCompoundCriticalSpeedAnalysis
        """
        return _Cast_GearMeshCompoundCriticalSpeedAnalysis(self)
