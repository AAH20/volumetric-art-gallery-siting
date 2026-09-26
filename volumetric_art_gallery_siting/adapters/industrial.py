"""
Industrial AOI (Automated Optical Inspection) PCB Camera Siting Adapter:
Generates 3D CAD geometries of dense printed circuit boards with tall capacitors,
shield cans, and solder joints requiring non-occluded camera angles.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import random
from typing import List, Tuple
from ..core.models import Point3D, TriangleFacet, SensorSite


class AOIPCBOpticalAdapter:
    """Simulates 3D Automated Optical Inspection (AOI) camera placement."""

    @staticmethod
    def generate_pcb_inspection_scenario(
        seed: int = 42
    ) -> Tuple[List[SensorSite], List[Point3D], List[TriangleFacet]]:
        """
        Creates a high-density PCB inspection chamber scenario.
        Returns: (candidate_cameras, critical_solder_joints, component_facets)
        """
        rng = random.Random(seed)

        # 1. 3D Obstacle Facets: High-Profile BGA & Shield Can (millimeter scale)
        # BGA processor box at center: (0, 0, 15mm tall)
        bga_top = (0.0, 0.0, 15.0)
        b1 = (-25.0, -25.0, 0.0)
        b2 = (25.0, -25.0, 0.0)
        b3 = (25.0, 25.0, 0.0)
        b4 = (-25.0, 25.0, 0.0)

        # Electrolytic Capacitor block at (50, 40, 25mm tall)
        cap_top = (50.0, 40.0, 25.0)
        c1 = (40.0, 30.0, 0.0)
        c2 = (60.0, 30.0, 0.0)
        c3 = (60.0, 50.0, 0.0)
        c4 = (40.0, 50.0, 0.0)

        facets = [
            TriangleFacet(b1, b2, bga_top),
            TriangleFacet(b2, b3, bga_top),
            TriangleFacet(b3, b4, bga_top),
            TriangleFacet(b4, b1, bga_top),
            TriangleFacet(c1, c2, cap_top),
            TriangleFacet(c2, c3, cap_top),
            TriangleFacet(c3, c4, cap_top),
            TriangleFacet(c4, c1, cap_top)
        ]

        # 2. Critical Solder Joints requiring line-of-sight inspection
        solder_joints: List[Point3D] = []
        for x in range(-60, 80, 15):
            for y in range(-60, 80, 15):
                solder_joints.append((float(x), float(y), 0.5))

        # 3. Candidate AOI Camera Mounts (Overhead gantry & angled oblique mounts)
        candidate_cameras = [
            SensorSite(site_id="CAM-OVERHEAD-TOP", position=(0.0, 0.0, 120.0), max_range=200.0, installation_cost=2.0),
            SensorSite(site_id="CAM-OBLIQUE-NORTH", position=(0.0, 90.0, 70.0), max_range=200.0, installation_cost=1.2),
            SensorSite(site_id="CAM-OBLIQUE-SOUTH", position=(0.0, -90.0, 70.0), max_range=200.0, installation_cost=1.2),
            SensorSite(site_id="CAM-OBLIQUE-EAST", position=(90.0, 0.0, 70.0), max_range=200.0, installation_cost=1.2),
            SensorSite(site_id="CAM-OBLIQUE-WEST", position=(-90.0, 0.0, 70.0), max_range=200.0, installation_cost=1.2),
        ]

        return candidate_cameras, solder_joints, facets
