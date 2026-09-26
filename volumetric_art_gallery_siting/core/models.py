"""
Data Models for Volumetric Art Gallery Siting:
Defines 3D points, obstacle facets, sensor candidate sites, and coverage outcomes.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class SitingMode(str, Enum):
    TACTICAL_RADAR_TERRAIN = "TACTICAL_RADAR_TERRAIN"
    INDUSTRIAL_PCB_AOI = "INDUSTRIAL_PCB_AOI"


Point3D = Tuple[float, float, float]


@dataclass
class TriangleFacet:
    """3D Obstacle facet (terrain mesh polygon or PCB component face)."""
    v0: Point3D
    v1: Point3D
    v2: Point3D


@dataclass
class SensorSite:
    """Candidate radar tower or optical camera installation point."""
    site_id: str
    position: Point3D
    max_range: float
    field_of_view_deg: float = 360.0
    installation_cost: float = 1.0


@dataclass
class CoverageResult:
    """Outcome of volumetric 3D Art Gallery optimization."""
    mode: SitingMode
    selected_sites: List[str]
    total_candidate_sites: int
    covered_voxels_count: int
    total_voxels_count: int
    coverage_percentage: float
    blind_spot_percentage: float
    total_installation_cost: float
    execution_latency_ms: float
    submodular_optimality_bound: float
    metrics: Dict[str, float] = field(default_factory=dict)
