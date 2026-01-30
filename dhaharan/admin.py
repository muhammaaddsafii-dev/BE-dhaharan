from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from .models import (
    JenisKegiatan, StatusKegiatan, Kegiatan, FotoKegiatan, Volunteer,
    Resep, BahanResep, StepsResep, TipsResep, NutrisiResep, FotoResep,
    TipeTransaksi, Transaksi, Pengurus
)


@admin.register(JenisKegiatan)
class JenisKegiatanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'created_at']
    search_fields = ['nama']


@admin.register(StatusKegiatan)
class StatusKegiatanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'created_at']
    search_fields = ['nama']


@admin.register(Kegiatan)
class KegiatanAdmin(GISModelAdmin):
    list_display = ['id', 'nama', 'tanggal', 'jenis_kegiatan', 'status_kegiatan', 'jumlah_peserta']
    list_filter = ['jenis_kegiatan', 'status_kegiatan', 'tanggal']
    search_fields = ['nama', 'deskripsi']
    date_hierarchy = 'tanggal'


@admin.register(FotoKegiatan)
class FotoKegiatanAdmin(admin.ModelAdmin):
    list_display = ['id', 'kegiatan', 'file_name', 'created_at']
    list_filter = ['kegiatan']
    search_fields = ['file_name', 'kegiatan__nama']


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'email', 'phone', 'kegiatan', 'is_approved']
    list_filter = ['is_approved', 'kegiatan']
    search_fields = ['nama', 'email']
    actions = ['approve_volunteers']
    
    def approve_volunteers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_volunteers.short_description = "Approve selected volunteers"


@admin.register(Resep)
class ResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'judul', 'kategori', 'tingkat_kesulitan', 'porsi', 'created_at']
    list_filter = ['kategori', 'tingkat_kesulitan']
    search_fields = ['judul', 'deskripsi']


@admin.register(BahanResep)
class BahanResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'resep', 'nama', 'takaran']
    list_filter = ['resep']
    search_fields = ['nama', 'resep__judul']


@admin.register(StepsResep)
class StepsResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'resep', 'urutan', 'nama']
    list_filter = ['resep']
    ordering = ['resep', 'urutan']


@admin.register(TipsResep)
class TipsResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'resep', 'urutan', 'nama']
    list_filter = ['resep']
    ordering = ['resep', 'urutan']


@admin.register(NutrisiResep)
class NutrisiResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'resep', 'label', 'nilai']
    list_filter = ['resep']
    search_fields = ['label', 'resep__judul']


@admin.register(FotoResep)
class FotoResepAdmin(admin.ModelAdmin):
    list_display = ['id', 'resep', 'file_name', 'created_at']
    list_filter = ['resep']
    search_fields = ['file_name', 'resep__judul']


@admin.register(TipeTransaksi)
class TipeTransaksiAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'created_at']
    search_fields = ['nama']


@admin.register(Transaksi)
class TransaksiAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'tipe_transaksi', 'jumlah', 'tanggal']
    list_filter = ['tipe_transaksi', 'tanggal']
    search_fields = ['nama', 'deskripsi']
    date_hierarchy = 'tanggal'


@admin.register(Pengurus)
class PengurusAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama', 'jabatan', 'created_at']
    search_fields = ['nama', 'jabatan']



