"""CylindricalPlanetGearFromCAD"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.import_from_cad import _2558

_CYLINDRICAL_PLANET_GEAR_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "CylindricalPlanetGearFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2554,
        _2557,
        _2563,
    )

    Self = TypeVar("Self", bound="CylindricalPlanetGearFromCAD")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearFromCAD._Cast_CylindricalPlanetGearFromCAD",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearFromCAD:
    """Special nested class for casting CylindricalPlanetGearFromCAD to subclasses."""

    __parent__: "CylindricalPlanetGearFromCAD"

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2558.CylindricalGearInPlanetarySetFromCAD":
        return self.__parent__._cast(_2558.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2557.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2557

        return self.__parent__._cast(_2557.CylindricalGearFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2563.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2563

        return self.__parent__._cast(_2563.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2554.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2554

        return self.__parent__._cast(_2554.ComponentFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearFromCAD":
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
class CylindricalPlanetGearFromCAD(_2558.CylindricalGearInPlanetarySetFromCAD):
    """CylindricalPlanetGearFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGearFromCAD":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearFromCAD
        """
        return _Cast_CylindricalPlanetGearFromCAD(self)
