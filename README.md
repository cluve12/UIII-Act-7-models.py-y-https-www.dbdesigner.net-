<img width="1081" height="716" alt="image" src="https://github.com/user-attachments/assets/2882b14e-6b3e-462d-ae22-fb902fd6992e" />

from django.db import models


# --------------------------------------------------
#  ENTIDADES PRINCIPALES
# --------------------------------------------------

class ClienteLimpieza(models.Model):
    """Cliente o empresa que contrata servicios."""

    id_cliente = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(
        max_length=255, null=True, blank=True
    )
    direccion_servicio = models.CharField(
        max_length=255, null=True, blank=True
    )
    contacto_principal = models.CharField(
        max_length=100, null=True, blank=True
    )
    email_contacto = models.EmailField(
        max_length=100, null=True, blank=True
    )
    telefono_contacto = models.CharField(
        max_length=20, null=True, blank=True
    )
    tipo_negocio = models.CharField(
        max_length=100, null=True, blank=True
    )
    fecha_inicio_contrato = models.DateField(
        null=True, blank=True
    )
    estado_contrato = models.CharField(
        max_length=50, null=True, blank=True
    )
    frecuencia_servicio = models.CharField(
        max_length=50, null=True, blank=True
    )

    def __str__(self):
        return self.nombre_empresa or f"Cliente #{self.id_cliente}"

    class Meta:
        verbose_name = "Cliente de Limpieza"
        verbose_name_plural = "Clientes de Limpieza"


class ServicioLimpieza(models.Model):
    """Tipos de servicios disponibles."""

    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(
        max_length=100, null=True, blank=True
    )
    descripcion = models.TextField(
        null=True, blank=True
    )
    costo_estandar = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    duracion_estimada_horas = models.IntegerField(
        null=True, blank=True
    )
    productos_usados = models.TextField(
        null=True, blank=True
    )
    requiere_equipo_especial = models.BooleanField(
        null=True, blank=True
    )
    categoria_servicio = models.CharField(
        max_length=50, null=True, blank=True
    )

    def __str__(self):
        return self.nombre_servicio or f"Servicio #{self.id_servicio}"

    class Meta:
        verbose_name = "Servicio de Limpieza"
        verbose_name_plural = "Servicios de Limpieza"


class EmpleadoLimpieza(models.Model):
    """Datos de empleados de limpieza."""

    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=100, null=True, blank=True
    )
    apellido = models.CharField(
        max_length=100, null=True, blank=True
    )
    dni = models.CharField(
        max_length=20, null=True, blank=True
    )
    fecha_contratacion = models.DateField(
        null=True, blank=True
    )
    salario_hora = models.DecimalField(
        max_digits=7, decimal_places=2,
        null=True, blank=True
    )
    turno = models.CharField(
        max_length=50, null=True, blank=True
    )
    telefono = models.CharField(
        max_length=20, null=True, blank=True
    )
    email = models.EmailField(
        max_length=100, null=True, blank=True
    )
    certificaciones_seguridad = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Empleado de Limpieza"
        verbose_name_plural = "Empleados de Limpieza"


class MaterialLimpieza(models.Model):
    """Inventario y stock de materiales."""

    id_material = models.AutoField(primary_key=True)
    nombre_material = models.CharField(
        max_length=255, null=True, blank=True
    )
    descripcion = models.TextField(
        null=True, blank=True
    )
    stock_actual = models.IntegerField(
        null=True, blank=True
    )
    fecha_caducidad = models.DateField(
        null=True, blank=True
    )
    id_proveedor = models.IntegerField(
        null=True, blank=True
    )
    costo_unitario = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    tipo_material = models.CharField(
        max_length=50, null=True, blank=True
    )
    ubicacion_almacen = models.CharField(
        max_length=100, null=True, blank=True
    )

    def __str__(self):
        return self.nombre_material or f"Material #{self.id_material}"

    class Meta:
        verbose_name = "Material de Limpieza"
        verbose_name_plural = "Materiales de Limpieza"


# --------------------------------------------------
#  RELACION / TRANSACCIONES
# --------------------------------------------------

class ProgramacionServicio(models.Model):
    """Servicios programados con cliente y empleado."""

    id_programacion = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        ClienteLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    servicio = models.ForeignKey(
        ServicioLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    empleado_asignado = models.ForeignKey(
        EmpleadoLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    fecha_programada = models.DateTimeField(
        null=True, blank=True
    )
    hora_inicio = models.TimeField(
        null=True, blank=True
    )
    hora_fin = models.TimeField(
        null=True, blank=True
    )

    estado_servicio = models.CharField(
        max_length=50, null=True, blank=True
    )
    observaciones_cliente = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        cliente = (
            self.cliente.nombre_empresa
            if self.cliente else "N/A"
        )
        return f"Prog. {self.id_programacion} - {cliente}"

    class Meta:
        verbose_name = "Programación de Servicio"
        verbose_name_plural = "Programaciones de Servicios"


class FacturaLimpieza(models.Model):
    """Facturas generadas por servicios."""

    id_factura = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        ClienteLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    programacion_asociada = models.ForeignKey(
        ProgramacionServicio,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    fecha_emision = models.DateField(
        null=True, blank=True
    )
    monto_total = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    impuestos_aplicados = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True
    )
    estado_pago = models.CharField(
        max_length=50, null=True, blank=True
    )
    metodo_pago = models.CharField(
        max_length=50, null=True, blank=True
    )
    fecha_vencimiento = models.DateField(
        null=True, blank=True
    )

    def __str__(self):
        return f"Factura #{self.id_factura}"

    class Meta:
        verbose_name = "Factura de Limpieza"
        verbose_name_plural = "Facturas de Limpieza"


class UsoMaterial(models.Model):
    """Registro de materiales usados en el servicio."""

    id_uso = models.AutoField(primary_key=True)

    programacion = models.ForeignKey(
        ProgramacionServicio,
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        MaterialLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    empleado_registro = models.ForeignKey(
        EmpleadoLimpieza,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    cantidad_usada = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True
    )
    fecha_registro = models.DateTimeField(
        null=True, blank=True
    )
    comentarios_uso = models.TextField(
        null=True, blank=True
    )

    def __str__(self):
        material = (
            self.material.nombre_material
            if self.material else "N/A"
        )
        return f"Uso #{self.id_uso} de {material}"

    class Meta:
        verbose_name = "Uso de Material"
        verbose_name_plural = "Usos de Materiales"

