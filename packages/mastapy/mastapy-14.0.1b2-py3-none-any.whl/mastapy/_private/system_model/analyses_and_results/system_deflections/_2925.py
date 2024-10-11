"""WormGearMeshSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2846

_WORM_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "WormGearMeshSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.worm import _386
    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7712,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4270
    from mastapy._private.system_model.analyses_and_results.static_loads import _7136
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2814,
        _2854,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2384

    Self = TypeVar("Self", bound="WormGearMeshSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearMeshSystemDeflection._Cast_WormGearMeshSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearMeshSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearMeshSystemDeflection:
    """Special nested class for casting WormGearMeshSystemDeflection to subclasses."""

    __parent__: "WormGearMeshSystemDeflection"

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2846.GearMeshSystemDeflection":
        return self.__parent__._cast(_2846.GearMeshSystemDeflection)

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
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2814.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2814,
        )

        return self.__parent__._cast(_2814.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7712.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionFEAnalysis)

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
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "WormGearMeshSystemDeflection":
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
class WormGearMeshSystemDeflection(_2846.GearMeshSystemDeflection):
    """WormGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_MESH_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rating(self: "Self") -> "_386.WormGearMeshRating":
        """mastapy.gears.rating.worm.WormGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_386.WormGearMeshRating":
        """mastapy.gears.rating.worm.WormGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2384.WormGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.WormGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7136.WormGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4270.WormGearMeshPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearMeshSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_WormGearMeshSystemDeflection
        """
        return _Cast_WormGearMeshSystemDeflection(self)
