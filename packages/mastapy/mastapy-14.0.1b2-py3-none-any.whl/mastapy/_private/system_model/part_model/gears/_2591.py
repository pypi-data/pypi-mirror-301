"""GearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _976
from mastapy._private.system_model.part_model import _2535

_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2490, _2526
    from mastapy._private.system_model.part_model.gears import (
        _2573,
        _2575,
        _2579,
        _2581,
        _2583,
        _2585,
        _2588,
        _2594,
        _2596,
        _2598,
        _2600,
        _2601,
        _2603,
        _2605,
        _2607,
        _2611,
        _2613,
    )

    Self = TypeVar("Self", bound="GearSet")
    CastSelf = TypeVar("CastSelf", bound="GearSet._Cast_GearSet")


__docformat__ = "restructuredtext en"
__all__ = ("GearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSet:
    """Special nested class for casting GearSet to subclasses."""

    __parent__: "GearSet"

    @property
    def specialised_assembly(self: "CastSelf") -> "_2535.SpecialisedAssembly":
        return self.__parent__._cast(_2535.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2490.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2490

        return self.__parent__._cast(_2490.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2573.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2575.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2579.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2581.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2583.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2585.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2588.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.FaceGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2594.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2600.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2601.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.PlanetaryGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2603.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2605.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2607.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2611.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2613.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.ZerolBevelGearSet)

    @property
    def gear_set(self: "CastSelf") -> "GearSet":
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
class GearSet(_2535.SpecialisedAssembly):
    """GearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_design(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_GearSetDesign":
        """ListWithSelectedItem[mastapy.gears.gear_designs.GearSetDesign]"""
        temp = pythonnet_property_get(self.wrapped, "ActiveDesign")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_GearSetDesign",
        )(temp)

    @active_design.setter
    @enforce_parameter_types
    def active_design(self: "Self", value: "_976.GearSetDesign") -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_GearSetDesign.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_GearSetDesign.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(self.wrapped, "ActiveDesign", value)

    @property
    def maximum_number_of_teeth_in_mesh(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeethInMesh")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth_in_mesh.setter
    @enforce_parameter_types
    def maximum_number_of_teeth_in_mesh(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfTeethInMesh",
            int(value) if value is not None else 0,
        )

    @property
    def mesh_ratio_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeshRatioLimit")

        if temp is None:
            return 0.0

        return temp

    @mesh_ratio_limit.setter
    @enforce_parameter_types
    def mesh_ratio_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeshRatioLimit", float(value) if value is not None else 0.0
        )

    @property
    def minimum_number_of_teeth_in_mesh(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeethInMesh")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth_in_mesh.setter
    @enforce_parameter_types
    def minimum_number_of_teeth_in_mesh(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfTeethInMesh",
            int(value) if value is not None else 0,
        )

    @property
    def required_safety_factor_for_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RequiredSafetyFactorForBending", value)

    @property
    def required_safety_factor_for_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RequiredSafetyFactorForContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RequiredSafetyFactorForContact", value)

    @property
    def required_safety_factor_for_static_bending(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticBending"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_static_bending.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_bending(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RequiredSafetyFactorForStaticBending", value
        )

    @property
    def required_safety_factor_for_static_contact(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForStaticContact"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @required_safety_factor_for_static_contact.setter
    @enforce_parameter_types
    def required_safety_factor_for_static_contact(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "RequiredSafetyFactorForStaticContact", value
        )

    @property
    def active_gear_set_design(self: "Self") -> "_976.GearSetDesign":
        """mastapy.gears.gear_designs.GearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_set_designs(self: "Self") -> "List[_976.GearSetDesign]":
        """List[mastapy.gears.gear_designs.GearSetDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def add_gear_set_design(self: "Self", design: "_976.GearSetDesign") -> None:
        """Method does not return.

        Args:
            design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped, "AddGearSetDesign", design.wrapped if design else None
        )

    @enforce_parameter_types
    def remove_design(self: "Self", design: "_976.GearSetDesign") -> None:
        """Method does not return.

        Args:
            design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveDesign", design.wrapped if design else None
        )

    @enforce_parameter_types
    def set_active_gear_set_design(
        self: "Self", gear_set_design: "_976.GearSetDesign"
    ) -> None:
        """Method does not return.

        Args:
            gear_set_design (mastapy.gears.gear_designs.GearSetDesign)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetActiveGearSetDesign",
            gear_set_design.wrapped if gear_set_design else None,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSet":
        """Cast to another type.

        Returns:
            _Cast_GearSet
        """
        return _Cast_GearSet(self)
