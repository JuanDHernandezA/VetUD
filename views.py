from django.http import HttpResponse
from django.template import Template
from django.template.context import Context
from django.shortcuts import render
from VETUD_Py.models import Cliente
from VETUD_Py.models import Mascota
from VETUD_Py.models import Empleado
from VETUD_Py.models import Perfil
from VETUD_Py.models import Estado
from VETUD_Py.models import HistoriaClinica

from VETUD_Py.models import Cita
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import logging

cliente_actual = ''
empleado_actual = ''
cita_actual = ''

max = 26
cont = True

def MensajeEncriptado(modo, mensaje, clave):
  traduccion = ''
  if modo[0] == 'd':
    clave= -clave
  for simbolo in mensaje:
    if simbolo.isalpha():
      num = ord(simbolo)
      num += clave
      if simbolo.isupper():
        if num > ord('Z'):
          num -= 26
        elif num < ord('A'):
          num += 26
      elif simbolo.islower():
        if num > ord('z'):
          num -= 26
        elif num < ord('a'):
          num += 26

      traduccion += chr(num)
    else:
      traduccion += simbolo
  
  return traduccion


def PaginaPrincipal(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/index.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)

@csrf_exempt
def RegistroUsuario(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/registro_usr.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    if request.method == 'POST':
        nombre_cliente = request.POST['nombre']
        direccion_cliente = request.POST['direccion']
        correo_cliente = request.POST['correo']
        contrasena_cliente = request.POST['contraseña']
        telefono_cliente = request.POST['telefono']
        confirmacion_contrasena = request.POST['confirmacion']
        messages.success(request, 'Funciona')
        
        if nombre_cliente != '' and direccion_cliente != '' and correo_cliente != '' and contrasena_cliente != '' and telefono_cliente != '' and contrasena_cliente == confirmacion_contrasena:
            contrasena_enc = MensajeEncriptado('e',contrasena_cliente, 15)
            Cliente(nombre_cliente = nombre_cliente, direccion_cliente = direccion_cliente, correo_cliente =
            correo_cliente, contrasena_cliente = contrasena_enc, telefono_cliente = telefono_cliente).save()
            global cliente_actual
            cliente_actual = nombre_cliente
            return redirect("reg_mas")

        else:
            return redirect("reg_usr")

    return HttpResponse(documento)

@csrf_exempt
def RegistroMascota(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/registro_mas.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    if request.method == 'POST':
        nombre_mascota = request.POST['nombre']
        tipo_mascota = request.POST['tipo']
        raza_mascota = request.POST['raza']
        edad_mascota = request.POST['edad']
        peso_mascota = request.POST['peso']
        sexo_mascota = request.POST['sexo']
        id_cliente = Cliente.objects.get(nombre_cliente = cliente_actual)
        Mascota(nombre_mascota = nombre_mascota, tipo_mascota = tipo_mascota, raza_mascota =
        raza_mascota, edad_mascota = edad_mascota, peso_mascota = peso_mascota, sexo_mascota = sexo_mascota, id_cliente = id_cliente).save()
        messages.success(request, 'Funciona')

        if nombre_mascota != '' and raza_mascota != '' and edad_mascota != '' and peso_mascota != '' and sexo_mascota != '':
            return redirect("pedir_cita")
        else:
            return redirect("reg_mas")

    return HttpResponse(documento)

@csrf_exempt
def RegistroEmpleado(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/registro_emp.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    if request.method == 'POST':
        nombre_emp = request.POST['nombre']
        direccion_emp = request.POST['direccion']
        correo_emp = request.POST['correo']
        contrasena_emp = request.POST['contraseña']
        telefono_emp = request.POST['telefono']
        confirmacion_contrasena = request.POST['confirmacion']
        perfil_emp = request.POST['profesion']
        id_perfil = None
        if perfil_emp == "Veterinario":
            id_bus = Perfil.objects.filter(id_perfil = 1)
            for b in id_bus:
                id_perfil = b
        else:
            id_bus = Perfil.objects.filter(id_perfil = 2)
            for b in id_bus:
                id_perfil = b
        if nombre_emp != '' and direccion_emp != '' and correo_emp != '' and contrasena_emp != '' and telefono_emp != '' and contrasena_emp == confirmacion_contrasena:
            contrasena_enc = MensajeEncriptado('e',contrasena_emp, 15)
            Empleado(nombre_emp = nombre_emp, direccion_emp = direccion_emp, correo_emp =
            correo_emp, contrasena_emp = contrasena_enc, telefono_emp = telefono_emp, id_perfil = id_perfil).save()
            return redirect('menu_medico')
        else:
            return redirect('reg_emp')

    return HttpResponse(documento)

@csrf_exempt
def AgendarCita(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/agendar_cita.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    clientes = Cliente.objects.all()
    mascota = MascotasRegistradas()
    perfil = Perfil.objects.all()
    contexto = Context({'empleados': empleado, 'perfiles': perfil, 'clientes':clientes, 'mascotas':mascota})
    documento = template.render(contexto)
    if request.method == 'POST':
        empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
        fecha_inicio = request.POST['fecha'] + ' ' + request.POST['hora']
        estados = Estado.objects.filter(id_estado = 1)
        id_estado = None
        for es in estados:
            id_estado = es
        id_mascota = None
        id_empleado = None
        for em in empleado:
            id_empleado = em
        Cita(fecha_inicio = fecha_inicio, id_estado = id_estado, id_mascota = id_mascota, id_empleado = id_empleado).save()

    return HttpResponse(documento)

def HistoriaClinicaAct(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/historia_clinica_act.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    clientes = Cliente.objects.all()
    perfil = Perfil.objects.all()
    historias = HistoriaClinica.objects.all()
    citas = CitasDisponibles()
    mascota = MascotasRegistradas()
    citas_p = CitasProgramadas()
    citas_f = CitasFinalizadas()
    contexto = Context({"mascotas": mascota, "clientes": clientes, "empleados": empleado, "citas":citas, "perfiles": perfil, "citas_p": citas_p, "citas_f":citas_f, "historias":historias})

    documento = template.render(contexto)
    return HttpResponse(documento)

def HistoriaClinicaDet(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/historia_clinica_det.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)

def CitasFinalizadas():
    cliente = Cliente.objects.filter(nombre_cliente = cliente_actual)
    cliente_sel = None
    for c in cliente:
        cliente_sel = c
    mascota = Mascota.objects.filter(id_cliente = cliente_sel)
    mascota_sel = None
    for m in mascota:
        mascota_sel = m
    citas = Cita.objects.filter(id_estado = 3)
    return citas


def HistoriaClinicaM(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/historia_clinica.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    empleado = Empleado.objects.all()
    perfil = Perfil.objects.all()
    historias = HistoriaClinica.objects.all()
    citas = CitasDisponibles()
    mascota = MascotasActuales()
    citas_p = CitasProgramadas()
    citas_f = CitasFinalizadas()
    contexto = Context({"mascotas": mascota, "empleados": empleado, "citas":citas, "perfiles": perfil, "citas_p": citas_p, "citas_f":citas_f, "historias":historias})
    documento = template.render(contexto)
    return HttpResponse(documento)

def MenuCliente(request, cita):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/menu_cliente.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    cliente = Cliente.objects.filter(nombre_cliente = cliente_actual)
    mascota = Mascota.objects.filter(id_cliente = cliente)
    mascota_nombre = mascota[0].nombre_mascota
    contexto = Context({'mascota_nombre': mascota_nombre})
    documento = template.render(contexto)
    return HttpResponse(documento)

@csrf_exempt
def MenuMedico(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/menu_medico.html', encoding='utf-8')
    template = Template(plantilla.read())
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    perfil = Perfil.objects.all()
    clientes = Cliente.objects.all()
    mascotas = MascotasRegistradas()
    citas = CitasMedico()
    plantilla.close()
    contexto = Context({'empleados': empleado, 'perfiles': perfil, 'mascotas': mascotas, 'citas': citas, 'clientes':clientes})
    documento = template.render(contexto)
    if request.method == 'POST':
        cita = request.POST['cita']
        citas = Cita.objects.filter(id_cita = cita)
        cita_sel = None
        for ct in citas:
            cita_sel = ct
        global cita_actual
        cita_actual = cita_sel
        return redirect('seleccionar_cita')
    return HttpResponse(documento)

@csrf_exempt
def ModificarMascota(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/modificar_mascota.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)

@csrf_exempt
def PedirCitaMedico(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/pedir_cita_medico.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    clientes = Cliente.objects.all()
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    perfil = Perfil.objects.all()
    mascotas = MascotasRegistradas()
    citas = CitasDisponibles()
    citas_p = CitasProgramadas()
    contexto = Context({"mascotas": mascotas,'citas':citas, "empleados": empleado, "perfiles": perfil, "citas_p": citas_p, 'clientes':clientes})
    documento = template.render(contexto)
    return HttpResponse(documento)

@csrf_exempt
def Login(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/login.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    if request.method == 'POST':
        if request.POST['select'] == 'paciente':
            try:
                correo_cliente = request.POST['correo']
                contraseña_cliente = request.POST['contraseña']
                contraseña_desc = MensajeEncriptado('e',contraseña_cliente, 15)
                id_cliente = Cliente.objects.get(correo_cliente = correo_cliente, contrasena_cliente = contraseña_desc)
                global cliente_actual
                cliente_actual = id_cliente.nombre_cliente
                request.session['correo'] = id_cliente.correo_cliente
                messages.success(request, 'Funciona')
                return redirect("pedir_cita")
            except id_cliente.DoesNotExist as e:
                messages.success(request, 'Falló')
        else:
            try:
                correo_emp = request.POST['correo']
                contraseña_emp = request.POST['contraseña']
                contraseña_desc = MensajeEncriptado('e',contraseña_emp, 15)
                id_empleado = Empleado.objects.get(correo_emp = correo_emp, contrasena_emp = contraseña_desc)
                global empleado_actual
                empleado_actual = id_empleado.nombre_emp
                request.session['correo'] = id_empleado.correo_emp
                messages.success(request, 'Funciona')
                return redirect("menu_medico")
            except id_empleado.DoesNotExist as e:
                messages.success(request, 'Falló')


    return HttpResponse(documento)



def CitasDisponibles():
    cita = Cita.objects.filter(id_estado = 1)
    return cita

def CitasProgramadas():
    cliente = Cliente.objects.filter(nombre_cliente = cliente_actual)
    cliente_sel = None
    for c in cliente:
        cliente_sel = c
    mascota = Mascota.objects.filter(id_cliente = cliente_sel)
    mascota_sel = None
    for m in mascota:
        mascota_sel = m
    citas = Cita.objects.filter(id_estado = 2)
    return citas

def CitasMedico():
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    empleado_sel = None
    for em in empleado:
        empleado_sel = em
    citas = Cita.objects.filter(id_empleado = empleado_sel, id_estado = 2)
    return citas
    
def MascotasActuales():
    cliente = Cliente.objects.filter(nombre_cliente = cliente_actual)
    cliente_sel = None
    for c in cliente:
        cliente_sel = c
    mascota = Mascota.objects.filter(id_cliente = cliente_sel)
    return mascota
    
def MascotasRegistradas():
    mascotas = Mascota.objects.all()
    return mascotas

def Pedir(horario, request):
    cita = Cita.objects.filter(id_cita = horario.id_cita)
    cita.id_estado = 2
    cita.update() 

@csrf_exempt
def PedirCita(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/pedir_cita.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    print(cliente_actual)
    empleado = Empleado.objects.all()
    perfil = Perfil.objects.all()
    citas = CitasDisponibles()
    mascota = MascotasActuales()
    citas_p = CitasProgramadas()
    contexto = Context({"mascotas": mascota, "empleados": empleado, "citas":citas, "perfiles": perfil, "citas_p": citas_p})
    documento = template.render(contexto)    
    if request.method == 'POST':
        print(cliente_actual)
        x = request.POST.get('citas_dis',False)
        mascota_sel = request.POST.get('masc_cita',False)
        mascota1 = Mascota.objects.filter(nombre_mascota = mascota_sel)
        masc_sel = None
        cita1 = Cita.objects.filter(id_cita = x)
        cita_sel = None
        estado = Estado.objects.filter(id_estado = 2)
        estado_sel = None
        for m in mascota1:
            masc_sel = m
        for c in cita1:
            cita_sel = c
        for e in estado:
            estado_sel = e
        cita_sel.id_mascota = masc_sel
        cita_sel.id_estado = estado_sel
        cita_sel.save()
    return HttpResponse(documento)

@csrf_exempt
def SeleccionarCita(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/seleccionar_cita.html', encoding='utf-8')
    template = Template(plantilla.read())
    cita = cita_actual
    mascotas = MascotasRegistradas()
    empleado = Empleado.objects.filter(nombre_emp = empleado_actual)
    clientes = Cliente.objects.all()
    perfil = Perfil.objects.all()
    plantilla.close()
    contexto = Context({'cita':cita, 'mascotas':mascotas, 'empleados':empleado, 'perfiles':perfil, 'clientes':clientes})
    documento = template.render(contexto)
    if request.method == 'POST':
        cita = request.POST['cita']
        citas = Cita.objects.filter(id_cita = cita)
        cita_sel = None
        for ct in citas:
            cita_sel = ct
        hc_descripcion = request.POST['descripcion']
        hc_tratamiento = request.POST['tratamiento']
        HistoriaClinica(descripcion = hc_descripcion, tratamiento = hc_tratamiento,id_cita = cita_sel).save()
        estado_sel = None
        estados = Estado.objects.filter(id_estado = 3)
        for es in estados:
            estado_sel = es
        cita_sel.id_estado = estado_sel
        cita_sel.save()


    return HttpResponse(documento)

def SeleccionarPaciente(request):
    plantilla = open('C:/Users/sebas/Desktop/VETUD_Py/VETUD_Py/templates/seleccionar_paciente.html', encoding='utf-8')
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    documento = template.render(contexto)
    return HttpResponse(documento)




