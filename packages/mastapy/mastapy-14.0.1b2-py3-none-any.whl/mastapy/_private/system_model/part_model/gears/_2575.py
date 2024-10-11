"""BevelDifferentialGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2579

_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1222
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets.gears import _2358
    from mastapy._private.system_model.part_model import _2490, _2526, _2535
    from mastapy._private.system_model.part_model.gears import (
        _2573,
        _2578,
        _2583,
        _2591,
    )

    Self = TypeVar("Self", bound="BevelDifferentialGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelDifferentialGearSet._Cast_BevelDifferentialGearSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearSet:
    """Special nested class for casting BevelDifferentialGearSet to subclasses."""

    __parent__: "BevelDifferentialGearSet"

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2579.BevelGearSet":
        return self.__parent__._cast(_2579.BevelGearSet)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2573.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.AGMAGleasonConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2583.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2535.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2535

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
    def bevel_differential_gear_set(self: "CastSelf") -> "BevelDifferentialGearSet":
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
class BevelDifferentialGearSet(_2579.BevelGearSet):
    """BevelDifferentialGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_set_design(self: "Self") -> "_1222.BevelGearSetDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gear_set_design(self: "Self") -> "_1222.BevelGearSetDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gears(self: "Self") -> "List[_2578.BevelGear]":
        """List[mastapy.system_model.part_model.gears.BevelGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes(self: "Self") -> "List[_2358.BevelGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.BevelGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearSet":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearSet
        """
        return _Cast_BevelDifferentialGearSet(self)
