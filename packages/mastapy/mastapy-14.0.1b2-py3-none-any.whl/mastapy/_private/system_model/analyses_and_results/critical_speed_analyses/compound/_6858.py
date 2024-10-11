"""ConnectionCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7711

_CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "ConnectionCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6724,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6826,
        _6828,
        _6832,
        _6835,
        _6840,
        _6845,
        _6847,
        _6850,
        _6853,
        _6856,
        _6861,
        _6863,
        _6867,
        _6869,
        _6871,
        _6877,
        _6882,
        _6886,
        _6888,
        _6890,
        _6893,
        _6896,
        _6906,
        _6908,
        _6915,
        _6918,
        _6922,
        _6925,
        _6928,
        _6931,
        _6934,
        _6943,
        _6949,
        _6952,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundCriticalSpeedAnalysis._Cast_ConnectionCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundCriticalSpeedAnalysis:
    """Special nested class for casting ConnectionCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "ConnectionCompoundCriticalSpeedAnalysis"

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6826.AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6826,
        )

        return self.__parent__._cast(
            _6826.AbstractShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

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
    def belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6832.BeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6832,
        )

        return self.__parent__._cast(_6832.BeltConnectionCompoundCriticalSpeedAnalysis)

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
    def clutch_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6845.ClutchConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6845,
        )

        return self.__parent__._cast(
            _6845.ClutchConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def coaxial_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6847.CoaxialConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6847,
        )

        return self.__parent__._cast(
            _6847.CoaxialConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def concept_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6850.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6850,
        )

        return self.__parent__._cast(
            _6850.ConceptCouplingConnectionCompoundCriticalSpeedAnalysis
        )

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
    def coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6861.CouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6861,
        )

        return self.__parent__._cast(
            _6861.CouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cvt_belt_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6863.CVTBeltConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6863,
        )

        return self.__parent__._cast(
            _6863.CVTBeltConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6867.CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6867,
        )

        return self.__parent__._cast(
            _6867.CycloidalDiscCentralBearingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6869.CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6869,
        )

        return self.__parent__._cast(
            _6869.CycloidalDiscPlanetaryBearingConnectionCompoundCriticalSpeedAnalysis
        )

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
    def gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6882.GearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6882,
        )

        return self.__parent__._cast(_6882.GearMeshCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6886.HypoidGearMeshCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6886,
        )

        return self.__parent__._cast(_6886.HypoidGearMeshCompoundCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6888.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6888,
        )

        return self.__parent__._cast(
            _6888.InterMountableComponentConnectionCompoundCriticalSpeedAnalysis
        )

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
    def part_to_part_shear_coupling_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6906.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6906,
        )

        return self.__parent__._cast(
            _6906.PartToPartShearCouplingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def planetary_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6908.PlanetaryConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6908,
        )

        return self.__parent__._cast(
            _6908.PlanetaryConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6915.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6915,
        )

        return self.__parent__._cast(
            _6915.RingPinsToDiscConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6918.RollingRingConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6918,
        )

        return self.__parent__._cast(
            _6918.RollingRingConnectionCompoundCriticalSpeedAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6922.ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6922,
        )

        return self.__parent__._cast(
            _6922.ShaftToMountableComponentConnectionCompoundCriticalSpeedAnalysis
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
    def spring_damper_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6928.SpringDamperConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6928,
        )

        return self.__parent__._cast(
            _6928.SpringDamperConnectionCompoundCriticalSpeedAnalysis
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
    def torque_converter_connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6943.TorqueConverterConnectionCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6943,
        )

        return self.__parent__._cast(
            _6943.TorqueConverterConnectionCompoundCriticalSpeedAnalysis
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
    def connection_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "ConnectionCompoundCriticalSpeedAnalysis":
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
class ConnectionCompoundCriticalSpeedAnalysis(_7711.ConnectionCompoundAnalysis):
    """ConnectionCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6724.ConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConnectionCriticalSpeedAnalysis]

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
    ) -> "List[_6724.ConnectionCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.ConnectionCriticalSpeedAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundCriticalSpeedAnalysis
        """
        return _Cast_ConnectionCompoundCriticalSpeedAnalysis(self)
