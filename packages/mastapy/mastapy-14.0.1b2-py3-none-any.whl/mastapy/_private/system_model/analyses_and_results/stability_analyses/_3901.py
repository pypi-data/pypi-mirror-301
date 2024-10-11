"""ConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7713

_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "ConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3869,
        _3870,
        _3875,
        _3877,
        _3882,
        _3887,
        _3890,
        _3892,
        _3895,
        _3898,
        _3903,
        _3907,
        _3911,
        _3912,
        _3914,
        _3921,
        _3926,
        _3930,
        _3933,
        _3934,
        _3937,
        _3940,
        _3950,
        _3953,
        _3960,
        _3962,
        _3967,
        _3969,
        _3972,
        _3975,
        _3978,
        _3981,
        _3990,
        _3996,
        _3999,
    )
    from mastapy._private.system_model.connections_and_sockets import _2327

    Self = TypeVar("Self", bound="ConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionStabilityAnalysis._Cast_ConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionStabilityAnalysis:
    """Special nested class for casting ConnectionStabilityAnalysis to subclasses."""

    __parent__: "ConnectionStabilityAnalysis"

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
    def abstract_shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3869.AbstractShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3869,
        )

        return self.__parent__._cast(
            _3869.AbstractShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3870.AGMAGleasonConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3870,
        )

        return self.__parent__._cast(_3870.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3875.BeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3875,
        )

        return self.__parent__._cast(_3875.BeltConnectionStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3877.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3877,
        )

        return self.__parent__._cast(_3877.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3882.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3882,
        )

        return self.__parent__._cast(_3882.BevelGearMeshStabilityAnalysis)

    @property
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3887.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3887,
        )

        return self.__parent__._cast(_3887.ClutchConnectionStabilityAnalysis)

    @property
    def coaxial_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3890.CoaxialConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3890,
        )

        return self.__parent__._cast(_3890.CoaxialConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3892.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3892,
        )

        return self.__parent__._cast(_3892.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def concept_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3895.ConceptGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3895,
        )

        return self.__parent__._cast(_3895.ConceptGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3898.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3898,
        )

        return self.__parent__._cast(_3898.ConicalGearMeshStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3903.CouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3903,
        )

        return self.__parent__._cast(_3903.CouplingConnectionStabilityAnalysis)

    @property
    def cvt_belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3907.CVTBeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3907,
        )

        return self.__parent__._cast(_3907.CVTBeltConnectionStabilityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3911.CycloidalDiscCentralBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3911,
        )

        return self.__parent__._cast(
            _3911.CycloidalDiscCentralBearingConnectionStabilityAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3912.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3912,
        )

        return self.__parent__._cast(
            _3912.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis
        )

    @property
    def cylindrical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3914.CylindricalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3914,
        )

        return self.__parent__._cast(_3914.CylindricalGearMeshStabilityAnalysis)

    @property
    def face_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3921.FaceGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3921,
        )

        return self.__parent__._cast(_3921.FaceGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3926.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3926,
        )

        return self.__parent__._cast(_3926.GearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3930.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3930,
        )

        return self.__parent__._cast(_3930.HypoidGearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3933.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3933,
        )

        return self.__parent__._cast(
            _3933.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3934.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3934,
        )

        return self.__parent__._cast(
            _3934.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3937.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3937,
        )

        return self.__parent__._cast(
            _3937.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3940.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3940,
        )

        return self.__parent__._cast(
            _3940.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3950.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3950,
        )

        return self.__parent__._cast(
            _3950.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def planetary_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3953.PlanetaryConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3953,
        )

        return self.__parent__._cast(_3953.PlanetaryConnectionStabilityAnalysis)

    @property
    def ring_pins_to_disc_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3960.RingPinsToDiscConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3960,
        )

        return self.__parent__._cast(_3960.RingPinsToDiscConnectionStabilityAnalysis)

    @property
    def rolling_ring_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3962.RollingRingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3962,
        )

        return self.__parent__._cast(_3962.RollingRingConnectionStabilityAnalysis)

    @property
    def shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3967.ShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3967,
        )

        return self.__parent__._cast(
            _3967.ShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3969.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3969,
        )

        return self.__parent__._cast(_3969.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3972.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3972,
        )

        return self.__parent__._cast(_3972.SpringDamperConnectionStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3978.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3978,
        )

        return self.__parent__._cast(_3978.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3981.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3981,
        )

        return self.__parent__._cast(_3981.StraightBevelGearMeshStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3990.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3990,
        )

        return self.__parent__._cast(_3990.TorqueConverterConnectionStabilityAnalysis)

    @property
    def worm_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3996.WormGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3996,
        )

        return self.__parent__._cast(_3996.WormGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3999.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3999,
        )

        return self.__parent__._cast(_3999.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "ConnectionStabilityAnalysis":
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
class ConnectionStabilityAnalysis(_7713.ConnectionStaticLoadAnalysisCase):
    """ConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2327.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2327.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis(self: "Self") -> "_3975.StabilityAnalysis":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionStabilityAnalysis
        """
        return _Cast_ConnectionStabilityAnalysis(self)
