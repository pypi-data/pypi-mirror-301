"""KlingelnbergCycloPalloidConicalGearMeshLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6997

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidConicalGearMeshLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7000,
        _7043,
        _7062,
        _7067,
        _7070,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2373

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshLoadCase._Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshLoadCase to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshLoadCase"

    @property
    def conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6997.ConicalGearMeshLoadCase":
        return self.__parent__._cast(_6997.ConicalGearMeshLoadCase)

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "_7043.GearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearMeshLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7062.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7062,
        )

        return self.__parent__._cast(_7062.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_7000.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7000,
        )

        return self.__parent__._cast(_7000.ConnectionLoadCase)

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
    def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshLoadCase":
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
class KlingelnbergCycloPalloidConicalGearMeshLoadCase(_6997.ConicalGearMeshLoadCase):
    """KlingelnbergCycloPalloidConicalGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2373.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshLoadCase(self)
