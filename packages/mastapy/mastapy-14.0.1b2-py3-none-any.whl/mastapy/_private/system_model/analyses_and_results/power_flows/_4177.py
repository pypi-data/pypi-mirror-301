"""CouplingHalfPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4221

_COUPLING_HALF_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "CouplingHalfPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4161,
        _4164,
        _4166,
        _4181,
        _4223,
        _4225,
        _4234,
        _4239,
        _4249,
        _4259,
        _4260,
        _4262,
        _4266,
        _4267,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CouplingHalfPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingHalfPowerFlow._Cast_CouplingHalfPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfPowerFlow:
    """Special nested class for casting CouplingHalfPowerFlow to subclasses."""

    __parent__: "CouplingHalfPowerFlow"

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4221.MountableComponentPowerFlow":
        return self.__parent__._cast(_4221.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4164.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4223.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartPowerFlow)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

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
    def clutch_half_power_flow(self: "CastSelf") -> "_4161.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ClutchHalfPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4166.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptCouplingHalfPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4181.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4181

        return self.__parent__._cast(_4181.CVTPulleyPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4225.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PartToPartShearCouplingHalfPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4234.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.PulleyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4239.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.RollingRingPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4249.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.SpringDamperHalfPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4260.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4260

        return self.__parent__._cast(_4260.SynchroniserPartPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4262.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4266.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4267.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.TorqueConverterTurbinePowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "CouplingHalfPowerFlow":
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
class CouplingHalfPowerFlow(_4221.MountableComponentPowerFlow):
    """CouplingHalfPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2645.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfPowerFlow
        """
        return _Cast_CouplingHalfPowerFlow(self)
