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
    
    def update(self, request, *args, **kwargs):
        """
        Override update to handle foto deletion before updating
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Check if there's a request to delete old photos
        # This can be done by checking if new photos are being uploaded
        # or if there's a specific flag in the request
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def delete_photos(self, request, pk=None):
        """
        Delete specific photos from kegiatan
        Expects: {"photo_ids": [1, 2, 3]}
        """
        kegiatan = self.get_object()
        photo_ids = request.data.get('photo_ids', [])
        
        if not photo_ids:
            return Response(
                {'error': 'photo_ids is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted_count = 0
        errors = []
        
        for photo_id in photo_ids:
            try:
                photo = FotoKegiatan.objects.get(id=photo_id, kegiatan=kegiatan)
                
                # Delete file from S3
                if photo.file_path:
                    try:
                        storage = photo.file_path.storage
                        if storage.exists(photo.file_path.name):
                            storage.delete(photo.file_path.name)
                    except Exception as e:
                        errors.append(f"Error deleting file for photo {photo_id}: {str(e)}")
                
                # Delete from database
                photo.delete()
                deleted_count += 1
                
            except FotoKegiatan.DoesNotExist:
                errors.append(f"Photo with id {photo_id} not found or doesn't belong to this kegiatan")
        
        response_data = {
            'deleted_count': deleted_count,
            'total_requested': len(photo_ids)
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def replace_all_photos(self, request, pk=None):
        """
        Delete all existing photos and prepare for new uploads
        This should be called BEFORE uploading new photos
        """
        kegiatan = self.get_object()
        
        # Get all photos for this kegiatan
        photos = FotoKegiatan.objects.filter(kegiatan=kegiatan)
        deleted_count = 0
        errors = []
        
        for photo in photos:
            try:
                # Delete file from S3
                if photo.file_path:
                    try:
                        storage = photo.file_path.storage
                        if storage.exists(photo.file_path.name):
                            storage.delete(photo.file_path.name)
                    except Exception as e:
                        errors.append(f"Error deleting file {photo.file_name}: {str(e)}")
                
                # Delete from database
                photo.delete()
                deleted_count += 1
                
            except Exception as e:
                errors.append(f"Error deleting photo {photo.id}: {str(e)}")
        
        response_data = {
            'message': f'Deleted {deleted_count} photos',
            'deleted_count': deleted_count
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_200_OK)


class FotoKegiatanViewSet(viewsets.ModelViewSet):
    queryset = FotoKegiatan.objects.all()
    serializer_class = FotoKegiatanSerializer
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to delete file from S3 before deleting from database
        """
        instance = self.get_object()
        
        # Delete file from S3 if exists
        if instance.file_path:
            try:
                # Get storage instance and delete from S3
                storage = instance.file_path.storage
                if storage.exists(instance.file_path.name):
                    storage.delete(instance.file_path.name)
            except Exception as e:
                # Log error but continue with database deletion
                print(f"Error deleting file from S3: {str(e)}")
        
        # Delete from database
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
