"""CylindricalGearMeshDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6480

_CYLINDRICAL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CylindricalGearMeshDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7712,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6454,
        _6486,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7014
    from mastapy._private.system_model.connections_and_sockets.gears import _2364

    Self = TypeVar("Self", bound="CylindricalGearMeshDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshDynamicAnalysis._Cast_CylindricalGearMeshDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshDynamicAnalysis:
    """Special nested class for casting CylindricalGearMeshDynamicAnalysis to subclasses."""

    __parent__: "CylindricalGearMeshDynamicAnalysis"

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6480.GearMeshDynamicAnalysis":
        return self.__parent__._cast(_6480.GearMeshDynamicAnalysis)

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
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6454.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6454,
        )

        return self.__parent__._cast(_6454.ConnectionDynamicAnalysis)

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
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "CylindricalGearMeshDynamicAnalysis":
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
class CylindricalGearMeshDynamicAnalysis(_6480.GearMeshDynamicAnalysis):
    """CylindricalGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2364.CylindricalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7014.CylindricalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: "Self") -> "List[CylindricalGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalGearMeshDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshDynamicAnalysis
        """
        return _Cast_CylindricalGearMeshDynamicAnalysis(self)
