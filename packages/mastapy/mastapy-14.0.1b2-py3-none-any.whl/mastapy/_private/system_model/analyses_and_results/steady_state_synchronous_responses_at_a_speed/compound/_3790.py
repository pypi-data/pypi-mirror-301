"""FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3795,
)

_FACE_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3657,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3735,
        _3788,
        _3789,
        _3816,
        _3835,
    )
    from mastapy._private.system_model.part_model.gears import _2588

    Self = TypeVar(
        "Self", bound="FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed._Cast_FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3795.GearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3795.GearSetCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def specialised_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3835.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3835,
        )

        return self.__parent__._cast(
            _3835.SpecialisedAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_assembly_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3735.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3735,
        )

        return self.__parent__._cast(
            _3735.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3816.PartCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3816,
        )

        return self.__parent__._cast(
            _3816.PartCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7715.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def face_gear_set_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
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
class FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed(
    _3795.GearSetCompoundSteadyStateSynchronousResponseAtASpeed
):
    """FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _FACE_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2588.FaceGearSet":
        """mastapy.system_model.part_model.gears.FaceGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2588.FaceGearSet":
        """mastapy.system_model.part_model.gears.FaceGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3657.FaceGearSetSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.FaceGearSetSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_gears_compound_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3788.FaceGearCompoundSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound.FaceGearCompoundSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceGearsCompoundSteadyStateSynchronousResponseAtASpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_meshes_compound_steady_state_synchronous_response_at_a_speed(
        self: "Self",
    ) -> "List[_3789.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FaceMeshesCompoundSteadyStateSynchronousResponseAtASpeed"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3657.FaceGearSetSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.FaceGearSetSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed(self)
