"""CylindricalGearLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7041

_CYLINDRICAL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CylindricalGearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1135
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6988,
        _7013,
        _7017,
        _7077,
        _7081,
    )
    from mastapy._private.system_model.part_model.gears import _2584

    Self = TypeVar("Self", bound="CylindricalGearLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearLoadCase._Cast_CylindricalGearLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearLoadCase:
    """Special nested class for casting CylindricalGearLoadCase to subclasses."""

    __parent__: "CylindricalGearLoadCase"

    @property
    def gear_load_case(self: "CastSelf") -> "_7041.GearLoadCase":
        return self.__parent__._cast(_7041.GearLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7077.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7077,
        )

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
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7017.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.CylindricalPlanetGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "CylindricalGearLoadCase":
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
class CylindricalGearLoadCase(_7041.GearLoadCase):
    """CylindricalGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_reaction_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialReactionForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def lateral_reaction_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LateralReactionForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def lateral_reaction_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LateralReactionMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    def override_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverrideMicroGeometry")

        if temp is None:
            return False

        return temp

    @override_micro_geometry.setter
    @enforce_parameter_types
    def override_micro_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    def power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Power")

        if temp is None:
            return 0.0

        return temp

    @property
    def reversed_bending_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ReversedBendingFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @reversed_bending_factor.setter
    @enforce_parameter_types
    def reversed_bending_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ReversedBendingFactor", value)

    @property
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    def torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @property
    def vertical_reaction_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VerticalReactionForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def vertical_reaction_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VerticalReactionMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2584.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_manufacture_errors(
        self: "Self",
    ) -> "_7013.CylindricalGearManufactureError":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearManufactureError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearManufactureErrors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def overridden_micro_geometry(
        self: "Self",
    ) -> "_1135.CylindricalGearMicroGeometryBase":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearMicroGeometryBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverriddenMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: "Self") -> "List[CylindricalGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase]

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearLoadCase
        """
        return _Cast_CylindricalGearLoadCase(self)
