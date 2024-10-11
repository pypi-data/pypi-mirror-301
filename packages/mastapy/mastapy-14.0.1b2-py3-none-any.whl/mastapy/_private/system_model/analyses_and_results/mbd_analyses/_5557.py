"""CylindricalPlanetGearMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5555

_CYLINDRICAL_PLANET_GEAR_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "CylindricalPlanetGearMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7721,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5532,
        _5567,
        _5594,
        _5597,
    )
    from mastapy._private.system_model.part_model.gears import _2586

    Self = TypeVar("Self", bound="CylindricalPlanetGearMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearMultibodyDynamicsAnalysis._Cast_CylindricalPlanetGearMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearMultibodyDynamicsAnalysis:
    """Special nested class for casting CylindricalPlanetGearMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CylindricalPlanetGearMultibodyDynamicsAnalysis"

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5555.CylindricalGearMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5555.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5567.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5567,
        )

        return self.__parent__._cast(_5567.GearMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(_5597.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7721.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartTimeSeriesLoadAnalysisCase)

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
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearMultibodyDynamicsAnalysis":
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
class CylindricalPlanetGearMultibodyDynamicsAnalysis(
    _5555.CylindricalGearMultibodyDynamicsAnalysis
):
    """CylindricalPlanetGearMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2586.CylindricalPlanetGear":
        """mastapy.system_model.part_model.gears.CylindricalPlanetGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGearMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearMultibodyDynamicsAnalysis
        """
        return _Cast_CylindricalPlanetGearMultibodyDynamicsAnalysis(self)
