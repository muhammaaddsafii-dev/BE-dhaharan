from rest_framework import serializers
from django.contrib.gis.geos import GEOSGeometry
import json
from .models import (
    JenisKegiatan, StatusKegiatan, Kegiatan, FotoKegiatan, Volunteer,
    Resep, BahanResep, StepsResep, TipsResep, NutrisiResep, FotoResep,
    TipeTransaksi, Transaksi, Pengurus
)


# Jenis Kegiatan Serializers
class JenisKegiatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisKegiatan
        fields = '__all__'


# Status Kegiatan Serializers
class StatusKegiatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusKegiatan
        fields = '__all__'


# Foto Kegiatan Serializers
class FotoKegiatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoKegiatan
        fields = '__all__'


# Kegiatan Serializers
class KegiatanSerializer(serializers.ModelSerializer):
    jenis_kegiatan_detail = JenisKegiatanSerializer(source='jenis_kegiatan', read_only=True)
    status_kegiatan_detail = StatusKegiatanSerializer(source='status_kegiatan', read_only=True)
    foto = FotoKegiatanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Kegiatan
        fields = [
            'id', 'nama', 'deskripsi', 'tanggal', 'jumlah_peserta',
            'lokasi', 'jenis_kegiatan', 'jenis_kegiatan_detail',
            'status_kegiatan', 'status_kegiatan_detail', 'foto',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Convert Point to GeoJSON format for output"""
        data = super().to_representation(instance)
        if instance.lokasi:
            data['lokasi'] = {
                'type': 'Point',
                'coordinates': [instance.lokasi.x, instance.lokasi.y]  # [lng, lat]
            }
        return data
    
    def create(self, validated_data):
        # Convert lokasi dict to GEOSGeometry if needed
        if 'lokasi' in validated_data and isinstance(validated_data['lokasi'], dict):
            validated_data['lokasi'] = GEOSGeometry(json.dumps(validated_data['lokasi']))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Convert lokasi dict to GEOSGeometry if needed
        if 'lokasi' in validated_data and isinstance(validated_data['lokasi'], dict):
            validated_data['lokasi'] = GEOSGeometry(json.dumps(validated_data['lokasi']))
        return super().update(instance, validated_data)


class KegiatanListSerializer(serializers.ModelSerializer):
    jenis_kegiatan_detail = JenisKegiatanSerializer(source='jenis_kegiatan', read_only=True)
    status_kegiatan_detail = StatusKegiatanSerializer(source='status_kegiatan', read_only=True)
    foto = FotoKegiatanSerializer(many=True, read_only=True)
    
    class Meta:
        model = Kegiatan
        fields = [
            'id', 'nama', 'deskripsi', 'tanggal', 'jumlah_peserta',
            'lokasi', 'jenis_kegiatan', 'jenis_kegiatan_detail',
            'status_kegiatan', 'status_kegiatan_detail', 'foto',
            'created_at', 'updated_at'
        ]
    
    def to_representation(self, instance):
        """Convert Point to GeoJSON format for output"""
        data = super().to_representation(instance)
        if instance.lokasi:
            data['lokasi'] = {
                'type': 'Point',
                'coordinates': [instance.lokasi.x, instance.lokasi.y]  # [lng, lat]
            }
        return data


# Volunteer Serializers
class VolunteerSerializer(serializers.ModelSerializer):
    kegiatan_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Volunteer
        fields = [
            'id', 'nama', 'email', 'phone', 'skill', 'motivasi',
            'kegiatan', 'kegiatan_detail', 'is_approved',
            'created_at', 'updated_at'
        ]
    
    def get_kegiatan_detail(self, obj):
        return {
            'id': obj.kegiatan.id,
            'nama': obj.kegiatan.nama,
            'tanggal': obj.kegiatan.tanggal
        }


# Bahan Resep Serializers
class BahanResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = BahanResep
        fields = '__all__'


# Steps Resep Serializers
class StepsResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepsResep
        fields = '__all__'


# Tips Resep Serializers
class TipsResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsResep
        fields = '__all__'


# Nutrisi Resep Serializers
class NutrisiResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutrisiResep
        fields = '__all__'


# Foto Resep Serializers
class FotoResepSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoResep
        fields = '__all__'


# Resep Serializers
class ResepSerializer(serializers.ModelSerializer):
    bahan = BahanResepSerializer(many=True, read_only=True)
    steps = StepsResepSerializer(many=True, read_only=True)
    tips = TipsResepSerializer(many=True, read_only=True)
    nutrisi = NutrisiResepSerializer(many=True, read_only=True)
    foto = FotoResepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resep
        fields = [
            'id', 'judul', 'deskripsi', 'kategori', 'tingkat_kesulitan',
            'waktu_memasak', 'waktu_persiapan', 'porsi', 'kalori',
            'bahan', 'steps', 'tips', 'nutrisi', 'foto',
            'created_at', 'updated_at'
        ]


class ResepListSerializer(serializers.ModelSerializer):
    bahan = BahanResepSerializer(many=True, read_only=True)
    steps = StepsResepSerializer(many=True, read_only=True)
    tips = TipsResepSerializer(many=True, read_only=True)
    nutrisi = NutrisiResepSerializer(many=True, read_only=True)
    foto = FotoResepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resep
        fields = [
            'id', 'judul', 'deskripsi', 'kategori', 'tingkat_kesulitan',
            'waktu_memasak', 'waktu_persiapan', 'porsi', 'kalori',
            'bahan', 'steps', 'tips', 'nutrisi', 'foto',
            'created_at', 'updated_at'
        ]


# Tipe Transaksi Serializers
class TipeTransaksiSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipeTransaksi
        fields = '__all__'


# Transaksi Serializers
class TransaksiSerializer(serializers.ModelSerializer):
    tipe_transaksi_detail = TipeTransaksiSerializer(source='tipe_transaksi', read_only=True)
    
    class Meta:
        model = Transaksi
        fields = [
            'id', 'nama', 'tipe_transaksi', 'tipe_transaksi_detail',
            'deskripsi', 'jumlah', 'tanggal',
            'created_at', 'updated_at'
        ]


# Pengurus Serializers
class PengurusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengurus
        fields = [
            'id', 'nama', 'jabatan', 'photo',
            'created_at', 'updated_at'
        ]
