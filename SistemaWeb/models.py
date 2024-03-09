
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Grifo(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()  # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()  # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Conductor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    apellido = models.CharField(max_length=150, unique= True)
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper() 
        self.apellido= self.apellido.upper() # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def get_nombre_apellido(self):
        return f"{self.nombre} {self.apellido}"

class Camion(models.Model):
    placa = models.CharField(max_length=7, unique=True)
    estado = models.BooleanField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    conductor = models.ForeignKey(Conductor,null=True, blank = True, on_delete = models.CASCADE) 

    def save(self, *args, **kwargs):
        self.placa = self.placa.upper() # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.placa

class DataGeneral(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente de Pago'),
        ('C', 'Cancelado'),
        ('CP', 'Cancelado Parcialmente'),
    ]
    fecha_creacion = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    placa = models.ForeignKey(Camion, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    galones = models.DecimalField(max_digits=10, decimal_places=3)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    documento = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    kilometraje = models.DecimalField(max_digits=10, decimal_places=1)
    grifo = models.ForeignKey(Grifo, on_delete=models.CASCADE)
    traspaso_id= models.IntegerField(blank=True, null=True)
    cantidad_traspaso= models.DecimalField(max_digits=15, decimal_places=3,blank=True, null=True)
    Monto_Transpaso= models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES)
    detalle = models.CharField(max_length=150,blank=True, null=True)    
    observacion = models.TextField(blank=True, null=True)
    estado_rendimiento= models.BooleanField(blank=True, null=True,default=False)
    estado_omitir= models.BooleanField(blank=True, null=True,default=False)

    def save(self, *args, **kwargs):
        self.documento = self.documento.upper()
         # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grifo} - {self.producto} - {self.placa} - {self.fecha_creacion}"

class Banco(models.Model):
    nombre= models.CharField(max_length=150, unique=True)
    abreviatura= models.CharField(max_length=5, null = False,blank=False)
    estado = models.BooleanField()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.abreviatura = self.abreviatura.upper() # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
class Rendimiento(models.Model):
    id_datageneral = models.ForeignKey(DataGeneral, on_delete=models.CASCADE)
    fecha_tanqueo = models.DateTimeField()
    año = models.IntegerField(blank=True, null=True)
    periodo = models.CharField(max_length=20, blank=True, null=True)  
    km_recorrido = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True) 
    rend_kmxglp = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    gl_esperado = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    ren_esperado = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    exceso_real = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    origen = models.CharField(max_length=150) 
    destino= models.CharField(max_length=150)
    carga = models.CharField(max_length=10)  
    peso = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.origen = self.origen.upper()
        self.destino = self.destino.upper()
        self.carga = self.carga.upper() # Convierte el nombre a mayúsculas antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return self.id

@receiver(pre_save, sender=Rendimiento)
def calcular_anio_periodo(sender, instance, **kwargs):
    # Obtener el año de la fecha de tanqueo
    instance.año = instance.fecha_tanqueo.year

    # Obtener el periodo de la fecha de tanqueo
    meses = {
        1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL', 5: 'MAYO', 6: 'JUNIO',
        7: 'JULIO', 8: 'AGOSTO', 9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
    }
    mes_numero = instance.fecha_tanqueo.month
    instance.periodo = meses[mes_numero]

class traspasos(models.Model):
    id_datageneral = models.ForeignKey(DataGeneral, on_delete=models.CASCADE, unique=True)
    cantidad_traspaso= models.DecimalField(max_digits=15, decimal_places=3,blank=True, null=True)
    def __str__(self):
        return self.id_datageneral