from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from dhaharan.models import (
    JenisKegiatan, StatusKegiatan, Kegiatan, FotoKegiatan, Volunteer,
    Resep, BahanResep, StepsResep, TipsResep, NutrisiResep, FotoResep,
    TipeTransaksi, Transaksi, Pengurus, FotoPengurus
)
from datetime import date, timedelta
from decimal import Decimal


class Command(BaseCommand):
    help = 'Generate dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to generate dummy data...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        JenisKegiatan.objects.all().delete()
        StatusKegiatan.objects.all().delete()
        TipeTransaksi.objects.all().delete()
        
        # Generate Jenis Kegiatan
        self.stdout.write('Creating Jenis Kegiatan...')
        jenis_kegiatan_data = [
            {'nama': 'Bakti Sosial', 'deskripsi': 'Kegiatan bakti sosial untuk masyarakat'},
            {'nama': 'Santunan', 'deskripsi': 'Pemberian santunan kepada yang membutuhkan'},
            {'nama': 'Event', 'deskripsi': 'Event khusus dan acara tahunan'},
        ]
        jenis_kegiatan_list = []
        for data in jenis_kegiatan_data:
            jk = JenisKegiatan.objects.create(**data)
            jenis_kegiatan_list.append(jk)
            self.stdout.write(f'  ✓ Created: {jk.nama}')
        
        # Generate Status Kegiatan
        self.stdout.write('Creating Status Kegiatan...')
        status_kegiatan_data = [
            {'nama': 'Akan Datang', 'deskripsi': 'Kegiatan yang akan dilaksanakan'},
            {'nama': 'Berlangsung', 'deskripsi': 'Kegiatan yang sedang berlangsung'},
            {'nama': 'Selesai', 'deskripsi': 'Kegiatan yang telah selesai'},
        ]
        status_kegiatan_list = []
        for data in status_kegiatan_data:
            sk = StatusKegiatan.objects.create(**data)
            status_kegiatan_list.append(sk)
            self.stdout.write(f'  ✓ Created: {sk.nama}')
        
        # Generate Kegiatan
        self.stdout.write('Creating Kegiatan...')
        kegiatan_data = [
            {
                'nama': 'Bakti Sosial Ramadan 2024',
                'deskripsi': 'Kegiatan bakti sosial menyambut bulan Ramadan dengan membagikan paket sembako',
                'tanggal': date.today() + timedelta(days=30),
                'jumlah_peserta': 150,
                'lokasi': Point(110.370529, -7.797068),  # Yogyakarta
                'jenis_kegiatan': jenis_kegiatan_list[0],
                'status_kegiatan': status_kegiatan_list[0],
            },
            {
                'nama': 'Santunan Anak Yatim',
                'deskripsi': 'Memberikan santunan kepada anak yatim piatu di panti asuhan',
                'tanggal': date.today() + timedelta(days=15),
                'jumlah_peserta': 75,
                'lokasi': Point(106.816666, -6.914744),  # Depok
                'jenis_kegiatan': jenis_kegiatan_list[1],
                'status_kegiatan': status_kegiatan_list[0],
            },
            {
                'nama': 'Festival Makanan Sehat',
                'deskripsi': 'Event tahunan festival makanan sehat dan bergizi',
                'tanggal': date.today(),
                'jumlah_peserta': 200,
                'lokasi': Point(106.845599, -6.208763),  # Jakarta
                'jenis_kegiatan': jenis_kegiatan_list[2],
                'status_kegiatan': status_kegiatan_list[1],
            },
            {
                'nama': 'Buka Puasa Bersama',
                'deskripsi': 'Acara buka puasa bersama masyarakat sekitar',
                'tanggal': date.today() - timedelta(days=10),
                'jumlah_peserta': 300,
                'lokasi': Point(112.731391, -7.257472),  # Surabaya
                'jenis_kegiatan': jenis_kegiatan_list[2],
                'status_kegiatan': status_kegiatan_list[2],
            },
            {
                'nama': 'Donor Darah Rutin',
                'deskripsi': 'Kegiatan donor darah rutin bekerjasama dengan PMI',
                'tanggal': date.today() - timedelta(days=30),
                'jumlah_peserta': 100,
                'lokasi': Point(107.608238, -6.914744),  # Bandung
                'jenis_kegiatan': jenis_kegiatan_list[0],
                'status_kegiatan': status_kegiatan_list[2],
            },
        ]
        kegiatan_list = []
        for data in kegiatan_data:
            kegiatan = Kegiatan.objects.create(**data)
            kegiatan_list.append(kegiatan)
            self.stdout.write(f'  ✓ Created: {kegiatan.nama}')
        
        # Generate Volunteer
        self.stdout.write('Creating Volunteer...')
        volunteer_data = [
            {
                'nama': 'Budi Santoso',
                'email': 'budi.santoso@email.com',
                'phone': '081234567890',
                'skill': 'Memasak, Koordinasi acara',
                'motivasi': 'Ingin berbagi kebahagiaan dengan sesama',
                'kegiatan': kegiatan_list[0],
                'is_approved': True,
            },
            {
                'nama': 'Siti Aminah',
                'email': 'siti.aminah@email.com',
                'phone': '081234567891',
                'skill': 'Dokumentasi, Fotografi',
                'motivasi': 'Mendokumentasikan momen kebaikan untuk inspirasi',
                'kegiatan': kegiatan_list[0],
                'is_approved': True,
            },
            {
                'nama': 'Ahmad Hidayat',
                'email': 'ahmad.hidayat@email.com',
                'phone': '081234567892',
                'skill': 'Public speaking, MC',
                'motivasi': 'Membantu kelancaran acara sosial',
                'kegiatan': kegiatan_list[1],
                'is_approved': False,
            },
            {
                'nama': 'Dewi Lestari',
                'email': 'dewi.lestari@email.com',
                'phone': '081234567893',
                'skill': 'Mengajar, Membimbing anak',
                'motivasi': 'Berbagi ilmu dengan anak-anak',
                'kegiatan': kegiatan_list[1],
                'is_approved': True,
            },
            {
                'nama': 'Rizky Pratama',
                'email': 'rizky.pratama@email.com',
                'phone': '081234567894',
                'skill': 'Logistik, Pengadaan barang',
                'motivasi': 'Memastikan kebutuhan acara terpenuhi',
                'kegiatan': kegiatan_list[2],
                'is_approved': False,
            },
        ]
        for data in volunteer_data:
            volunteer = Volunteer.objects.create(**data)
            self.stdout.write(f'  ✓ Created: {volunteer.nama}')
        
        # Generate Resep
        self.stdout.write('Creating Resep...')
        resep_data = [
            {
                'judul': 'Nasi Goreng Spesial',
                'deskripsi': 'Nasi goreng dengan bumbu rempah pilihan dan topping lengkap',
                'kategori': 'makanan',
                'tingkat_kesulitan': 'mudah',
                'waktu_memasak': 20,
                'waktu_persiapan': 15,
                'porsi': 4,
                'kalori': 450,
            },
            {
                'judul': 'Soto Ayam Kuning',
                'deskripsi': 'Soto ayam dengan kuah kuning yang gurih dan hangat',
                'kategori': 'makanan',
                'tingkat_kesulitan': 'sedang',
                'waktu_memasak': 45,
                'waktu_persiapan': 20,
                'porsi': 6,
                'kalori': 350,
            },
            {
                'judul': 'Es Teh Manis',
                'deskripsi': 'Minuman teh manis dingin yang menyegarkan',
                'kategori': 'minuman',
                'tingkat_kesulitan': 'mudah',
                'waktu_memasak': 5,
                'waktu_persiapan': 5,
                'porsi': 2,
                'kalori': 120,
            },
            {
                'judul': 'Pudding Coklat',
                'deskripsi': 'Pudding coklat lembut dengan topping vla vanila',
                'kategori': 'dessert',
                'tingkat_kesulitan': 'mudah',
                'waktu_memasak': 30,
                'waktu_persiapan': 10,
                'porsi': 8,
                'kalori': 200,
            },
            {
                'judul': 'Risoles Sayur',
                'deskripsi': 'Risoles isi sayuran dengan kulit yang renyah',
                'kategori': 'snack',
                'tingkat_kesulitan': 'sedang',
                'waktu_memasak': 40,
                'waktu_persiapan': 30,
                'porsi': 10,
                'kalori': 180,
            },
        ]
        resep_list = []
        for data in resep_data:
            resep = Resep.objects.create(**data)
            resep_list.append(resep)
            self.stdout.write(f'  ✓ Created: {resep.judul}')
        
        # Generate Bahan Resep untuk Nasi Goreng
        self.stdout.write('Creating Bahan Resep...')
        BahanResep.objects.create(resep=resep_list[0], nama='Nasi putih', takaran='500 gram')
        BahanResep.objects.create(resep=resep_list[0], nama='Telur', takaran='2 butir')
        BahanResep.objects.create(resep=resep_list[0], nama='Bawang merah', takaran='5 siung')
        BahanResep.objects.create(resep=resep_list[0], nama='Kecap manis', takaran='3 sdm')
        
        # Generate Steps Resep untuk Nasi Goreng
        self.stdout.write('Creating Steps Resep...')
        StepsResep.objects.create(resep=resep_list[0], urutan=1, nama='Panaskan minyak dalam wajan')
        StepsResep.objects.create(resep=resep_list[0], urutan=2, nama='Tumis bawang merah hingga harum')
        StepsResep.objects.create(resep=resep_list[0], urutan=3, nama='Masukkan telur, orak-arik')
        StepsResep.objects.create(resep=resep_list[0], urutan=4, nama='Masukkan nasi, aduk rata dengan bumbu')
        
        # Generate Tips Resep
        self.stdout.write('Creating Tips Resep...')
        TipsResep.objects.create(resep=resep_list[0], urutan=1, nama='Gunakan nasi dingin agar tidak lengket')
        TipsResep.objects.create(resep=resep_list[0], urutan=2, nama='Api harus besar agar nasi tidak lembek')
        
        # Generate Nutrisi Resep
        self.stdout.write('Creating Nutrisi Resep...')
        NutrisiResep.objects.create(resep=resep_list[0], label='Protein', nilai='15g')
        NutrisiResep.objects.create(resep=resep_list[0], label='Karbohidrat', nilai='65g')
        NutrisiResep.objects.create(resep=resep_list[0], label='Lemak', nilai='12g')
        
        # Generate Tipe Transaksi
        self.stdout.write('Creating Tipe Transaksi...')
        tipe_transaksi_data = [
            {'nama': 'Pemasukan'},
            {'nama': 'Pengeluaran'},
        ]
        tipe_transaksi_list = []
        for data in tipe_transaksi_data:
            tt = TipeTransaksi.objects.create(**data)
            tipe_transaksi_list.append(tt)
            self.stdout.write(f'  ✓ Created: {tt.nama}')
        
        # Generate Transaksi
        self.stdout.write('Creating Transaksi...')
        transaksi_data = [
            {
                'nama': 'Donasi Bulanan Januari',
                'tipe_transaksi': tipe_transaksi_list[0],
                'deskripsi': 'Penerimaan donasi rutin bulan Januari',
                'jumlah': Decimal('5000000.00'),
                'tanggal': date.today() - timedelta(days=20),
            },
            {
                'nama': 'Pembelian Sembako',
                'tipe_transaksi': tipe_transaksi_list[1],
                'deskripsi': 'Pembelian sembako untuk bakti sosial',
                'jumlah': Decimal('2500000.00'),
                'tanggal': date.today() - timedelta(days=15),
            },
            {
                'nama': 'Donasi Event Festival',
                'tipe_transaksi': tipe_transaksi_list[0],
                'deskripsi': 'Sponsorship untuk festival makanan sehat',
                'jumlah': Decimal('10000000.00'),
                'tanggal': date.today() - timedelta(days=10),
            },
            {
                'nama': 'Sewa Tempat Acara',
                'tipe_transaksi': tipe_transaksi_list[1],
                'deskripsi': 'Biaya sewa tempat untuk acara buka puasa',
                'jumlah': Decimal('3000000.00'),
                'tanggal': date.today() - timedelta(days=5),
            },
            {
                'nama': 'Donasi Online',
                'tipe_transaksi': tipe_transaksi_list[0],
                'deskripsi': 'Donasi melalui platform online',
                'jumlah': Decimal('1500000.00'),
                'tanggal': date.today(),
            },
        ]
        for data in transaksi_data:
            transaksi = Transaksi.objects.create(**data)
            self.stdout.write(f'  ✓ Created: {transaksi.nama}')
        
        # Generate Pengurus
        self.stdout.write('Creating Pengurus...')
        pengurus_data = [
            {'nama': 'Dr. Hadi Wijaya', 'jabatan': 'Ketua Umum'},
            {'nama': 'Ir. Lestari Putri', 'jabatan': 'Wakil Ketua'},
            {'nama': 'Drs. Muhammad Iqbal', 'jabatan': 'Sekretaris'},
            {'nama': 'SE. Ratna Sari', 'jabatan': 'Bendahara'},
            {'nama': 'S.Kom. Eko Prasetyo', 'jabatan': 'Koordinator IT'},
        ]
        for data in pengurus_data:
            pengurus = Pengurus.objects.create(**data)
            self.stdout.write(f'  ✓ Created: {pengurus.nama}')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Successfully generated all dummy data!'))
        self.stdout.write(self.style.SUCCESS('You can now test your API endpoints.'))
