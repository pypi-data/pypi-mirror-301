"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2255 import Design
    from mastapy._private.system_model._2256 import ComponentDampingOption
    from mastapy._private.system_model._2257 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2258 import DesignEntity
    from mastapy._private.system_model._2259 import DesignEntityId
    from mastapy._private.system_model._2260 import DesignSettings
    from mastapy._private.system_model._2261 import DutyCycleImporter
    from mastapy._private.system_model._2262 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2263 import ExternalFullFELoader
    from mastapy._private.system_model._2264 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2265 import IncludeDutyCycleOption
    from mastapy._private.system_model._2266 import MAAElectricMachineGroup
    from mastapy._private.system_model._2267 import MASTASettings
    from mastapy._private.system_model._2268 import MemorySummary
    from mastapy._private.system_model._2269 import MeshStiffnessModel
    from mastapy._private.system_model._2270 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2271 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2272 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2273 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2274 import PowerLoadType
    from mastapy._private.system_model._2275 import RelativeComponentAlignment
    from mastapy._private.system_model._2276 import RelativeOffsetOption
    from mastapy._private.system_model._2277 import SystemReporting
    from mastapy._private.system_model._2278 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2279 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2255": ["Design"],
        "_private.system_model._2256": ["ComponentDampingOption"],
        "_private.system_model._2257": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2258": ["DesignEntity"],
        "_private.system_model._2259": ["DesignEntityId"],
        "_private.system_model._2260": ["DesignSettings"],
        "_private.system_model._2261": ["DutyCycleImporter"],
        "_private.system_model._2262": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2263": ["ExternalFullFELoader"],
        "_private.system_model._2264": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2265": ["IncludeDutyCycleOption"],
        "_private.system_model._2266": ["MAAElectricMachineGroup"],
        "_private.system_model._2267": ["MASTASettings"],
        "_private.system_model._2268": ["MemorySummary"],
        "_private.system_model._2269": ["MeshStiffnessModel"],
        "_private.system_model._2270": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2271": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2272": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2273": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2274": ["PowerLoadType"],
        "_private.system_model._2275": ["RelativeComponentAlignment"],
        "_private.system_model._2276": ["RelativeOffsetOption"],
        "_private.system_model._2277": ["SystemReporting"],
        "_private.system_model._2278": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2279": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
