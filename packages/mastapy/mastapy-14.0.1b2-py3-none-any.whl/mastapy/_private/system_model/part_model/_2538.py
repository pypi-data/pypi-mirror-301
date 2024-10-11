"""VirtualComponent"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2522

_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import (
        _2500,
        _2518,
        _2519,
        _2526,
        _2529,
        _2530,
        _2536,
    )

    Self = TypeVar("Self", bound="VirtualComponent")
    CastSelf = TypeVar("CastSelf", bound="VirtualComponent._Cast_VirtualComponent")


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponent:
    """Special nested class for casting VirtualComponent to subclasses."""

    __parent__: "VirtualComponent"

    @property
    def mountable_component(self: "CastSelf") -> "_2522.MountableComponent":
        return self.__parent__._cast(_2522.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2500.Component":
        from mastapy._private.system_model.part_model import _2500

        return self.__parent__._cast(_2500.Component)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def mass_disc(self: "CastSelf") -> "_2518.MassDisc":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2519.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2519

        return self.__parent__._cast(_2519.MeasurementComponent)

    @property
    def point_load(self: "CastSelf") -> "_2529.PointLoad":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2530.PowerLoad":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2536.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "VirtualComponent":
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
class VirtualComponent(_2522.MountableComponent):
    """VirtualComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponent":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponent
        """
        return _Cast_VirtualComponent(self)
