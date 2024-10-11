"""FaceGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2591

_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.face import _1021
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets.gears import _2366
    from mastapy._private.system_model.part_model import _2490, _2526, _2535
    from mastapy._private.system_model.part_model.gears import _2587

    Self = TypeVar("Self", bound="FaceGearSet")
    CastSelf = TypeVar("CastSelf", bound="FaceGearSet._Cast_FaceGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSet:
    """Special nested class for casting FaceGearSet to subclasses."""

    __parent__: "FaceGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
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
    def face_gear_set(self: "CastSelf") -> "FaceGearSet":
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
class FaceGearSet(_2591.GearSet):
    """FaceGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_set_design(self: "Self") -> "_1021.FaceGearSetDesign":
        """mastapy.gears.gear_designs.face.FaceGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_gear_set_design(self: "Self") -> "_1021.FaceGearSetDesign":
        """mastapy.gears.gear_designs.face.FaceGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_gears(self: "Self") -> "List[_2587.FaceGear]":
        """List[mastapy.system_model.part_model.gears.FaceGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_meshes(self: "Self") -> "List[_2366.FaceGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.FaceGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSet":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSet
        """
        return _Cast_FaceGearSet(self)
