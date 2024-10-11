"""AGMAGleasonConicalGearMeshCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2973,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "AGMAGleasonConicalGearMeshCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2776,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2952,
        _2957,
        _2975,
        _3000,
        _3004,
        _3006,
        _3044,
        _3050,
        _3053,
        _3071,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundSystemDeflection._Cast_AGMAGleasonConicalGearMeshCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundSystemDeflection:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundSystemDeflection to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundSystemDeflection"

    @property
    def conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2973.ConicalGearMeshCompoundSystemDeflection":
        return self.__parent__._cast(_2973.ConicalGearMeshCompoundSystemDeflection)

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3000.GearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3000,
        )

        return self.__parent__._cast(_3000.GearMeshCompoundSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3006.InterMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3006,
        )

        return self.__parent__._cast(
            _3006.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2975.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2975,
        )

        return self.__parent__._cast(_2975.ConnectionCompoundSystemDeflection)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def bevel_differential_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2952.BevelDifferentialGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2952,
        )

        return self.__parent__._cast(
            _2952.BevelDifferentialGearMeshCompoundSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2957.BevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2957,
        )

        return self.__parent__._cast(_2957.BevelGearMeshCompoundSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3004.HypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3004,
        )

        return self.__parent__._cast(_3004.HypoidGearMeshCompoundSystemDeflection)

    @property
    def spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3044.SpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3044,
        )

        return self.__parent__._cast(_3044.SpiralBevelGearMeshCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3050.StraightBevelDiffGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3050,
        )

        return self.__parent__._cast(
            _3050.StraightBevelDiffGearMeshCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3053.StraightBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3053,
        )

        return self.__parent__._cast(
            _3053.StraightBevelGearMeshCompoundSystemDeflection
        )

    @property
    def zerol_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3071.ZerolBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3071,
        )

        return self.__parent__._cast(_3071.ZerolBevelGearMeshCompoundSystemDeflection)

    @property
    def agma_gleason_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundSystemDeflection":
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
class AGMAGleasonConicalGearMeshCompoundSystemDeflection(
    _2973.ConicalGearMeshCompoundSystemDeflection
):
    """AGMAGleasonConicalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2776.AGMAGleasonConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2776.AGMAGleasonConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundSystemDeflection
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundSystemDeflection(self)
