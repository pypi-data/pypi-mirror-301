"""ConicalGearSetSteadyStateSynchronousResponseOnAShaft"""

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
    _3399,
)

_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "ConicalGearSetSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3340,
        _3345,
        _3352,
        _3357,
        _3372,
        _3374,
        _3403,
        _3407,
        _3410,
        _3413,
        _3421,
        _3440,
        _3442,
        _3449,
        _3452,
        _3470,
    )
    from mastapy._private.system_model.part_model.gears import _2583

    Self = TypeVar("Self", bound="ConicalGearSetSteadyStateSynchronousResponseOnAShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetSteadyStateSynchronousResponseOnAShaft._Cast_ConicalGearSetSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting ConicalGearSetSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "ConicalGearSetSteadyStateSynchronousResponseOnAShaft"

    @property
    def gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3399.GearSetSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3399.GearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def specialised_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3440.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3440,
        )

        return self.__parent__._cast(
            _3440.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3340.AbstractAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3340,
        )

        return self.__parent__._cast(
            _3340.AbstractAssemblySteadyStateSynchronousResponseOnAShaft
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
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3345.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3345,
        )

        return self.__parent__._cast(
            _3345.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3352.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3352,
        )

        return self.__parent__._cast(
            _3352.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3357.BevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3357,
        )

        return self.__parent__._cast(
            _3357.BevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3403.HypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3403,
        )

        return self.__parent__._cast(
            _3403.HypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3407.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3407,
        )

        return self.__parent__._cast(
            _3407.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3410.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3410,
        )

        return self.__parent__._cast(
            _3410.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3413.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3413,
        )

        return self.__parent__._cast(
            _3413.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3442.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3442,
        )

        return self.__parent__._cast(
            _3442.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3449.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3449,
        )

        return self.__parent__._cast(
            _3449.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3452.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3452,
        )

        return self.__parent__._cast(
            _3452.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3470.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3470,
        )

        return self.__parent__._cast(
            _3470.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
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
class ConicalGearSetSteadyStateSynchronousResponseOnAShaft(
    _3399.GearSetSteadyStateSynchronousResponseOnAShaft
):
    """ConicalGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2583.ConicalGearSet":
        """mastapy.system_model.part_model.gears.ConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3374.ConicalGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ConicalGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearsSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3374.ConicalGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ConicalGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalGearsSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3372.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshesSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3372.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalMeshesSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_ConicalGearSetSteadyStateSynchronousResponseOnAShaft(self)
