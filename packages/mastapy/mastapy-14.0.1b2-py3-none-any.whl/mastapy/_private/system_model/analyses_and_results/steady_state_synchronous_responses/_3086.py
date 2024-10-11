"""BevelDifferentialGearSetSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3091,
)

_BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "BevelDifferentialGearSetSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6975
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3074,
        _3079,
        _3085,
        _3087,
        _3107,
        _3134,
        _3156,
        _3175,
    )
    from mastapy._private.system_model.part_model.gears import _2575

    Self = TypeVar(
        "Self", bound="BevelDifferentialGearSetSteadyStateSynchronousResponse"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearSetSteadyStateSynchronousResponse._Cast_BevelDifferentialGearSetSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearSetSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearSetSteadyStateSynchronousResponse:
    """Special nested class for casting BevelDifferentialGearSetSteadyStateSynchronousResponse to subclasses."""

    __parent__: "BevelDifferentialGearSetSteadyStateSynchronousResponse"

    @property
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3091.BevelGearSetSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3091.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3079.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3079,
        )

        return self.__parent__._cast(
            _3079.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3107.ConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3107,
        )

        return self.__parent__._cast(_3107.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3134.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3134,
        )

        return self.__parent__._cast(_3134.GearSetSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3175.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3175,
        )

        return self.__parent__._cast(
            _3175.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3074.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3074,
        )

        return self.__parent__._cast(
            _3074.AbstractAssemblySteadyStateSynchronousResponse
        )

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3156.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3156,
        )

        return self.__parent__._cast(_3156.PartSteadyStateSynchronousResponse)

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
    def bevel_differential_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "BevelDifferentialGearSetSteadyStateSynchronousResponse":
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
class BevelDifferentialGearSetSteadyStateSynchronousResponse(
    _3091.BevelGearSetSteadyStateSynchronousResponse
):
    """BevelDifferentialGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_DIFFERENTIAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2575.BevelDifferentialGearSet":
        """mastapy.system_model.part_model.gears.BevelDifferentialGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_6975.BevelDifferentialGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3087.BevelDifferentialGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.BevelDifferentialGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3087.BevelDifferentialGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.BevelDifferentialGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelDifferentialGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3085.BevelDifferentialGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.BevelDifferentialGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3085.BevelDifferentialGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.BevelDifferentialGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelDifferentialMeshesSteadyStateSynchronousResponse"
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
    ) -> "_Cast_BevelDifferentialGearSetSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearSetSteadyStateSynchronousResponse
        """
        return _Cast_BevelDifferentialGearSetSteadyStateSynchronousResponse(self)
