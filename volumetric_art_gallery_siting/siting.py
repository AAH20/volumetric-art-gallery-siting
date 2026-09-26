"""
Volumetric Art Gallery Siting Master Facade:
Unifies 3D ray-triangle occlusion solving across mountain radar horizon siting
and industrial AOI printed circuit board camera placement.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
from typing import List, Tuple
from .core.models import Point3D, TriangleFacet, SensorSite, CoverageResult, SitingMode
from .core.art_gallery_engine import VolumetricArtGalleryEngine
from .adapters.defense import TerrainRadarSitingAdapter
from .adapters.industrial import AOIPCBOpticalAdapter


class VolumetricArtGallerySiting:
    """Master facade for 3D Art Gallery line-of-sight sensor siting."""

    def __init__(self, target_coverage_ratio: float = 0.95):
        self.engine = VolumetricArtGalleryEngine(target_coverage_ratio=target_coverage_ratio)

    def site_terrain_radars(self, seed: int = 42) -> CoverageResult:
        """Optimizes 3D radar watchtower placement across mountain terrain."""
        cands, voxels, facets = TerrainRadarSitingAdapter.generate_mountain_corridor_scenario(seed=seed)
        return self.engine.optimize_siting(cands, voxels, facets, mode=SitingMode.TACTICAL_RADAR_TERRAIN)

    def site_pcb_cameras(self, seed: int = 42) -> CoverageResult:
        """Optimizes multi-camera placement for 3D PCB Automated Optical Inspection (AOI)."""
        cands, voxels, facets = AOIPCBOpticalAdapter.generate_pcb_inspection_scenario(seed=seed)
        return self.engine.optimize_siting(cands, voxels, facets, mode=SitingMode.INDUSTRIAL_PCB_AOI)

    def optimize_custom(
        self,
        candidate_sites: List[SensorSite],
        target_voxels: List[Point3D],
        obstacle_facets: List[TriangleFacet],
        mode: SitingMode = SitingMode.TACTICAL_RADAR_TERRAIN
    ) -> CoverageResult:
        """Optimizes custom user-provided 3D geometry."""
        return self.engine.optimize_siting(candidate_sites, target_voxels, obstacle_facets, mode=mode)
