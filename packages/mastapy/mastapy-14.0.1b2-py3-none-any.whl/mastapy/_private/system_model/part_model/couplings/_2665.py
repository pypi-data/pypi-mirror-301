"""SpringDamper"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.couplings import _2644

_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.connections_and_sockets.couplings import _2405
    from mastapy._private.system_model.part_model import _2490, _2526, _2535

    Self = TypeVar("Self", bound="SpringDamper")
    CastSelf = TypeVar("CastSelf", bound="SpringDamper._Cast_SpringDamper")


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamper",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpringDamper:
    """Special nested class for casting SpringDamper to subclasses."""

    __parent__: "SpringDamper"

    @property
    def coupling(self: "CastSelf") -> "_2644.Coupling":
        return self.__parent__._cast(_2644.Coupling)

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
    def spring_damper(self: "CastSelf") -> "SpringDamper":
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
class SpringDamper(_2644.Coupling):
    """SpringDamper

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPRING_DAMPER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection(self: "Self") -> "_2405.SpringDamperConnection":
        """mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpringDamper":
        """Cast to another type.

        Returns:
            _Cast_SpringDamper
        """
        return _Cast_SpringDamper(self)
