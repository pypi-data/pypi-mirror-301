"""ConnectorSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.system_deflections import _2871

_CONNECTOR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ConnectorSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility.measured_vectors import _1612
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4175
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2785,
        _2802,
        _2844,
        _2873,
        _2874,
        _2890,
    )
    from mastapy._private.system_model.fe import _2441
    from mastapy._private.system_model.part_model import _2503

    Self = TypeVar("Self", bound="ConnectorSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectorSystemDeflection._Cast_ConnectorSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorSystemDeflection:
    """Special nested class for casting ConnectorSystemDeflection to subclasses."""

    __parent__: "ConnectorSystemDeflection"

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2871.MountableComponentSystemDeflection":
        return self.__parent__._cast(_2871.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2802.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2802,
        )

        return self.__parent__._cast(_2802.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

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
    def bearing_system_deflection(self: "CastSelf") -> "_2785.BearingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2785,
        )

        return self.__parent__._cast(_2785.BearingSystemDeflection)

    @property
    def oil_seal_system_deflection(self: "CastSelf") -> "_2873.OilSealSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2873,
        )

        return self.__parent__._cast(_2873.OilSealSystemDeflection)

    @property
    def shaft_hub_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2890.ShaftHubConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2890,
        )

        return self.__parent__._cast(_2890.ShaftHubConnectionSystemDeflection)

    @property
    def connector_system_deflection(self: "CastSelf") -> "ConnectorSystemDeflection":
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
class ConnectorSystemDeflection(_2871.MountableComponentSystemDeflection):
    """ConnectorSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def convergence_delta_energy(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConvergenceDeltaEnergy")

        if temp is None:
            return 0.0

        return temp

    @property
    def linear_force_on_inner(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearForceOnInner")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def moment_on_inner(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentOnInner")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def component_design(self: "Self") -> "_2503.Connector":
        """mastapy.system_model.part_model.Connector

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_on_outer_support_in_lcs(
        self: "Self",
    ) -> "_1612.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceOnOuterSupportInLCS")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def force_on_outer_support_in_wcs(
        self: "Self",
    ) -> "_1612.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceOnOuterSupportInWCS")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_fe_part(self: "Self") -> "_2844.FEPartSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.FEPartSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterFEPart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_fe_substructure_nodes(self: "Self") -> "List[_2441.FESubstructureNode]":
        """List[mastapy.system_model.fe.FESubstructureNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterFESubstructureNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_flow_results(self: "Self") -> "_4175.ConnectorPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectorSystemDeflection
        """
        return _Cast_ConnectorSystemDeflection(self)
