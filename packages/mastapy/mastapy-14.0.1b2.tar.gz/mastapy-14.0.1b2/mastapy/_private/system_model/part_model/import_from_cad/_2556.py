"""ConnectorFromCAD"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.import_from_cad import _2563

_CONNECTOR_FROM_CAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD", "ConnectorFromCAD"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model.import_from_cad import (
        _2554,
        _2555,
        _2562,
        _2566,
        _2567,
    )

    Self = TypeVar("Self", bound="ConnectorFromCAD")
    CastSelf = TypeVar("CastSelf", bound="ConnectorFromCAD._Cast_ConnectorFromCAD")


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorFromCAD",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorFromCAD:
    """Special nested class for casting ConnectorFromCAD to subclasses."""

    __parent__: "ConnectorFromCAD"

    @property
    def mountable_component_from_cad(
        self: "CastSelf",
    ) -> "_2563.MountableComponentFromCAD":
        return self.__parent__._cast(_2563.MountableComponentFromCAD)

    @property
    def component_from_cad(self: "CastSelf") -> "_2554.ComponentFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2554

        return self.__parent__._cast(_2554.ComponentFromCAD)

    @property
    def concept_bearing_from_cad(self: "CastSelf") -> "_2555.ConceptBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2555

        return self.__parent__._cast(_2555.ConceptBearingFromCAD)

    @property
    def rigid_connector_from_cad(self: "CastSelf") -> "_2566.RigidConnectorFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2566

        return self.__parent__._cast(_2566.RigidConnectorFromCAD)

    @property
    def rolling_bearing_from_cad(self: "CastSelf") -> "_2567.RollingBearingFromCAD":
        from mastapy._private.system_model.part_model.import_from_cad import _2567

        return self.__parent__._cast(_2567.RollingBearingFromCAD)

    @property
    def connector_from_cad(self: "CastSelf") -> "ConnectorFromCAD":
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
class ConnectorFromCAD(_2563.MountableComponentFromCAD):
    """ConnectorFromCAD

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_FROM_CAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mounting(self: "Self") -> "_2562.HousedOrMounted":
        """mastapy.system_model.part_model.import_from_cad.HousedOrMounted"""
        temp = pythonnet_property_get(self.wrapped, "Mounting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD.HousedOrMounted"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.part_model.import_from_cad._2562",
            "HousedOrMounted",
        )(value)

    @mounting.setter
    @enforce_parameter_types
    def mounting(self: "Self", value: "_2562.HousedOrMounted") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD.HousedOrMounted"
        )
        pythonnet_property_set(self.wrapped, "Mounting", value)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorFromCAD":
        """Cast to another type.

        Returns:
            _Cast_ConnectorFromCAD
        """
        return _Cast_ConnectorFromCAD(self)
