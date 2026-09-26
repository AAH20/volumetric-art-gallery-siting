"""
Volumetric Art Gallery Siting:
Dual-Use 3D Radar Horizon Siting & PCB AOI Camera Placement Engine.
Zero external dependencies (pure Python standard library).
"""

from .core.models import (
    Point3D,
    TriangleFacet,
    SensorSite,
    CoverageResult,
    SitingMode
)
from .core.art_gallery_engine import VolumetricArtGalleryEngine
from .adapters.defense import TerrainRadarSitingAdapter
from .adapters.industrial import AOIPCBOpticalAdapter
from .siting import VolumetricArtGallerySiting

__all__ = [
    "Point3D",
    "TriangleFacet",
    "SensorSite",
    "CoverageResult",
    "SitingMode",
    "VolumetricArtGalleryEngine",
    "TerrainRadarSitingAdapter",
    "AOIPCBOpticalAdapter",
    "VolumetricArtGallerySiting"
]

__version__ = "1.0.0"
