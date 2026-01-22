from django.contrib.gis.db import models as gis_models
from django.db import models


class JenisKegiatan(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jenis_kegiatan'
        verbose_name = 'Jenis Kegiatan'
        verbose_name_plural = 'Jenis Kegiatan'

    def __str__(self):
        return self.nama


class StatusKegiatan(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'status_kegiatan'
        verbose_name = 'Status Kegiatan'
        verbose_name_plural = 'Status Kegiatan'

    def __str__(self):
        return self.nama


class Kegiatan(models.Model):
    nama = models.CharField(max_length=200)
    deskripsi = models.TextField()
    tanggal = models.DateField()
    jumlah_peserta = models.IntegerField(default=0)
    lokasi = gis_models.PointField()
    jenis_kegiatan = models.ForeignKey(JenisKegiatan, on_delete=models.CASCADE, related_name='kegiatan')
    status_kegiatan = models.ForeignKey(StatusKegiatan, on_delete=models.CASCADE, related_name='kegiatan')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kegiatan'
        verbose_name = 'Kegiatan'
        verbose_name_plural = 'Kegiatan'
        ordering = ['-tanggal']

    def __str__(self):
        return self.nama


class FotoKegiatan(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='foto')
    file_path = models.ImageField(upload_to='kegiatan/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_kegiatan'
        verbose_name = 'Foto Kegiatan'
        verbose_name_plural = 'Foto Kegiatan'

    def __str__(self):
        return f"{self.kegiatan.nama} - {self.file_name}"


class Volunteer(models.Model):
    nama = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    skill = models.TextField()
    motivasi = models.TextField()
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='volunteer')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'volunteer'
        verbose_name = 'Volunteer'
        verbose_name_plural = 'Volunteer'

    def __str__(self):
        return f"{self.nama} - {self.kegiatan.nama}"


class Resep(models.Model):
    KATEGORI_CHOICES = [
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
        ('dessert', 'Dessert'),
        ('snack', 'Snack'),
    ]
    
    TINGKAT_KESULITAN_CHOICES = [
        ('mudah', 'Mudah'),
        ('sedang', 'Sedang'),
        ('sulit', 'Sulit'),
    ]

    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES)
    tingkat_kesulitan = models.CharField(max_length=50, choices=TINGKAT_KESULITAN_CHOICES)
    waktu_memasak = models.IntegerField(help_text='Waktu dalam menit')
    waktu_persiapan = models.IntegerField(help_text='Waktu dalam menit')
    porsi = models.IntegerField()
    kalori = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resep'
        verbose_name = 'Resep'
        verbose_name_plural = 'Resep'
        ordering = ['-created_at']

    def __str__(self):
        return self.judul


class BahanResep(models.Model):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='bahan')
    nama = models.CharField(max_length=200)
    takaran = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bahan_resep'
        verbose_name = 'Bahan Resep'
        verbose_name_plural = 'Bahan Resep'

    def __str__(self):
        return f"{self.nama} - {self.resep.judul}"


class StepsResep(models.Model):
    urutan = models.IntegerField()
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='steps')
    nama = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'steps_resep'
        verbose_name = 'Steps Resep'
        verbose_name_plural = 'Steps Resep'
        ordering = ['urutan']

    def __str__(self):
        return f"Step {self.urutan} - {self.resep.judul}"


class TipsResep(models.Model):
    urutan = models.IntegerField()
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='tips')
    nama = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tips_resep'
        verbose_name = 'Tips Resep'
        verbose_name_plural = 'Tips Resep'
        ordering = ['urutan']

    def __str__(self):
        return f"Tips {self.urutan} - {self.resep.judul}"


class NutrisiResep(models.Model):
    label = models.CharField(max_length=100)
    nilai = models.CharField(max_length=100)
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='nutrisi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nutrisi_resep'
        verbose_name = 'Nutrisi Resep'
        verbose_name_plural = 'Nutrisi Resep'

    def __str__(self):
        return f"{self.label} - {self.resep.judul}"


class TipeTransaksi(models.Model):
    nama = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tipe_transaksi'
        verbose_name = 'Tipe Transaksi'
        verbose_name_plural = 'Tipe Transaksi'

    def __str__(self):
        return self.nama


class Transaksi(models.Model):
    nama = models.CharField(max_length=200)
    tipe_transaksi = models.ForeignKey(TipeTransaksi, on_delete=models.CASCADE, related_name='transaksi')
    deskripsi = models.TextField()
    jumlah = models.DecimalField(max_digits=15, decimal_places=2)
    tanggal = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transaksi'
        verbose_name = 'Transaksi'
        verbose_name_plural = 'Transaksi'
        ordering = ['-tanggal']

    def __str__(self):
        return self.nama


class Pengurus(models.Model):
    nama = models.CharField(max_length=200)
    jabatan = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pengurus'
        verbose_name = 'Pengurus'
        verbose_name_plural = 'Pengurus'

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


class FotoPengurus(models.Model):
    pengurus = models.ForeignKey(Pengurus, on_delete=models.CASCADE, related_name='foto')
    file_path = models.ImageField(upload_to='pengurus/')
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_pengurus'
        verbose_name = 'Foto Pengurus'
        verbose_name_plural = 'Foto Pengurus'

    def __str__(self):
        return f"{self.pengurus.nama} - {self.file_name}"


class FotoResep(models.Model):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='foto')
    file_path = models.CharField(max_length=500)  # Changed from ImageField to CharField for S3 URLs
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'foto_resep'
        verbose_name = 'Foto Resep'
        verbose_name_plural = 'Foto Resep'

    def __str__(self):
        return f"{self.resep.judul} - {self.file_name}"
