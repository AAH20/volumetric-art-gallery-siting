"""
Terrain Radar Siting Adapter:
Generates 3D digital elevation models (DEM) with mountainous ridgelines,
valley penetration corridors, and candidate radar watchtower locations.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import random
from typing import List, Tuple
from ..core.models import Point3D, TriangleFacet, SensorSite


class TerrainRadarSitingAdapter:
    """Simulates 3D mountain topography and radar siting optimization."""

    @staticmethod
    def generate_mountain_corridor_scenario(
        seed: int = 42
    ) -> Tuple[List[SensorSite], List[Point3D], List[TriangleFacet]]:
        """
        Creates a mountain valley corridor where low-flying cruise missiles penetrate.
        Returns: (candidate_radar_sites, low_altitude_airspace_voxels, mountain_facets)
        """
        rng = random.Random(seed)

        # 1. Mountain Ridge Obstacles (Two non-convex mountain pyramids blocking line-of-sight)
        # Peak 1 at (0, 0, 1200m)
        p1_top = (0.0, 0.0, 1200.0)
        p1_b1 = (-3000.0, -3000.0, 0.0)
        p1_b2 = (3000.0, -3000.0, 0.0)
        p1_b3 = (3000.0, 3000.0, 0.0)
        p1_b4 = (-3000.0, 3000.0, 0.0)

        # Peak 2 at (6000, 2000, 1400m)
        p2_top = (6000.0, 2000.0, 1400.0)
        p2_b1 = (4000.0, 0.0, 0.0)
        p2_b2 = (8000.0, 0.0, 0.0)
        p2_b3 = (8000.0, 4000.0, 0.0)
        p2_b4 = (4000.0, 4000.0, 0.0)

        facets = [
            TriangleFacet(p1_b1, p1_b2, p1_top),
            TriangleFacet(p1_b2, p1_b3, p1_top),
            TriangleFacet(p1_b3, p1_b4, p1_top),
            TriangleFacet(p1_b4, p1_b1, p1_top),
            TriangleFacet(p2_b1, p2_b2, p2_top),
            TriangleFacet(p2_b2, p2_b3, p2_top),
            TriangleFacet(p2_b3, p2_b4, p2_top),
            TriangleFacet(p2_b4, p2_b1, p2_top),
        ]

        # 2. Airspace Corridor Voxels to Protect (Low altitude: 50m - 300m AGL)
        target_voxels: List[Point3D] = []
        for x in range(-5000, 10000, 1500):
            for y in range(-5000, 6000, 1500):
                target_voxels.append((float(x), float(y), 150.0))

        # 3. Candidate Radar Watchtower Sites (Perimeter & Ridge positions)
        candidate_sites = [
            SensorSite(site_id="RADAR-MAST-NORTH", position=(-4000.0, 5000.0, 600.0), max_range=20000.0, installation_cost=1.5),
            SensorSite(site_id="RADAR-MAST-SOUTH", position=(-4000.0, -5000.0, 550.0), max_range=20000.0, installation_cost=1.2),
            SensorSite(site_id="RADAR-PEAK-ALPHA", position=(-200.0, 500.0, 1250.0), max_range=25000.0, installation_cost=3.0),
            SensorSite(site_id="RADAR-PEAK-BRAVO", position=(6100.0, 2100.0, 1450.0), max_range=25000.0, installation_cost=3.5),
            SensorSite(site_id="RADAR-VALLEY-EAST", position=(9000.0, 1000.0, 300.0), max_range=18000.0, installation_cost=1.0),
            SensorSite(site_id="RADAR-WEST-CORRIDOR", position=(-6000.0, 0.0, 400.0), max_range=18000.0, installation_cost=1.0),
        ]

        return candidate_sites, target_voxels, facets
