"""ConnectionFEAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7713

_CONNECTION_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "ConnectionFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6422,
        _6424,
        _6428,
        _6431,
        _6436,
        _6440,
        _6443,
        _6445,
        _6449,
        _6452,
        _6454,
        _6456,
        _6459,
        _6463,
        _6465,
        _6467,
        _6475,
        _6480,
        _6484,
        _6486,
        _6488,
        _6491,
        _6494,
        _6503,
        _6506,
        _6513,
        _6515,
        _6520,
        _6523,
        _6525,
        _6529,
        _6532,
        _6540,
        _6547,
        _6550,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2775,
        _2776,
        _2786,
        _2788,
        _2793,
        _2798,
        _2801,
        _2804,
        _2807,
        _2811,
        _2814,
        _2816,
        _2819,
        _2823,
        _2824,
        _2826,
        _2827,
        _2828,
        _2841,
        _2846,
        _2850,
        _2854,
        _2855,
        _2858,
        _2861,
        _2875,
        _2878,
        _2884,
        _2887,
        _2894,
        _2896,
        _2899,
        _2902,
        _2905,
        _2917,
        _2925,
        _2928,
    )

    Self = TypeVar("Self", bound="ConnectionFEAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionFEAnalysis._Cast_ConnectionFEAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionFEAnalysis:
    """Special nested class for casting ConnectionFEAnalysis to subclasses."""

    __parent__: "ConnectionFEAnalysis"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
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
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2775.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2775,
        )

        return self.__parent__._cast(
            _2775.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2776.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2776,
        )

        return self.__parent__._cast(_2776.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2786.BeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2786,
        )

        return self.__parent__._cast(_2786.BeltConnectionSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2788.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2788,
        )

        return self.__parent__._cast(_2788.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2793.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2793,
        )

        return self.__parent__._cast(_2793.BevelGearMeshSystemDeflection)

    @property
    def clutch_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2798.ClutchConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2798,
        )

        return self.__parent__._cast(_2798.ClutchConnectionSystemDeflection)

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2801.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2801,
        )

        return self.__parent__._cast(_2801.CoaxialConnectionSystemDeflection)

    @property
    def concept_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2804.ConceptCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2804,
        )

        return self.__parent__._cast(_2804.ConceptCouplingConnectionSystemDeflection)

    @property
    def concept_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2807.ConceptGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2807,
        )

        return self.__parent__._cast(_2807.ConceptGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2811.ConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2811,
        )

        return self.__parent__._cast(_2811.ConicalGearMeshSystemDeflection)

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2814.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2814,
        )

        return self.__parent__._cast(_2814.ConnectionSystemDeflection)

    @property
    def coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2816.CouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2816,
        )

        return self.__parent__._cast(_2816.CouplingConnectionSystemDeflection)

    @property
    def cvt_belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2819.CVTBeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2819,
        )

        return self.__parent__._cast(_2819.CVTBeltConnectionSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2823.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2823,
        )

        return self.__parent__._cast(
            _2823.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2824.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2824,
        )

        return self.__parent__._cast(
            _2824.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2826.CylindricalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2826,
        )

        return self.__parent__._cast(_2826.CylindricalGearMeshSystemDeflection)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2827.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2827,
        )

        return self.__parent__._cast(_2827.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2828.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2828,
        )

        return self.__parent__._cast(
            _2828.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2841.FaceGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2841,
        )

        return self.__parent__._cast(_2841.FaceGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2846.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2846,
        )

        return self.__parent__._cast(_2846.GearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2850.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2850,
        )

        return self.__parent__._cast(_2850.HypoidGearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2854.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2854,
        )

        return self.__parent__._cast(
            _2854.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2855.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2855,
        )

        return self.__parent__._cast(
            _2855.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2858.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2858,
        )

        return self.__parent__._cast(
            _2858.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2861.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2861,
        )

        return self.__parent__._cast(
            _2861.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2875.PartToPartShearCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2875,
        )

        return self.__parent__._cast(
            _2875.PartToPartShearCouplingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2878.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2878,
        )

        return self.__parent__._cast(_2878.PlanetaryConnectionSystemDeflection)

    @property
    def ring_pins_to_disc_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2884.RingPinsToDiscConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2884,
        )

        return self.__parent__._cast(_2884.RingPinsToDiscConnectionSystemDeflection)

    @property
    def rolling_ring_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2887.RollingRingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2887,
        )

        return self.__parent__._cast(_2887.RollingRingConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2894.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2894,
        )

        return self.__parent__._cast(
            _2894.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2896.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2896,
        )

        return self.__parent__._cast(_2896.SpiralBevelGearMeshSystemDeflection)

    @property
    def spring_damper_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2899.SpringDamperConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2899,
        )

        return self.__parent__._cast(_2899.SpringDamperConnectionSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2902.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2902,
        )

        return self.__parent__._cast(_2902.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2905.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2905,
        )

        return self.__parent__._cast(_2905.StraightBevelGearMeshSystemDeflection)

    @property
    def torque_converter_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2917.TorqueConverterConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2917,
        )

        return self.__parent__._cast(_2917.TorqueConverterConnectionSystemDeflection)

    @property
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2925.WormGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2925,
        )

        return self.__parent__._cast(_2925.WormGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2928.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2928,
        )

        return self.__parent__._cast(_2928.ZerolBevelGearMeshSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6422.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6422,
        )

        return self.__parent__._cast(
            _6422.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6424.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6424,
        )

        return self.__parent__._cast(_6424.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6428.BeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6428,
        )

        return self.__parent__._cast(_6428.BeltConnectionDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6431.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6431,
        )

        return self.__parent__._cast(_6431.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6436.BevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6436,
        )

        return self.__parent__._cast(_6436.BevelGearMeshDynamicAnalysis)

    @property
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6440.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6440,
        )

        return self.__parent__._cast(_6440.ClutchConnectionDynamicAnalysis)

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6443.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6443,
        )

        return self.__parent__._cast(_6443.CoaxialConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6445.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6445,
        )

        return self.__parent__._cast(_6445.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def concept_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6449.ConceptGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6449,
        )

        return self.__parent__._cast(_6449.ConceptGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6452.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6452,
        )

        return self.__parent__._cast(_6452.ConicalGearMeshDynamicAnalysis)

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6454.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6454,
        )

        return self.__parent__._cast(_6454.ConnectionDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6456.CouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6456,
        )

        return self.__parent__._cast(_6456.CouplingConnectionDynamicAnalysis)

    @property
    def cvt_belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6459.CVTBeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6459,
        )

        return self.__parent__._cast(_6459.CVTBeltConnectionDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6463.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6463,
        )

        return self.__parent__._cast(
            _6463.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6465.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6465,
        )

        return self.__parent__._cast(
            _6465.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6467.CylindricalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6467,
        )

        return self.__parent__._cast(_6467.CylindricalGearMeshDynamicAnalysis)

    @property
    def face_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6475.FaceGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6475,
        )

        return self.__parent__._cast(_6475.FaceGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6480.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6480,
        )

        return self.__parent__._cast(_6480.GearMeshDynamicAnalysis)

    @property
    def hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6484.HypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6484,
        )

        return self.__parent__._cast(_6484.HypoidGearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6486.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6486,
        )

        return self.__parent__._cast(
            _6486.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6488.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6488,
        )

        return self.__parent__._cast(
            _6488.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6491.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6491,
        )

        return self.__parent__._cast(
            _6491.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6494.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6494,
        )

        return self.__parent__._cast(
            _6494.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6503.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6503,
        )

        return self.__parent__._cast(
            _6503.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6506.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6506,
        )

        return self.__parent__._cast(_6506.PlanetaryConnectionDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6513.RingPinsToDiscConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6513,
        )

        return self.__parent__._cast(_6513.RingPinsToDiscConnectionDynamicAnalysis)

    @property
    def rolling_ring_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6515.RollingRingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6515,
        )

        return self.__parent__._cast(_6515.RollingRingConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6520.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6520,
        )

        return self.__parent__._cast(
            _6520.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6523.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6523,
        )

        return self.__parent__._cast(_6523.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6525.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6525,
        )

        return self.__parent__._cast(_6525.SpringDamperConnectionDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6529.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6529,
        )

        return self.__parent__._cast(_6529.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6532.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6532,
        )

        return self.__parent__._cast(_6532.StraightBevelGearMeshDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6540.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6540,
        )

        return self.__parent__._cast(_6540.TorqueConverterConnectionDynamicAnalysis)

    @property
    def worm_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6547.WormGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6547,
        )

        return self.__parent__._cast(_6547.WormGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6550.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6550,
        )

        return self.__parent__._cast(_6550.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "ConnectionFEAnalysis":
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
class ConnectionFEAnalysis(_7713.ConnectionStaticLoadAnalysisCase):
    """ConnectionFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionFEAnalysis
        """
        return _Cast_ConnectionFEAnalysis(self)
