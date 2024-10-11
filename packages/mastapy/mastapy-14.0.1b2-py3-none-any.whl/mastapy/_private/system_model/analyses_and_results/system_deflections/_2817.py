"""CouplingHalfSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2871

_COUPLING_HALF_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CouplingHalfSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4177
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2799,
        _2802,
        _2805,
        _2820,
        _2874,
        _2876,
        _2882,
        _2888,
        _2900,
        _2910,
        _2911,
        _2912,
        _2918,
        _2920,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CouplingHalfSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfSystemDeflection._Cast_CouplingHalfSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfSystemDeflection:
    """Special nested class for casting CouplingHalfSystemDeflection to subclasses."""

    __parent__: "CouplingHalfSystemDeflection"

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2871.MountableComponentSystemDeflection":
        return self.__parent__._cast(_2871.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2802.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2802,
        )

        return self.__parent__._cast(_2802.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

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
    def clutch_half_system_deflection(
        self: "CastSelf",
    ) -> "_2799.ClutchHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2799,
        )

        return self.__parent__._cast(_2799.ClutchHalfSystemDeflection)

    @property
    def concept_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2805.ConceptCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2805,
        )

        return self.__parent__._cast(_2805.ConceptCouplingHalfSystemDeflection)

    @property
    def cvt_pulley_system_deflection(
        self: "CastSelf",
    ) -> "_2820.CVTPulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2820,
        )

        return self.__parent__._cast(_2820.CVTPulleySystemDeflection)

    @property
    def part_to_part_shear_coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "_2876.PartToPartShearCouplingHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2876,
        )

        return self.__parent__._cast(_2876.PartToPartShearCouplingHalfSystemDeflection)

    @property
    def pulley_system_deflection(self: "CastSelf") -> "_2882.PulleySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2882,
        )

        return self.__parent__._cast(_2882.PulleySystemDeflection)

    @property
    def rolling_ring_system_deflection(
        self: "CastSelf",
    ) -> "_2888.RollingRingSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2888,
        )

        return self.__parent__._cast(_2888.RollingRingSystemDeflection)

    @property
    def spring_damper_half_system_deflection(
        self: "CastSelf",
    ) -> "_2900.SpringDamperHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2900,
        )

        return self.__parent__._cast(_2900.SpringDamperHalfSystemDeflection)

    @property
    def synchroniser_half_system_deflection(
        self: "CastSelf",
    ) -> "_2910.SynchroniserHalfSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2910,
        )

        return self.__parent__._cast(_2910.SynchroniserHalfSystemDeflection)

    @property
    def synchroniser_part_system_deflection(
        self: "CastSelf",
    ) -> "_2911.SynchroniserPartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2911,
        )

        return self.__parent__._cast(_2911.SynchroniserPartSystemDeflection)

    @property
    def synchroniser_sleeve_system_deflection(
        self: "CastSelf",
    ) -> "_2912.SynchroniserSleeveSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2912,
        )

        return self.__parent__._cast(_2912.SynchroniserSleeveSystemDeflection)

    @property
    def torque_converter_pump_system_deflection(
        self: "CastSelf",
    ) -> "_2918.TorqueConverterPumpSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2918,
        )

        return self.__parent__._cast(_2918.TorqueConverterPumpSystemDeflection)

    @property
    def torque_converter_turbine_system_deflection(
        self: "CastSelf",
    ) -> "_2920.TorqueConverterTurbineSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2920,
        )

        return self.__parent__._cast(_2920.TorqueConverterTurbineSystemDeflection)

    @property
    def coupling_half_system_deflection(
        self: "CastSelf",
    ) -> "CouplingHalfSystemDeflection":
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
class CouplingHalfSystemDeflection(_2871.MountableComponentSystemDeflection):
    """CouplingHalfSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2645.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4177.CouplingHalfPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfSystemDeflection
        """
        return _Cast_CouplingHalfSystemDeflection(self)
