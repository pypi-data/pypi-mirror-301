"""InterMountableComponentConnectionCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4311,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "InterMountableComponentConnectionCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4207
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4281,
        _4285,
        _4288,
        _4293,
        _4298,
        _4303,
        _4306,
        _4309,
        _4314,
        _4316,
        _4324,
        _4330,
        _4335,
        _4339,
        _4343,
        _4346,
        _4349,
        _4359,
        _4368,
        _4371,
        _4378,
        _4381,
        _4384,
        _4387,
        _4396,
        _4402,
        _4405,
    )

    Self = TypeVar("Self", bound="InterMountableComponentConnectionCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundPowerFlow._Cast_InterMountableComponentConnectionCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundPowerFlow:
    """Special nested class for casting InterMountableComponentConnectionCompoundPowerFlow to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundPowerFlow"

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4311.ConnectionCompoundPowerFlow":
        return self.__parent__._cast(_4311.ConnectionCompoundPowerFlow)

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
    def agma_gleason_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4281.AGMAGleasonConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4281,
        )

        return self.__parent__._cast(_4281.AGMAGleasonConicalGearMeshCompoundPowerFlow)

    @property
    def belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4285.BeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4285,
        )

        return self.__parent__._cast(_4285.BeltConnectionCompoundPowerFlow)

    @property
    def bevel_differential_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4288.BevelDifferentialGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4288,
        )

        return self.__parent__._cast(_4288.BevelDifferentialGearMeshCompoundPowerFlow)

    @property
    def bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4293.BevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4293,
        )

        return self.__parent__._cast(_4293.BevelGearMeshCompoundPowerFlow)

    @property
    def clutch_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4298.ClutchConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4298,
        )

        return self.__parent__._cast(_4298.ClutchConnectionCompoundPowerFlow)

    @property
    def concept_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4303.ConceptCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4303,
        )

        return self.__parent__._cast(_4303.ConceptCouplingConnectionCompoundPowerFlow)

    @property
    def concept_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4306.ConceptGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4306,
        )

        return self.__parent__._cast(_4306.ConceptGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4309.ConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4309,
        )

        return self.__parent__._cast(_4309.ConicalGearMeshCompoundPowerFlow)

    @property
    def coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4314.CouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4314,
        )

        return self.__parent__._cast(_4314.CouplingConnectionCompoundPowerFlow)

    @property
    def cvt_belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4316.CVTBeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4316,
        )

        return self.__parent__._cast(_4316.CVTBeltConnectionCompoundPowerFlow)

    @property
    def cylindrical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4324.CylindricalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4324,
        )

        return self.__parent__._cast(_4324.CylindricalGearMeshCompoundPowerFlow)

    @property
    def face_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4330.FaceGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4330,
        )

        return self.__parent__._cast(_4330.FaceGearMeshCompoundPowerFlow)

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4335.GearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4335,
        )

        return self.__parent__._cast(_4335.GearMeshCompoundPowerFlow)

    @property
    def hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4339.HypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4339,
        )

        return self.__parent__._cast(_4339.HypoidGearMeshCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4343.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4343,
        )

        return self.__parent__._cast(
            _4343.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4346.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4346,
        )

        return self.__parent__._cast(
            _4346.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4349.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4349,
        )

        return self.__parent__._cast(
            _4349.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4359.PartToPartShearCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4359,
        )

        return self.__parent__._cast(
            _4359.PartToPartShearCouplingConnectionCompoundPowerFlow
        )

    @property
    def ring_pins_to_disc_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4368.RingPinsToDiscConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4368,
        )

        return self.__parent__._cast(_4368.RingPinsToDiscConnectionCompoundPowerFlow)

    @property
    def rolling_ring_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4371.RollingRingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4371,
        )

        return self.__parent__._cast(_4371.RollingRingConnectionCompoundPowerFlow)

    @property
    def spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4378.SpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4378,
        )

        return self.__parent__._cast(_4378.SpiralBevelGearMeshCompoundPowerFlow)

    @property
    def spring_damper_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4381.SpringDamperConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4381,
        )

        return self.__parent__._cast(_4381.SpringDamperConnectionCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4384.StraightBevelDiffGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4384,
        )

        return self.__parent__._cast(_4384.StraightBevelDiffGearMeshCompoundPowerFlow)

    @property
    def straight_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4387.StraightBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4387,
        )

        return self.__parent__._cast(_4387.StraightBevelGearMeshCompoundPowerFlow)

    @property
    def torque_converter_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4396.TorqueConverterConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4396,
        )

        return self.__parent__._cast(_4396.TorqueConverterConnectionCompoundPowerFlow)

    @property
    def worm_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4402.WormGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4402,
        )

        return self.__parent__._cast(_4402.WormGearMeshCompoundPowerFlow)

    @property
    def zerol_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4405.ZerolBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4405,
        )

        return self.__parent__._cast(_4405.ZerolBevelGearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundPowerFlow":
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
class InterMountableComponentConnectionCompoundPowerFlow(
    _4311.ConnectionCompoundPowerFlow
):
    """InterMountableComponentConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4207.InterMountableComponentConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow]

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
    ) -> "List[_4207.InterMountableComponentConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow]

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
    ) -> "_Cast_InterMountableComponentConnectionCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundPowerFlow
        """
        return _Cast_InterMountableComponentConnectionCompoundPowerFlow(self)
