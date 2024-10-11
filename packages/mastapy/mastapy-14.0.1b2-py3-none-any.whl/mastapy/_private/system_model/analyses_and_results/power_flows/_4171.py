"""ConicalGearMeshPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4200

_CONICAL_GEAR_MESH_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConicalGearMeshPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4143,
        _4150,
        _4155,
        _4174,
        _4204,
        _4207,
        _4208,
        _4211,
        _4214,
        _4245,
        _4251,
        _4254,
        _4273,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2362

    Self = TypeVar("Self", bound="ConicalGearMeshPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshPowerFlow:
    """Special nested class for casting ConicalGearMeshPowerFlow to subclasses."""

    __parent__: "ConicalGearMeshPowerFlow"

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4200.GearMeshPowerFlow":
        return self.__parent__._cast(_4200.GearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4207.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(_4207.InterMountableComponentConnectionPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "_4174.ConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.ConnectionPowerFlow)

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
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4143.AGMAGleasonConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4143

        return self.__parent__._cast(_4143.AGMAGleasonConicalGearMeshPowerFlow)

    @property
    def bevel_differential_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4150.BevelDifferentialGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4150

        return self.__parent__._cast(_4150.BevelDifferentialGearMeshPowerFlow)

    @property
    def bevel_gear_mesh_power_flow(self: "CastSelf") -> "_4155.BevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4155

        return self.__parent__._cast(_4155.BevelGearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4204.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4204

        return self.__parent__._cast(_4204.HypoidGearMeshPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4208.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4208

        return self.__parent__._cast(
            _4208.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4211.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4211

        return self.__parent__._cast(
            _4211.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4214.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4214

        return self.__parent__._cast(
            _4214.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        )

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4245.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4245

        return self.__parent__._cast(_4245.SpiralBevelGearMeshPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4251.StraightBevelDiffGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4251

        return self.__parent__._cast(_4251.StraightBevelDiffGearMeshPowerFlow)

    @property
    def straight_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4273.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4273

        return self.__parent__._cast(_4273.ZerolBevelGearMeshPowerFlow)

    @property
    def conical_gear_mesh_power_flow(self: "CastSelf") -> "ConicalGearMeshPowerFlow":
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
class ConicalGearMeshPowerFlow(_4200.GearMeshPowerFlow):
    """ConicalGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2362.ConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshPowerFlow
        """
        return _Cast_ConicalGearMeshPowerFlow(self)
