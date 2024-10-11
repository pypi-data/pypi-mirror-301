"""ComponentFromCAD"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COMPONENT_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ComponentFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2552,
        _2553,
        _2555,
        _2556,
        _2557,
        _2558,
        _2559,
        _2560,
        _2561,
        _2563,
        _2564,
        _2565,
        _2566,
        _2567,
        _2568,
    )

    Self = TypeVar("Self", bound="ComponentFromCAD")
    CastSelf = TypeVar("CastSelf", bound="ComponentFromCAD._Cast_ComponentFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentFromCAD:
    """Special nested class for casting ComponentFromCAD to subclasses."""

    __parent__: "ComponentFromCAD"

    @property
    def abstract_shaft_from_cad(self: "CastSelf") -> "_2552.AbstractShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2552

        return self.__parent__._cast(_2552.AbstractShaftFromCAD)

    @property
    def clutch_from_cad(self: "CastSelf") -> "_2553.ClutchFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2553

        return self.__parent__._cast(_2553.ClutchFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "_2555.ConceptBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2555

        return self.__parent__._cast(_2555.ConceptBearingFromCAD)

    @property
    def connector_from_cad(self: "CastSelf") -> "_2556.ConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2556

        return self.__parent__._cast(_2556.ConnectorFromCAD)

    @property
    def cylindrical_gear_from_cad(self: "CastSelf") -> "_2557.CylindricalGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2557

        return self.__parent__._cast(_2557.CylindricalGearFromCAD)

    @property
    def cylindrical_gear_in_planetary_set_from_cad(
        self: "CastSelf",
    ) -> "_2558.CylindricalGearInPlanetarySetFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2558

        return self.__parent__._cast(_2558.CylindricalGearInPlanetarySetFromCAD)

    @property
    def cylindrical_planet_gear_from_cad(
        self: "CastSelf",
    ) -> "_2559.CylindricalPlanetGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2559

        return self.__parent__._cast(_2559.CylindricalPlanetGearFromCAD)

    @property
    def cylindrical_ring_gear_from_cad(
        self: "CastSelf",
    ) -> "_2560.CylindricalRingGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2560

        return self.__parent__._cast(_2560.CylindricalRingGearFromCAD)

    @property
    def cylindrical_sun_gear_from_cad(
        self: "CastSelf",
    ) -> "_2561.CylindricalSunGearFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2561

        return self.__parent__._cast(_2561.CylindricalSunGearFromCAD)

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2563.MountableComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2563

        return self.__parent__._cast(_2563.MountableComponentFromCAD)

    @property
    def planet_shaft_from_cad(self: "CastSelf") -> "_2564.PlanetShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2564

        return self.__parent__._cast(_2564.PlanetShaftFromCAD)

    @property
    def pulley_from_cad(self: "CastSelf") -> "_2565.PulleyFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2565

        return self.__parent__._cast(_2565.PulleyFromCAD)

    @property
    def rigid_connector_from_cad(self: "CastSelf") -> "_2566.RigidConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2566

        return self.__parent__._cast(_2566.RigidConnectorFromCAD)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "_2567.RollingBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2567

        return self.__parent__._cast(_2567.RollingBearingFromCAD)

    @property
    def shaft_from_cad(self: "CastSelf") -> "_2568.ShaftFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2568

        return self.__parent__._cast(_2568.ShaftFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "ComponentFromCAD":
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
class ComponentFromCAD(_0.APIBase):
    """ComponentFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ComponentFromCAD
        """
        return _Cast_ComponentFromCAD(self)
