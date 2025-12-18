from django.db import models

class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    direccion = models.CharField(max_length=100)
    foto_sucursal = models.ImageField(upload_to='sucursales/fotos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.TextField()
    rfc = models.CharField(max_length=13)  # Campo adicional 1
    tipo_proveedor = models.CharField(max_length=50)  # Campo adicional 2
    fecha_registro = models.DateField(auto_now_add=True)  # Campo adicional 3
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_CHOICES = [
        ('sandwich', 'Sandwich'),
        ('ensalada', 'Ensalada'),
        ('bebida', 'Bebida'),
        ('postre', 'Postre'),
        ('combo', 'Combo'),
    ]
    
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    calorias = models.IntegerField()
    descripcion = models.TextField()  # Campo adicional 1
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos')  # Campo adicional 2
    disponible = models.BooleanField(default=True)  # Campo adicional 3
    
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.CharField(max_length=100)
    fecha_registro = models.DateField()
    sucursales = models.ManyToManyField(Sucursal, related_name="clientes")
    foto_perfil = models.ImageField(upload_to='clientes_fotos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparando', 'Preparando'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    
    id_pedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')  # Campo adicional 1
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES)  # Campo adicional 2
    notas = models.TextField(blank=True, null=True)  # Campo adicional 3
    
    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)  # Campo adicional
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Empleado(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="empleados")
    nombre = models.CharField(max_length=100, default="Empleado")
    telefono = models.CharField(max_length=15)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_contratacion = models.DateField()
    puesto = models.CharField(max_length=50)
    foto_perfil = models.ImageField(upload_to='empleados/fotos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.puesto} - {self.sucursal.nombre}"