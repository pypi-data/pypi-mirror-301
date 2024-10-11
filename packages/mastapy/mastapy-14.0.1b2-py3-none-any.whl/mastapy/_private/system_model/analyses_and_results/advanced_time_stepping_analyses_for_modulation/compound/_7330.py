"""ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"""

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

_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7198,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7298,
        _7300,
        _7304,
        _7307,
        _7312,
        _7317,
        _7319,
        _7322,
        _7325,
        _7328,
        _7333,
        _7335,
        _7339,
        _7341,
        _7343,
        _7349,
        _7354,
        _7358,
        _7360,
        _7362,
        _7365,
        _7368,
        _7378,
        _7380,
        _7387,
        _7390,
        _7394,
        _7397,
        _7400,
        _7403,
        _7406,
        _7415,
        _7421,
        _7424,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

    Self = TypeVar(
        "Self", bound="ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"

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
    def abstract_shaft_to_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7298.AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7298,
        )

        return self.__parent__._cast(
            _7298.AbstractShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7300.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7300,
        )

        return self.__parent__._cast(
            _7300.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def belt_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7304.BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7304,
        )

        return self.__parent__._cast(
            _7304.BeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7307.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7307,
        )

        return self.__parent__._cast(
            _7307.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7312.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7312,
        )

        return self.__parent__._cast(
            _7312.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7317.ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7317,
        )

        return self.__parent__._cast(
            _7317.ClutchConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coaxial_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7319.CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7319,
        )

        return self.__parent__._cast(
            _7319.CoaxialConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7322.ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7322,
        )

        return self.__parent__._cast(
            _7322.ConceptCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7325.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7325,
        )

        return self.__parent__._cast(
            _7325.ConceptGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7328.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7328,
        )

        return self.__parent__._cast(
            _7328.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7333.CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7333,
        )

        return self.__parent__._cast(
            _7333.CouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_belt_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7335.CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7335,
        )

        return self.__parent__._cast(
            _7335.CVTBeltConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7339.CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7339,
        )

        return self.__parent__._cast(
            _7339.CycloidalDiscCentralBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7341.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7341,
        )

        return self.__parent__._cast(
            _7341.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7343.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7343,
        )

        return self.__parent__._cast(
            _7343.CylindricalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7349.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7349,
        )

        return self.__parent__._cast(
            _7349.FaceGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7354.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7354,
        )

        return self.__parent__._cast(
            _7354.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7358.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7358,
        )

        return self.__parent__._cast(
            _7358.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7360.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7360,
        )

        return self.__parent__._cast(
            _7360.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7362.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7362,
        )

        return self.__parent__._cast(
            _7362.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7365.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7365,
        )

        return self.__parent__._cast(
            _7365.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7368.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7368,
        )

        return self.__parent__._cast(
            _7368.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7378.PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7378,
        )

        return self.__parent__._cast(
            _7378.PartToPartShearCouplingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planetary_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7380.PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7380,
        )

        return self.__parent__._cast(
            _7380.PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_to_disc_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7387.RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7387,
        )

        return self.__parent__._cast(
            _7387.RingPinsToDiscConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7390.RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7390,
        )

        return self.__parent__._cast(
            _7390.RollingRingConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_to_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7394.ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7394,
        )

        return self.__parent__._cast(
            _7394.ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7397.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7397,
        )

        return self.__parent__._cast(
            _7397.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7400.SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7400,
        )

        return self.__parent__._cast(
            _7400.SpringDamperConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7403.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7403,
        )

        return self.__parent__._cast(
            _7403.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7406.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7406,
        )

        return self.__parent__._cast(
            _7406.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7415.TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7415,
        )

        return self.__parent__._cast(
            _7415.TorqueConverterConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7421.WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7421,
        )

        return self.__parent__._cast(
            _7421.WormGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7424.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7424,
        )

        return self.__parent__._cast(
            _7424.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7711.ConnectionCompoundAnalysis
):
    """ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
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
    ) -> "List[_7198.ConnectionAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ConnectionAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7198.ConnectionAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ConnectionAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "_Cast_ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(self)
