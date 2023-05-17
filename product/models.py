from django.db import models

# Create your models here.
class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=50, blank=True)
    linea = models.CharField(max_length=50, blank=True)
    sublinea = models.CharField(max_length=50, blank=True)
    departamento = models.CharField(max_length=50, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    precio1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    ptje1 = models.IntegerField(blank=True)
    ptjeReal = models.IntegerField(blank=True)
    precioCalculado = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    maximo = models.IntegerField(blank=True)
    minimo = models.IntegerField(blank=True)
    estatus = models.IntegerField(blank=True)
    nombreStatus = models.CharField(max_length=50, blank=True)
    tipoProd = models.IntegerField(blank=True)
    tipoProdDesc = models.CharField(max_length=50, blank=True)
    codigosAlternos = models.CharField(max_length=100, blank=True)
    activo = models.CharField(max_length=10, blank=True)
    prov = models.IntegerField(blank=True)
    nombreProveedor = models.CharField(max_length=100, blank=True)
    unidad = models.CharField(max_length=50, blank=True)
    codigoSat = models.CharField(max_length=50, blank=True)
    nomCodSat = models.CharField(max_length=100, blank=True)
    unidadSat = models.CharField(max_length=50, blank=True)
    nomUniSat = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Productos"
        indexes = [
            models.Index(fields=['codigo', 'nombre'])
        ]
        ordering = ['codigo', 'nombre']

    def __str__(self):
        return self.nombre