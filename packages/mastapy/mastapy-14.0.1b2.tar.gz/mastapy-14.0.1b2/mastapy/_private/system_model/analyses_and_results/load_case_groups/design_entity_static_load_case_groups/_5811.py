"""PartStaticLoadCaseGroup"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
    _5809,
)

_PART_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "PartStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5806,
        _5807,
        _5810,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7081
    from mastapy._private.system_model.part_model import _2526

    Self = TypeVar("Self", bound="PartStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="PartStaticLoadCaseGroup._Cast_PartStaticLoadCaseGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartStaticLoadCaseGroup:
    """Special nested class for casting PartStaticLoadCaseGroup to subclasses."""

    __parent__: "PartStaticLoadCaseGroup"

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "_5809.DesignEntityStaticLoadCaseGroup":
        return self.__parent__._cast(_5809.DesignEntityStaticLoadCaseGroup)

    @property
    def abstract_assembly_static_load_case_group(
        self: "CastSelf",
    ) -> "_5806.AbstractAssemblyStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5806,
        )

        return self.__parent__._cast(_5806.AbstractAssemblyStaticLoadCaseGroup)

    @property
    def component_static_load_case_group(
        self: "CastSelf",
    ) -> "_5807.ComponentStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5807,
        )

        return self.__parent__._cast(_5807.ComponentStaticLoadCaseGroup)

    @property
    def gear_set_static_load_case_group(
        self: "CastSelf",
    ) -> "_5810.GearSetStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5810,
        )

        return self.__parent__._cast(_5810.GearSetStaticLoadCaseGroup)

    @property
    def part_static_load_case_group(self: "CastSelf") -> "PartStaticLoadCaseGroup":
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
class PartStaticLoadCaseGroup(_5809.DesignEntityStaticLoadCaseGroup):
    """PartStaticLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def part(self: "Self") -> "_2526.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def part_load_cases(self: "Self") -> "List[_7081.PartLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PartLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def clear_user_specified_excitation_data_for_all_load_cases(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForAllLoadCases"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_PartStaticLoadCaseGroup
        """
        return _Cast_PartStaticLoadCaseGroup(self)
