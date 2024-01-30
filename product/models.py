from django.db import models

# Create your models here.
class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    linea = models.CharField(max_length=50, blank=True, null=True)
    sublinea = models.CharField(max_length=50, blank=True, null=True)
    departamento = models.CharField(max_length=50, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ptje1 = models.IntegerField(blank=True, null=True)
    ptjeReal = models.IntegerField(blank=True, null=True)
    precioCalculado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maximo = models.IntegerField(blank=True, null=True)
    minimo = models.IntegerField(blank=True, null=True)
    estatus = models.IntegerField(blank=True, null=True)
    nombreStatus = models.CharField(max_length=50, blank=True, null=True)
    tipoProd = models.IntegerField(blank=True, null=True)
    tipoProdDesc = models.CharField(max_length=50, blank=True, null=True)
    codigosAlternos = models.CharField(max_length=200, blank=True, null=True)
    activo = models.CharField(max_length=10, blank=True, null=True)
    prov = models.CharField(max_length=200, blank=True, null=True)
    nombreProveedor = models.CharField(max_length=200, blank=True, null=True)
    unidad = models.CharField(max_length=50, blank=True, null=True)
    codigoSat = models.CharField(max_length=50, blank=True, null=True)
    nomCodSat = models.CharField(max_length=200, blank=True, null=True)
    unidadSat = models.CharField(max_length=50, blank=True, null=True)
    nomUniSat = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Productos"
        indexes = [
            models.Index(fields=['codigo', 'nombre'])
        ]
        ordering = ['codigo', 'nombre']

    def __str__(self):
        return self.nombre