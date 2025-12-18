from django.db import models
from django.utils import timezone

# Modelo unificado de Cliente
class Cliente(models.Model):
    nombre_empresa = models.CharField(max_length=255, help_text="Nombre de la empresa o cliente particular", default="")
    contacto_principal = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, help_text="Dirección de facturación o principal")
    direccion_servicio = models.CharField(max_length=255, blank=True, help_text="Dirección donde se realiza el servicio (si es diferente)")
    
    # Detalles del negocio y contrato
    tipo_negocio = models.CharField(max_length=100, blank=True)
    fecha_inicio_contrato = models.DateField(null=True, blank=True)
    estado_contrato = models.CharField(max_length=50, blank=True, help_text="Ej: Activo, Inactivo, Pausado")
    frecuencia_servicio = models.CharField(max_length=50, blank=True, help_text="Ej: Semanal, Quincenal, Mensual")

    def __str__(self):
        return self.nombre_empresa

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, blank=True, null=True)
    puesto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_contratacion = models.DateField()
    salario_por_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    turno = models.CharField(max_length=50, blank=True, help_text="Ej: Mañana, Tarde, Noche")

    def __str__(self):
        return self.nombre

class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre del servicio")
    categoria_servicio = models.ForeignKey(CategoriaServicio, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    costo_estandar = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada_horas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    productos_usados = models.ManyToManyField('Material', blank=True, help_text="Productos que se usan habitualmente en este servicio")

    def __str__(self):
        return self.nombre

class CategoriaMaterial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, help_text="Teléfono principal de la empresa")
    email = models.EmailField(blank=True, help_text="Email principal de la empresa")
    nombre_contacto = models.CharField(max_length=100, blank=True, help_text="Nombre de la persona de contacto")
    email_contacto = models.EmailField(max_length=100, blank=True, help_text="Email de la persona de contacto")
    telefono_contacto = models.CharField(max_length=20, blank=True, help_text="Teléfono de la persona de contacto")

    def __str__(self):
        return self.nombre

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, help_text="Descripción detallada del material.")
    categoria = models.ForeignKey(CategoriaMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    unidad_medida = models.CharField(max_length=50, blank=True)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Costo por unidad del material.")
    fecha_caducidad = models.DateField(null=True, blank=True, help_text="Fecha de caducidad del producto.")
    ubicacion_almacen = models.CharField(max_length=100, blank=True, help_text="Ubicación física en el almacén (Ej: Estantería A, Fila 3).")
    tipo_material = models.CharField(max_length=50, blank=True, help_text="Tipo de material (Ej: Consumible, Equipo, Herramienta).")

    def __str__(self):
        return self.nombre

class UsoMaterial(models.Model):
    programacion = models.ForeignKey('ProgramacionServicio', on_delete=models.SET_NULL, null=True, blank=True, related_name='materiales_usados')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Cantidad de material utilizado (ej: litros, unidades)")
    fecha_registro = models.DateTimeField(default=timezone.now)
    empleado_registro = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, help_text="Empleado que registra el uso del material")
    comentarios_uso = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cantidad_usada} de {self.material.nombre} en {self.programacion}"

class Factura(models.Model):
    ESTADO_PAGO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Pagada', 'Pagada'),
        ('Vencida', 'Vencida'),
        ('Cancelada', 'Cancelada'),
    )
    METODO_PAGO_CHOICES = (
        ('Transferencia', 'Transferencia Bancaria'),
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta de Crédito/Débito'),
        ('Otro', 'Otro'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    programacion_asociada = models.ForeignKey('ProgramacionServicio', on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas')
    fecha_emision = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    impuestos_aplicados = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente')
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, blank=True)

    def __str__(self):
        return f"Factura {self.id} para {self.cliente.nombre_empresa}"

class ProgramacionServicio(models.Model):
    ESTADO_CHOICES = (
        ('Programado', 'Programado'),
        ('En Progreso', 'En Progreso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='programaciones')
    empleado_asignado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True, related_name='servicios_asignados')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_programada = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado_servicio = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Programado')
    observaciones_cliente = models.TextField(blank=True, help_text="Comentarios o requerimientos especiales del cliente.")

    def __str__(self):
        return f"Servicio de {self.servicio.nombre} para {self.cliente.nombre_empresa} el {self.fecha_programada}"
