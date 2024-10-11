"""CouplingHalfLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7077

_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6984,
        _6988,
        _6990,
        _7007,
        _7081,
        _7083,
        _7093,
        _7100,
        _7110,
        _7120,
        _7122,
        _7123,
        _7127,
        _7128,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CouplingHalfLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingHalfLoadCase._Cast_CouplingHalfLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfLoadCase:
    """Special nested class for casting CouplingHalfLoadCase to subclasses."""

    __parent__: "CouplingHalfLoadCase"

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7077.MountableComponentLoadCase":
        return self.__parent__._cast(_7077.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6988.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7081.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7081,
        )

        return self.__parent__._cast(_7081.PartLoadCase)

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
    def clutch_half_load_case(self: "CastSelf") -> "_6984.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6984,
        )

        return self.__parent__._cast(_6984.ClutchHalfLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6990.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ConceptCouplingHalfLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7007.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CVTPulleyLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7083.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartToPartShearCouplingHalfLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7093.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.PulleyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7100.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.RollingRingLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7110.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.SpringDamperHalfLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserHalfLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7122.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7122,
        )

        return self.__parent__._cast(_7122.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7123.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7127.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7127,
        )

        return self.__parent__._cast(_7127.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7128.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7128,
        )

        return self.__parent__._cast(_7128.TorqueConverterTurbineLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "CouplingHalfLoadCase":
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
class CouplingHalfLoadCase(_7077.MountableComponentLoadCase):
    """CouplingHalfLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_LOAD_CASE

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalfLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfLoadCase
        """
        return _Cast_CouplingHalfLoadCase(self)
