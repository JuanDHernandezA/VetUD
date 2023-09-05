from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key = True)
    nombre_cliente = models.CharField(max_length=50)
    direccion_cliente = models.CharField(max_length=50)
    correo_cliente = models.CharField(max_length=30)
    contrasena_cliente = models.CharField(max_length=20)
    telefono_cliente = models.CharField(max_length=20)


class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    nombre_perfil = models.CharField(max_length=30)

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre_emp = models.CharField(max_length=50)
    direccion_emp = models.CharField(max_length=50)
    telefono_emp = models.CharField(max_length=20)
    correo_emp = models.CharField(max_length=30)
    contrasena_emp = models.CharField(max_length=25)
    id_perfil = models.ForeignKey(Perfil ,models.DO_NOTHING, db_column='id_perfil')

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    tipo_estado = models.CharField(max_length=30)

class Mascota(models.Model):
    id_mascota = models.AutoField(primary_key=True)
    nombre_mascota = models.CharField(max_length=30)
    tipo_mascota = models.CharField(max_length=20)
    raza_mascota = models.CharField(max_length=30, blank=True, null=True)
    edad_mascota = models.CharField(max_length=5, blank=True, null=True)
    peso_mascota = models.CharField(max_length=5, blank=True, null=True)
    sexo_mascota = models.CharField(max_length=5, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

class Cita(models.Model):
    id_cita = models.AutoField(primary_key=True)
    fecha_inicio = models.DateTimeField()
    id_estado = models.ForeignKey(Estado, models.DO_NOTHING, db_column='id_estado')
    id_mascota = models.ForeignKey(Mascota, models.DO_NOTHING, db_column='id_mascota', null=True)
    id_empleado = models.ForeignKey(Empleado, models.DO_NOTHING, db_column='id_empleado')


class HistoriaClinica(models.Model):
    id_historia = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)
    tratamiento = models.CharField(max_length=200)
    id_cita = models.ForeignKey(Cita, models.DO_NOTHING, db_column='id_cita')










