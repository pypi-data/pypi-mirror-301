"""ShaftHubConnectionPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4175

_SHAFT_HUB_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "ShaftHubConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.rating import _1484
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4164,
        _4221,
        _4223,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7102
    from mastapy._private.system_model.part_model.couplings import _2660

    Self = TypeVar("Self", bound="ShaftHubConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftHubConnectionPowerFlow._Cast_ShaftHubConnectionPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionPowerFlow:
    """Special nested class for casting ShaftHubConnectionPowerFlow to subclasses."""

    __parent__: "ShaftHubConnectionPowerFlow"

    @property
    def connector_power_flow(self: "CastSelf") -> "_4175.ConnectorPowerFlow":
        return self.__parent__._cast(_4175.ConnectorPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4221.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4221

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
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "ShaftHubConnectionPowerFlow":
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
class ShaftHubConnectionPowerFlow(_4175.ConnectorPowerFlow):
    """ShaftHubConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2660.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_1484.ShaftHubConnectionRating":
        """mastapy.detailed_rigid_connectors.rating.ShaftHubConnectionRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7102.ShaftHubConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionPowerFlow
        """
        return _Cast_ShaftHubConnectionPowerFlow(self)
