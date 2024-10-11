"""SteadyStateSynchronousResponseAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2707

_STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults",
    "SteadyStateSynchronousResponseAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7725

    Self = TypeVar("Self", bound="SteadyStateSynchronousResponseAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SteadyStateSynchronousResponseAnalysis._Cast_SteadyStateSynchronousResponseAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SteadyStateSynchronousResponseAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SteadyStateSynchronousResponseAnalysis:
    """Special nested class for casting SteadyStateSynchronousResponseAnalysis to subclasses."""

    __parent__: "SteadyStateSynchronousResponseAnalysis"

    @property
    def single_analysis(self: "CastSelf") -> "_2707.SingleAnalysis":
        return self.__parent__._cast(_2707.SingleAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7725.MarshalByRefObjectPermanent":
        from mastapy._private import _7725

        return self.__parent__._cast(_7725.MarshalByRefObjectPermanent)

    @property
    def steady_state_synchronous_response_analysis(
        self: "CastSelf",
    ) -> "SteadyStateSynchronousResponseAnalysis":
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
class SteadyStateSynchronousResponseAnalysis(_2707.SingleAnalysis):
    """SteadyStateSynchronousResponseAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STEADY_STATE_SYNCHRONOUS_RESPONSE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SteadyStateSynchronousResponseAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SteadyStateSynchronousResponseAnalysis
        """
        return _Cast_SteadyStateSynchronousResponseAnalysis(self)
