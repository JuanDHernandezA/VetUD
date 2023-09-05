"""VETUD_Py URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from VETUD_Py.views import PaginaPrincipal
from VETUD_Py.views import AgendarCita
from VETUD_Py.views import HistoriaClinicaAct
from VETUD_Py.views import HistoriaClinicaDet
from VETUD_Py.views import HistoriaClinicaM
from VETUD_Py.views import MenuCliente
from VETUD_Py.views import MenuMedico
from VETUD_Py.views import ModificarMascota
from VETUD_Py.views import PedirCita
from VETUD_Py.views import PedirCitaMedico
from VETUD_Py.views import SeleccionarCita
from VETUD_Py.views import SeleccionarPaciente
from VETUD_Py.views import RegistroEmpleado
from VETUD_Py.views import RegistroUsuario
from VETUD_Py.views import RegistroMascota
from VETUD_Py.views import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agendar_cita/', AgendarCita, name="agendar_cita"),
    path('historia_clinica_act/', HistoriaClinicaAct, name="historia_clinica_act"),
    path('historia_clinica_det/', HistoriaClinicaDet, name="historia_clinica_det"),
    path('historia_clinica/', HistoriaClinicaM, name="historia_clinica"),
    path('menu_medico/', MenuMedico, name="menu_medico"),
    path('pedir_cita/', PedirCita, name="pedir_cita"),
    path('pedir_cita_medico/', PedirCitaMedico, name="pedir_cita_medico"),
    path('seleccionar_cita/', SeleccionarCita, name="seleccionar_cita"),
    path('seleccionar_paciente/', SeleccionarPaciente, name="seleccionar_paciente"),
    path('', PaginaPrincipal, name="index"),
    path('reg_emp/', RegistroEmpleado, name="reg_emp"),
    path('reg_usr/', RegistroUsuario, name="reg_usr"),
    path('reg_mas/', RegistroMascota, name="reg_mas"),
    path('login/', Login, name="login")
    ]
