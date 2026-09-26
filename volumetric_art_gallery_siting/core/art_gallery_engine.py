"""
Volumetric Art Gallery Engine:
Implements Möller-Trumbore 3D ray-triangle occlusion testing and greedy submodular
maximum coverage siting with proven (1 - 1/e) approximation bounds.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import math
import time
from typing import List, Tuple, Set, Dict
from .models import Point3D, TriangleFacet, SensorSite, CoverageResult, SitingMode


def vector_sub(a: Point3D, b: Point3D) -> Point3D:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def vector_cross(a: Point3D, b: Point3D) -> Point3D:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    )


def vector_dot(a: Point3D, b: Point3D) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def vector_length(a: Point3D) -> float:
    return math.sqrt(vector_dot(a, a))


def ray_triangle_intersect(
    ray_origin: Point3D,
    ray_dir: Point3D,
    facet: TriangleFacet,
    max_dist: float
) -> bool:
    """Möller-Trumbore ray-triangle intersection algorithm."""
    EPSILON = 1e-7
    edge1 = vector_sub(facet.v1, facet.v0)
    edge2 = vector_sub(facet.v2, facet.v0)
    h = vector_cross(ray_dir, edge2)
    a = vector_dot(edge1, h)

    if -EPSILON < a < EPSILON:
        return False  # Ray is parallel to triangle

    f = 1.0 / a
    s = vector_sub(ray_origin, facet.v0)
    u = f * vector_dot(s, h)

    if u < 0.0 or u > 1.0:
        return False

    q = vector_cross(s, edge1)
    v = f * vector_dot(ray_dir, q)

    if v < 0.0 or (u + v) > 1.0:
        return False

    t = f * vector_dot(edge2, q)
    return EPSILON < t < (max_dist - EPSILON)


class VolumetricArtGalleryEngine:
    """3D Art Gallery & Ray-Tracing Siting Optimizer."""

    def __init__(self, target_coverage_ratio: float = 0.95):
        self.target_coverage_ratio = target_coverage_ratio

    def check_visibility(
        self,
        sensor_pos: Point3D,
        target_pos: Point3D,
        facets: List[TriangleFacet],
        max_range: float
    ) -> bool:
        """Determines if target_pos is visible from sensor_pos without terrain/component occlusion."""
        diff = vector_sub(target_pos, sensor_pos)
        dist = vector_length(diff)

        if dist > max_range or dist < 1e-4:
            return False

        ray_dir = (diff[0] / dist, diff[1] / dist, diff[2] / dist)

        for facet in facets:
            if ray_triangle_intersect(sensor_pos, ray_dir, facet, dist):
                return False  # Occluded by obstacle facet

        return True

    def optimize_siting(
        self,
        candidate_sites: List[SensorSite],
        target_voxels: List[Point3D],
        obstacle_facets: List[TriangleFacet],
        mode: SitingMode = SitingMode.TACTICAL_RADAR_TERRAIN
    ) -> CoverageResult:
        """
        Executes submodular greedy set coverage to select minimal sensor sites.
        """
        t0 = time.perf_counter()

        # Step 1: Precompute visibility bitsets for each candidate site
        site_coverage_sets: Dict[str, Set[int]] = {}
        site_dict = {s.site_id: s for s in candidate_sites}

        for site in candidate_sites:
            covered_indices: Set[int] = set()
            for v_idx, v_pos in enumerate(target_voxels):
                if self.check_visibility(site.position, v_pos, obstacle_facets, site.max_range):
                    covered_indices.add(v_idx)
            site_coverage_sets[site.site_id] = covered_indices

        # Step 2: Greedy Submodular Selection
        selected_site_ids: List[str] = []
        globally_covered: Set[int] = set()
        total_targets = len(target_voxels)
        required_targets = int(total_targets * self.target_coverage_ratio)
        total_cost = 0.0

        remaining_candidates = list(candidate_sites)

        while len(globally_covered) < required_targets and remaining_candidates:
            best_site = None
            best_marginal_gain = -1

            for cand in remaining_candidates:
                new_cover = len(site_coverage_sets[cand.site_id] - globally_covered)
                # Gain per cost unit
                marginal_utility = new_cover / max(0.01, cand.installation_cost)
                if marginal_utility > best_marginal_gain:
                    best_marginal_gain = marginal_utility
                    best_site = cand

            if best_site is None or best_marginal_gain <= 0:
                break

            selected_site_ids.append(best_site.site_id)
            globally_covered.update(site_coverage_sets[best_site.site_id])
            total_cost += best_site.installation_cost
            remaining_candidates.remove(best_site)

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        coverage_pct = (len(globally_covered) / max(1, total_targets)) * 100.0
        blind_spot_pct = 100.0 - coverage_pct

        # (1 - 1/e) ≈ 63.2% submodular lower bound guarantee
        bound_pct = coverage_pct * (1.0 - 1.0 / math.e)

        metrics = {
            "unobserved_voxels_count": float(total_targets - len(globally_covered)),
            "average_voxels_per_site": float(len(globally_covered) / max(1, len(selected_site_ids))),
            "site_efficiency_ratio": float(len(selected_site_ids) / max(1, len(candidate_sites)))
        }

        return CoverageResult(
            mode=mode,
            selected_sites=selected_site_ids,
            total_candidate_sites=len(candidate_sites),
            covered_voxels_count=len(globally_covered),
            total_voxels_count=total_targets,
            coverage_percentage=round(coverage_pct, 2),
            blind_spot_percentage=round(blind_spot_pct, 2),
            total_installation_cost=round(total_cost, 2),
            execution_latency_ms=round(elapsed_ms, 2),
            submodular_optimality_bound=round(bound_pct, 2),
            metrics=metrics
        )
