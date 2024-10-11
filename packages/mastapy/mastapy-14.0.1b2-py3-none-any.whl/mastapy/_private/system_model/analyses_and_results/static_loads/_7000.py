"""ConnectionLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2736

_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ConnectionLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6955,
        _6956,
        _6960,
        _6965,
        _6971,
        _6974,
        _6979,
        _6983,
        _6987,
        _6989,
        _6993,
        _6997,
        _7002,
        _7005,
        _7009,
        _7011,
        _7014,
        _7036,
        _7043,
        _7057,
        _7062,
        _7064,
        _7067,
        _7070,
        _7082,
        _7085,
        _7097,
        _7099,
        _7104,
        _7107,
        _7109,
        _7113,
        _7116,
        _7125,
        _7136,
        _7139,
    )
    from mastapy._private.system_model.connections_and_sockets import _2327

    Self = TypeVar("Self", bound="ConnectionLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ConnectionLoadCase._Cast_ConnectionLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionLoadCase:
    """Special nested class for casting ConnectionLoadCase to subclasses."""

    __parent__: "ConnectionLoadCase"

    @property
    def connection_analysis(self: "CastSelf") -> "_2736.ConnectionAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_6960.AbstractShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6960,
        )

        return self.__parent__._cast(
            _6960.AbstractShaftToMountableComponentConnectionLoadCase
        )

    @property
    def agma_gleason_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6965.AGMAGleasonConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6965,
        )

        return self.__parent__._cast(_6965.AGMAGleasonConicalGearMeshLoadCase)

    @property
    def belt_connection_load_case(self: "CastSelf") -> "_6971.BeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6971,
        )

        return self.__parent__._cast(_6971.BeltConnectionLoadCase)

    @property
    def bevel_differential_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6974.BevelDifferentialGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6974,
        )

        return self.__parent__._cast(_6974.BevelDifferentialGearMeshLoadCase)

    @property
    def bevel_gear_mesh_load_case(self: "CastSelf") -> "_6979.BevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6979,
        )

        return self.__parent__._cast(_6979.BevelGearMeshLoadCase)

    @property
    def clutch_connection_load_case(
        self: "CastSelf",
    ) -> "_6983.ClutchConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6983,
        )

        return self.__parent__._cast(_6983.ClutchConnectionLoadCase)

    @property
    def coaxial_connection_load_case(
        self: "CastSelf",
    ) -> "_6987.CoaxialConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.CoaxialConnectionLoadCase)

    @property
    def concept_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_6989.ConceptCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6989,
        )

        return self.__parent__._cast(_6989.ConceptCouplingConnectionLoadCase)

    @property
    def concept_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6993.ConceptGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6993,
        )

        return self.__parent__._cast(_6993.ConceptGearMeshLoadCase)

    @property
    def conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6997.ConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6997,
        )

        return self.__parent__._cast(_6997.ConicalGearMeshLoadCase)

    @property
    def coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7002.CouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7002,
        )

        return self.__parent__._cast(_7002.CouplingConnectionLoadCase)

    @property
    def cvt_belt_connection_load_case(
        self: "CastSelf",
    ) -> "_7005.CVTBeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7005,
        )

        return self.__parent__._cast(_7005.CVTBeltConnectionLoadCase)

    @property
    def cycloidal_disc_central_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7009.CycloidalDiscCentralBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7009,
        )

        return self.__parent__._cast(
            _7009.CycloidalDiscCentralBearingConnectionLoadCase
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "_7011.CycloidalDiscPlanetaryBearingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7011,
        )

        return self.__parent__._cast(
            _7011.CycloidalDiscPlanetaryBearingConnectionLoadCase
        )

    @property
    def cylindrical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7014.CylindricalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7014,
        )

        return self.__parent__._cast(_7014.CylindricalGearMeshLoadCase)

    @property
    def face_gear_mesh_load_case(self: "CastSelf") -> "_7036.FaceGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7036,
        )

        return self.__parent__._cast(_7036.FaceGearMeshLoadCase)

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "_7043.GearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearMeshLoadCase)

    @property
    def hypoid_gear_mesh_load_case(self: "CastSelf") -> "_7057.HypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7057,
        )

        return self.__parent__._cast(_7057.HypoidGearMeshLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7062.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7062,
        )

        return self.__parent__._cast(_7062.InterMountableComponentConnectionLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7064.KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7064,
        )

        return self.__parent__._cast(
            _7064.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7067.KlingelnbergCycloPalloidHypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7067,
        )

        return self.__parent__._cast(
            _7067.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7070.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7070,
        )

        return self.__parent__._cast(
            _7070.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        )

    @property
    def part_to_part_shear_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7082.PartToPartShearCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7082,
        )

        return self.__parent__._cast(_7082.PartToPartShearCouplingConnectionLoadCase)

    @property
    def planetary_connection_load_case(
        self: "CastSelf",
    ) -> "_7085.PlanetaryConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7085,
        )

        return self.__parent__._cast(_7085.PlanetaryConnectionLoadCase)

    @property
    def ring_pins_to_disc_connection_load_case(
        self: "CastSelf",
    ) -> "_7097.RingPinsToDiscConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7097,
        )

        return self.__parent__._cast(_7097.RingPinsToDiscConnectionLoadCase)

    @property
    def rolling_ring_connection_load_case(
        self: "CastSelf",
    ) -> "_7099.RollingRingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7099,
        )

        return self.__parent__._cast(_7099.RollingRingConnectionLoadCase)

    @property
    def shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7104.ShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7104,
        )

        return self.__parent__._cast(_7104.ShaftToMountableComponentConnectionLoadCase)

    @property
    def spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7107.SpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpiralBevelGearMeshLoadCase)

    @property
    def spring_damper_connection_load_case(
        self: "CastSelf",
    ) -> "_7109.SpringDamperConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7109,
        )

        return self.__parent__._cast(_7109.SpringDamperConnectionLoadCase)

    @property
    def straight_bevel_diff_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7113.StraightBevelDiffGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7113,
        )

        return self.__parent__._cast(_7113.StraightBevelDiffGearMeshLoadCase)

    @property
    def straight_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelGearMeshLoadCase)

    @property
    def torque_converter_connection_load_case(
        self: "CastSelf",
    ) -> "_7125.TorqueConverterConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.TorqueConverterConnectionLoadCase)

    @property
    def worm_gear_mesh_load_case(self: "CastSelf") -> "_7136.WormGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7136,
        )

        return self.__parent__._cast(_7136.WormGearMeshLoadCase)

    @property
    def zerol_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7139.ZerolBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7139,
        )

        return self.__parent__._cast(_7139.ZerolBevelGearMeshLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "ConnectionLoadCase":
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
class ConnectionLoadCase(_2736.ConnectionAnalysis):
    """ConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_LOAD_CASE

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
    def static_load_case(self: "Self") -> "_6955.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: "Self") -> "_6956.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ConnectionLoadCase
        """
        return _Cast_ConnectionLoadCase(self)
