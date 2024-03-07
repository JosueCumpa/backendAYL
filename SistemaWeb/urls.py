from django.urls import path, include
from . views import  UserViewSet, GrifoViewSet,GrifoView,ListadoRendimientoView,TraspasosViewSet,ListadoDataPendienteView,ProductoViewSet, ConductorViewSet,RendimientoViewSet, CamionViewSet,BancoViewSet, ConductoresActivosView,DataGeneralViewSet, ListadoNombresView, CamionView,MaxKilometrajeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"usuarios", UserViewSet, basename="usuarios")
router.register(r"Grifo", GrifoViewSet, basename="Grifo")
router.register(r"Producto",ProductoViewSet, basename="Producto")
router.register(r"Conductor",ConductorViewSet,basename="Conductor")
router.register(r'Camion',CamionViewSet,basename="Camion")
router.register(r'DataGeneral',DataGeneralViewSet, basename="DataGeneral")
router.register(r'Banco', BancoViewSet, basename="Bancos")
router.register(r'Rendimiento', RendimientoViewSet, basename="Rendimiento")
router.register(r'traspasos',TraspasosViewSet, basename="Traspasos")

urlpatterns = [ 
    path("", include(router.urls)),
    path("conductores-activos/", ConductoresActivosView.as_view(), name="conductores-activos"),
    path('listado_nombres/', ListadoNombresView.as_view(), name='listado_nombres'),
    path('listado_camion/', CamionView.as_view(), name='listado_camion'),
    path('grifo_activos/', GrifoView.as_view(), name= "grifo_activos"),
    path('maxKM/', MaxKilometrajeView.as_view(), name= "maxKM"),
    path('listado_rendimiento/', ListadoRendimientoView.as_view(), name= "listado_rendimiento"),
    path('listado_datapendiente/', ListadoDataPendienteView.as_view(), name= "listado_datapendiente"),
]