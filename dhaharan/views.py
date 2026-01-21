from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import (
    JenisKegiatan, StatusKegiatan, Kegiatan, FotoKegiatan, Volunteer,
    Resep, BahanResep, StepsResep, TipsResep, NutrisiResep, FotoResep,
    TipeTransaksi, Transaksi, Pengurus, FotoPengurus
)
from .serializers import (
    JenisKegiatanSerializer, StatusKegiatanSerializer,
    KegiatanSerializer, KegiatanListSerializer, FotoKegiatanSerializer,
    VolunteerSerializer, ResepSerializer, ResepListSerializer,
    BahanResepSerializer, StepsResepSerializer, TipsResepSerializer,
    NutrisiResepSerializer, FotoResepSerializer,
    TipeTransaksiSerializer, TransaksiSerializer,
    PengurusSerializer, FotoPengurusSerializer
)


class JenisKegiatanViewSet(viewsets.ModelViewSet):
    queryset = JenisKegiatan.objects.all()
    serializer_class = JenisKegiatanSerializer


class StatusKegiatanViewSet(viewsets.ModelViewSet):
    queryset = StatusKegiatan.objects.all()
    serializer_class = StatusKegiatanSerializer


class KegiatanViewSet(viewsets.ModelViewSet):
    queryset = Kegiatan.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return KegiatanListSerializer
        return KegiatanSerializer


class FotoKegiatanViewSet(viewsets.ModelViewSet):
    queryset = FotoKegiatan.objects.all()
    serializer_class = FotoKegiatanSerializer


class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        volunteer = self.get_object()
        volunteer.is_approved = True
        volunteer.save()
        serializer = self.get_serializer(volunteer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_volunteers = Volunteer.objects.filter(is_approved=False)
        serializer = self.get_serializer(pending_volunteers, many=True)
        return Response(serializer.data)


class ResepViewSet(viewsets.ModelViewSet):
    queryset = Resep.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResepListSerializer
        return ResepSerializer
    
    @action(detail=False, methods=['get'])
    def by_kategori(self, request):
        kategori = request.query_params.get('kategori', None)
        if kategori:
            resep = Resep.objects.filter(kategori=kategori)
            serializer = self.get_serializer(resep, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Parameter kategori diperlukan'},
            status=status.HTTP_400_BAD_REQUEST
        )


class BahanResepViewSet(viewsets.ModelViewSet):
    queryset = BahanResep.objects.all()
    serializer_class = BahanResepSerializer


class StepsResepViewSet(viewsets.ModelViewSet):
    queryset = StepsResep.objects.all()
    serializer_class = StepsResepSerializer


class TipsResepViewSet(viewsets.ModelViewSet):
    queryset = TipsResep.objects.all()
    serializer_class = TipsResepSerializer


class NutrisiResepViewSet(viewsets.ModelViewSet):
    queryset = NutrisiResep.objects.all()
    serializer_class = NutrisiResepSerializer


class FotoResepViewSet(viewsets.ModelViewSet):
    queryset = FotoResep.objects.all()
    serializer_class = FotoResepSerializer


class TipeTransaksiViewSet(viewsets.ModelViewSet):
    queryset = TipeTransaksi.objects.all()
    serializer_class = TipeTransaksiSerializer


class TransaksiViewSet(viewsets.ModelViewSet):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer
    
    @action(detail=False, methods=['get'])
    def by_tipe(self, request):
        tipe = request.query_params.get('tipe', None)
        if tipe:
            transaksi = Transaksi.objects.filter(tipe_transaksi_id=tipe)
            serializer = self.get_serializer(transaksi, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'Parameter tipe diperlukan'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        from django.db.models import Sum
        total_pemasukan = Transaksi.objects.filter(
            tipe_transaksi__nama='Pemasukan'
        ).aggregate(total=Sum('jumlah'))['total'] or 0
        
        total_pengeluaran = Transaksi.objects.filter(
            tipe_transaksi__nama='Pengeluaran'
        ).aggregate(total=Sum('jumlah'))['total'] or 0
        
        return Response({
            'total_pemasukan': total_pemasukan,
            'total_pengeluaran': total_pengeluaran,
            'saldo': total_pemasukan - total_pengeluaran
        })


class PengurusViewSet(viewsets.ModelViewSet):
    queryset = Pengurus.objects.all()
    serializer_class = PengurusSerializer


class FotoPengurusViewSet(viewsets.ModelViewSet):
    queryset = FotoPengurus.objects.all()
    serializer_class = FotoPengurusSerializer
