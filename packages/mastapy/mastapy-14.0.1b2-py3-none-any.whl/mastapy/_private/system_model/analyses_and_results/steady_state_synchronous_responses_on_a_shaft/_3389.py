"""CylindricalGearSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3400,
)

_CYLINDRICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "CylindricalGearSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7012
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3365,
        _3390,
        _3419,
        _3421,
    )
    from mastapy._private.system_model.part_model.gears import _2584

    Self = TypeVar(
        "Self", bound="CylindricalGearSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSteadyStateSynchronousResponseOnAShaft._Cast_CylindricalGearSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting CylindricalGearSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "CylindricalGearSteadyStateSynchronousResponseOnAShaft"

    @property
    def gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3400.GearSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(_3400.GearSteadyStateSynchronousResponseOnAShaft)

    @property
    def mountable_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3419.MountableComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3419,
        )

        return self.__parent__._cast(
            _3419.MountableComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3365.ComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3365,
        )

        return self.__parent__._cast(
            _3365.ComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3421.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3421,
        )

        return self.__parent__._cast(_3421.PartSteadyStateSynchronousResponseOnAShaft)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

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
    def cylindrical_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3390.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3390,
        )

        return self.__parent__._cast(
            _3390.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "CylindricalGearSteadyStateSynchronousResponseOnAShaft":
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
class CylindricalGearSteadyStateSynchronousResponseOnAShaft(
    _3400.GearSteadyStateSynchronousResponseOnAShaft
):
    """CylindricalGearSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYLINDRICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def component_load_case(self: "Self") -> "_7012.CylindricalGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(
        self: "Self",
    ) -> "List[CylindricalGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.CylindricalGearSteadyStateSynchronousResponseOnAShaft]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_CylindricalGearSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_CylindricalGearSteadyStateSynchronousResponseOnAShaft(self)
