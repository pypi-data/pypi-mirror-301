"""WormGearSetCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4905,
)

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "WormGearSetCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4829
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4845,
        _4926,
        _4945,
        _4970,
        _4971,
    )
    from mastapy._private.system_model.part_model.gears import _2611

    Self = TypeVar("Self", bound="WormGearSetCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGearSetCompoundModalAnalysis._Cast_WormGearSetCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetCompoundModalAnalysis:
    """Special nested class for casting WormGearSetCompoundModalAnalysis to subclasses."""

    __parent__: "WormGearSetCompoundModalAnalysis"

    @property
    def gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4905.GearSetCompoundModalAnalysis":
        return self.__parent__._cast(_4905.GearSetCompoundModalAnalysis)

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4945.SpecialisedAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4945,
        )

        return self.__parent__._cast(_4945.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4845.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4845,
        )

        return self.__parent__._cast(_4845.AbstractAssemblyCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.PartCompoundModalAnalysis)

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
    def worm_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "WormGearSetCompoundModalAnalysis":
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
class WormGearSetCompoundModalAnalysis(_4905.GearSetCompoundModalAnalysis):
    """WormGearSetCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2611.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2611.WormGearSet":
        """mastapy.system_model.part_model.gears.WormGearSet

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
    ) -> "List[_4829.WormGearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis]

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
    def worm_gears_compound_modal_analysis(
        self: "Self",
    ) -> "List[_4970.WormGearCompoundModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearCompoundModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearsCompoundModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_meshes_compound_modal_analysis(
        self: "Self",
    ) -> "List[_4971.WormGearMeshCompoundModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.compound.WormGearMeshCompoundModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshesCompoundModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4829.WormGearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.WormGearSetModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_WormGearSetCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetCompoundModalAnalysis
        """
        return _Cast_WormGearSetCompoundModalAnalysis(self)
