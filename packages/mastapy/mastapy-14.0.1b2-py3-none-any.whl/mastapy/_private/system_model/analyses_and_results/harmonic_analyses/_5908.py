"""InterMountableComponentConnectionHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5849

_INTER_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "InterMountableComponentConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5818,
        _5822,
        _5825,
        _5830,
        _5834,
        _5840,
        _5844,
        _5847,
        _5851,
        _5854,
        _5862,
        _5882,
        _5889,
        _5906,
        _5910,
        _5913,
        _5916,
        _5925,
        _5937,
        _5939,
        _5949,
        _5951,
        _5956,
        _5959,
        _5967,
        _5975,
        _5978,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2854,
    )
    from mastapy._private.system_model.connections_and_sockets import _2336

    Self = TypeVar("Self", bound="InterMountableComponentConnectionHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionHarmonicAnalysis._Cast_InterMountableComponentConnectionHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionHarmonicAnalysis:
    """Special nested class for casting InterMountableComponentConnectionHarmonicAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionHarmonicAnalysis"

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5849.ConnectionHarmonicAnalysis":
        return self.__parent__._cast(_5849.ConnectionHarmonicAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionStaticLoadAnalysisCase)

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
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5818.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5818,
        )

        return self.__parent__._cast(_5818.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5822.BeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5822,
        )

        return self.__parent__._cast(_5822.BeltConnectionHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5825.BevelDifferentialGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5825,
        )

        return self.__parent__._cast(_5825.BevelDifferentialGearMeshHarmonicAnalysis)

    @property
    def bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5830.BevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5830,
        )

        return self.__parent__._cast(_5830.BevelGearMeshHarmonicAnalysis)

    @property
    def clutch_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5834.ClutchConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5834,
        )

        return self.__parent__._cast(_5834.ClutchConnectionHarmonicAnalysis)

    @property
    def concept_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5840.ConceptCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5840,
        )

        return self.__parent__._cast(_5840.ConceptCouplingConnectionHarmonicAnalysis)

    @property
    def concept_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5844.ConceptGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5844,
        )

        return self.__parent__._cast(_5844.ConceptGearMeshHarmonicAnalysis)

    @property
    def conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5847.ConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5847,
        )

        return self.__parent__._cast(_5847.ConicalGearMeshHarmonicAnalysis)

    @property
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5851.CouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5851,
        )

        return self.__parent__._cast(_5851.CouplingConnectionHarmonicAnalysis)

    @property
    def cvt_belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5854.CVTBeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5854,
        )

        return self.__parent__._cast(_5854.CVTBeltConnectionHarmonicAnalysis)

    @property
    def cylindrical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5862.CylindricalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5862,
        )

        return self.__parent__._cast(_5862.CylindricalGearMeshHarmonicAnalysis)

    @property
    def face_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5882.FaceGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5882,
        )

        return self.__parent__._cast(_5882.FaceGearMeshHarmonicAnalysis)

    @property
    def gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5889.GearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5889,
        )

        return self.__parent__._cast(_5889.GearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5906.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5906,
        )

        return self.__parent__._cast(_5906.HypoidGearMeshHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5910.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5910,
        )

        return self.__parent__._cast(
            _5910.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5913.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5913,
        )

        return self.__parent__._cast(
            _5913.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5916.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5916,
        )

        return self.__parent__._cast(
            _5916.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5925.PartToPartShearCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5925,
        )

        return self.__parent__._cast(
            _5925.PartToPartShearCouplingConnectionHarmonicAnalysis
        )

    @property
    def ring_pins_to_disc_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5937.RingPinsToDiscConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5937,
        )

        return self.__parent__._cast(_5937.RingPinsToDiscConnectionHarmonicAnalysis)

    @property
    def rolling_ring_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5939.RollingRingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5939,
        )

        return self.__parent__._cast(_5939.RollingRingConnectionHarmonicAnalysis)

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5949.SpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5949,
        )

        return self.__parent__._cast(_5949.SpiralBevelGearMeshHarmonicAnalysis)

    @property
    def spring_damper_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5951.SpringDamperConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5951,
        )

        return self.__parent__._cast(_5951.SpringDamperConnectionHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5956.StraightBevelDiffGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5956,
        )

        return self.__parent__._cast(_5956.StraightBevelDiffGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5959.StraightBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5959,
        )

        return self.__parent__._cast(_5959.StraightBevelGearMeshHarmonicAnalysis)

    @property
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5967.TorqueConverterConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5967,
        )

        return self.__parent__._cast(_5967.TorqueConverterConnectionHarmonicAnalysis)

    @property
    def worm_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5975.WormGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5975,
        )

        return self.__parent__._cast(_5975.WormGearMeshHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5978.ZerolBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5978,
        )

        return self.__parent__._cast(_5978.ZerolBevelGearMeshHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionHarmonicAnalysis":
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
class InterMountableComponentConnectionHarmonicAnalysis(
    _5849.ConnectionHarmonicAnalysis
):
    """InterMountableComponentConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2336.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2854.InterMountableComponentConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.InterMountableComponentConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionHarmonicAnalysis
        """
        return _Cast_InterMountableComponentConnectionHarmonicAnalysis(self)
