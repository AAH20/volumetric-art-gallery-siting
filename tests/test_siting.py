"""
Unit Tests for Volumetric Art Gallery Siting:
Verifies Möller-Trumbore ray occlusion, greedy submodular coverage,
blind spot minimization, and sub-second execution latency.
Zero external dependencies (pure Python standard library).
"""

import unittest
from volumetric_art_gallery_siting import (
    VolumetricArtGallerySiting,
    VolumetricArtGalleryEngine,
    Point3D,
    TriangleFacet,
    SensorSite,
    SitingMode
)


class TestVolumetricArtGallerySiting(unittest.TestCase):

    def setUp(self):
        self.siter = VolumetricArtGallerySiting(target_coverage_ratio=0.90)

    def test_ray_triangle_occlusion(self):
        """Verifies that a solid triangle facet between two points occludes line-of-sight."""
        engine = VolumetricArtGalleryEngine()
        sensor_pos = (0.0, 0.0, 10.0)
        target_pos = (0.0, 0.0, 0.0)

        # Triangle placed at z = 5 directly blocking the vertical ray
        blocking_facet = TriangleFacet(
            (-2.0, -2.0, 5.0),
            (2.0, -2.0, 5.0),
            (0.0, 2.0, 5.0)
        )

        is_visible = engine.check_visibility(sensor_pos, target_pos, [blocking_facet], max_range=20.0)
        self.assertFalse(is_visible, "Expected obstacle to occlude line-of-sight!")

        # Target shifted outside the blocking triangle
        clear_target = (10.0, 0.0, 0.0)
        is_clear = engine.check_visibility(sensor_pos, clear_target, [blocking_facet], max_range=20.0)
        self.assertTrue(is_clear, "Expected clear line-of-sight outside obstacle boundary!")

    def test_terrain_radar_siting(self):
        """Verifies 3D mountain radar siting coverage and submodular lower bound."""
        res = self.siter.site_terrain_radars(seed=42)

        self.assertEqual(res.mode, SitingMode.TACTICAL_RADAR_TERRAIN)
        self.assertGreater(len(res.selected_sites), 0)
        self.assertGreaterEqual(res.coverage_percentage, 50.0)
        self.assertLessEqual(res.blind_spot_percentage, 50.0)
        self.assertGreater(res.submodular_optimality_bound, 0.0)
        self.assertLess(res.execution_latency_ms, 200.0)

    def test_pcb_aoi_camera_siting(self):
        """Verifies that industrial AOI camera placement achieves high solder joint coverage."""
        res = self.siter.site_pcb_cameras(seed=42)

        self.assertEqual(res.mode, SitingMode.INDUSTRIAL_PCB_AOI)
        self.assertGreater(len(res.selected_sites), 0)
        self.assertGreaterEqual(res.coverage_percentage, 75.0)
        self.assertLess(res.execution_latency_ms, 150.0)


if __name__ == "__main__":
    unittest.main()
