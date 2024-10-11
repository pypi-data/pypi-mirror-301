"""ConnectorModalAnalysis"""

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

_CONNECTOR_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ConnectorModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4695,
        _4712,
        _4777,
        _4779,
        _4795,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2815,
    )
    from mastapy._private.system_model.part_model import _2503

    Self = TypeVar("Self", bound="ConnectorModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectorModalAnalysis._Cast_ConnectorModalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorModalAnalysis:
    """Special nested class for casting ConnectorModalAnalysis to subclasses."""

    __parent__: "ConnectorModalAnalysis"

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
    def bearing_modal_analysis(self: "CastSelf") -> "_4695.BearingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4695,
        )

        return self.__parent__._cast(_4695.BearingModalAnalysis)

    @property
    def oil_seal_modal_analysis(self: "CastSelf") -> "_4777.OilSealModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4777,
        )

        return self.__parent__._cast(_4777.OilSealModalAnalysis)

    @property
    def shaft_hub_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4795.ShaftHubConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4795,
        )

        return self.__parent__._cast(_4795.ShaftHubConnectionModalAnalysis)

    @property
    def connector_modal_analysis(self: "CastSelf") -> "ConnectorModalAnalysis":
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
class ConnectorModalAnalysis(_4775.MountableComponentModalAnalysis):
    """ConnectorModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2503.Connector":
        """mastapy.system_model.part_model.Connector

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2815.ConnectorSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConnectorSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectorModalAnalysis
        """
        return _Cast_ConnectorModalAnalysis(self)
