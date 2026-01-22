from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JenisKegiatanViewSet, StatusKegiatanViewSet, KegiatanViewSet,
    FotoKegiatanViewSet, VolunteerViewSet, ResepViewSet,
    BahanResepViewSet, StepsResepViewSet, TipsResepViewSet,
    NutrisiResepViewSet, FotoResepViewSet, TipeTransaksiViewSet,
    TransaksiViewSet, PengurusViewSet, FotoPengurusViewSet
)
from .upload_views import upload_to_s3

router = DefaultRouter()
router.register(r'jenis-kegiatan', JenisKegiatanViewSet, basename='jenis-kegiatan')
router.register(r'status-kegiatan', StatusKegiatanViewSet, basename='status-kegiatan')
router.register(r'kegiatan', KegiatanViewSet, basename='kegiatan')
router.register(r'foto-kegiatan', FotoKegiatanViewSet, basename='foto-kegiatan')
router.register(r'volunteer', VolunteerViewSet, basename='volunteer')
router.register(r'resep', ResepViewSet, basename='resep')
router.register(r'bahan-resep', BahanResepViewSet, basename='bahan-resep')
router.register(r'steps-resep', StepsResepViewSet, basename='steps-resep')
router.register(r'tips-resep', TipsResepViewSet, basename='tips-resep')
router.register(r'nutrisi-resep', NutrisiResepViewSet, basename='nutrisi-resep')
router.register(r'foto-resep', FotoResepViewSet, basename='foto-resep')
router.register(r'tipe-transaksi', TipeTransaksiViewSet, basename='tipe-transaksi')
router.register(r'transaksi', TransaksiViewSet, basename='transaksi')
router.register(r'pengurus', PengurusViewSet, basename='pengurus')
router.register(r'foto-pengurus', FotoPengurusViewSet, basename='foto-pengurus')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/s3/', upload_to_s3, name='upload-s3'),
]
