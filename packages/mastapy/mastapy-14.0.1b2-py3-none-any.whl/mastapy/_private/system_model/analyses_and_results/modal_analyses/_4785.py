"""PlanetCarrierModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4775

_PLANET_CARRIER_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "PlanetCarrierModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4712,
        _4779,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7088
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2879,
    )
    from mastapy._private.system_model.part_model import _2527

    Self = TypeVar("Self", bound="PlanetCarrierModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetCarrierModalAnalysis._Cast_PlanetCarrierModalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetCarrierModalAnalysis:
    """Special nested class for casting PlanetCarrierModalAnalysis to subclasses."""

    __parent__: "PlanetCarrierModalAnalysis"

    @property
    def mountable_component_modal_analysis(
        self: "CastSelf",
    ) -> "_4775.MountableComponentModalAnalysis":
        return self.__parent__._cast(_4775.MountableComponentModalAnalysis)

    @property
    def component_modal_analysis(self: "CastSelf") -> "_4712.ComponentModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4712,
        )

        return self.__parent__._cast(_4712.ComponentModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4779.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4779,
        )

        return self.__parent__._cast(_4779.PartModalAnalysis)

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
    def planet_carrier_modal_analysis(self: "CastSelf") -> "PlanetCarrierModalAnalysis":
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
class PlanetCarrierModalAnalysis(_4775.MountableComponentModalAnalysis):
    """PlanetCarrierModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_CARRIER_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2527.PlanetCarrier":
        """mastapy.system_model.part_model.PlanetCarrier

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7088.PlanetCarrierLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2879.PlanetCarrierSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.PlanetCarrierSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetCarrierModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PlanetCarrierModalAnalysis
        """
        return _Cast_PlanetCarrierModalAnalysis(self)
