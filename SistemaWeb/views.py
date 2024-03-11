from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from . serializers import UserSerializer, GrifoSerializer,ProductoSerializer,TraspasosSerializer,ciudadSerializer,RendimientoSerializer ,ConductoSerializer,BancoSerializer, CamionSerializer, DataGeneralSerializer
from .models import Grifo,Producto, Conductor, Camion, DataGeneral, Banco, Rendimiento, traspasos, ciudad
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.views import APIView

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data.get('username'))

        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {
                "user_data": {
                    "name": user.first_name + " " + user.last_name,
                    "group": "true" if user.is_superuser else "false",
                    "op": "true" if user.is_staff else "false",
                },
                "tokens": serializer.validated_data,
            },
            status=status.HTTP_200_OK,
        )


class GrifoViewSet(viewsets.ModelViewSet):
    queryset = Grifo.objects.all()
    serializer_class = GrifoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class GrifoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        grifo_activos = Grifo.objects.filter(estado=True)
        serializer = GrifoSerializer(grifo_activos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all().order_by('nombre')
    serializer_class= ConductoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class ciudadViewSet(viewsets.ModelViewSet):
    queryset = ciudad.objects.all().order_by('nombre')
    serializer_class = ciudadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

#listado conductores activo (apiview para solo invocar un get ... el otro es para que te de un crud completo viewsets.ModelViewSet)
class ConductoresActivosView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        conductores_activos = Conductor.objects.filter(estado=True)
        serializer = ConductoSerializer(conductores_activos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CamionViewSet(viewsets.ModelViewSet):
    queryset = Camion.objects.all()
    serializer_class= CamionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class CamionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        camion_activos = Camion.objects.filter(estado=True)
        serializer = CamionSerializer(camion_activos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class DataGeneralViewSet(viewsets.ModelViewSet):
    queryset = DataGeneral.objects.all()
    serializer_class= DataGeneralSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ListadoNombresView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data_generales = DataGeneral.objects.all()
        result = []

        for data_general in data_generales:
            grifo_serializer = GrifoSerializer(Grifo.objects.get(pk=data_general.grifo.id))
            producto_serializer = ProductoSerializer(Producto.objects.get(pk=data_general.producto.id))
            conductor_serializer = ConductoSerializer(Conductor.objects.get(pk=data_general.conductor.id))
            camion_serializer = CamionSerializer(Camion.objects.get(pk= data_general.placa.id))
            rendimiento_data = {}
            rendimiento_instance = Rendimiento.objects.filter(id_datageneral=data_general.id).first()
            if rendimiento_instance:
                rendimiento_serializer = RendimientoSerializer(rendimiento_instance)
                rendimiento_data = rendimiento_serializer.data



            placa_traspaso = None
            if data_general.traspaso_id:
                placa_traspaso = camion_serializer.data['placa']
                
            else: 
                placa_traspaso= "vacio"

            result.append({
                "id": data_general.id,
                "fecha_creacion": data_general.fecha_creacion,
                "fecha_actualizacion": data_general.fecha_actualizacion,
                "traspaso": data_general.traspaso_id,
                "placa": data_general.placa.id,
                "placa_traspaso": placa_traspaso,
                "placa_nombre": camion_serializer.data['placa'],
                "conductor": data_general.conductor.id,
                "conductor_nombre": conductor_serializer.data['nombre'],
                "conductor_apellido": conductor_serializer.data['apellido'],
                "galones": data_general.galones,
                "producto": data_general.producto.id,
                "producto_nombre": producto_serializer.data['nombre'],
                "documento": data_general.documento,
                "precio": data_general.precio,
                "total": data_general.total,
                "kilometraje": data_general.kilometraje,
                "grifo": data_general.grifo.id,
                "grifo_nombre": grifo_serializer.data['nombre'],
                "cantidad_traspaso": data_general.cantidad_traspaso,
                "Monto_Transpaso":data_general.Monto_Transpaso,
                "estado" : data_general.estado,
                "detalle": data_general.detalle,
                "observacion": data_general.observacion,
                "estado_rendimiento": data_general.estado_rendimiento,
                "estado_omitir": data_general.estado_omitir,
                # "origen" : data_general.origen,
                # "destino": data_general.destino,
                # "carga": data_general.carga,
                # "peso": data_general.peso,  
                "rendimiento": rendimiento_data
            })

        return Response(result)

class ListadoDataPendienteView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        placa_camion = request.query_params.get('placa', None)

        if not placa_camion:
            return Response({"error": "Se requiere especificar la placa del camión."}, status=400)

        data_generales = DataGeneral.objects.filter(estado_rendimiento=False, placa__placa=placa_camion)

        result = []

        for data_general in data_generales:
            grifo_serializer = GrifoSerializer(Grifo.objects.get(pk=data_general.grifo.id))
            producto_serializer = ProductoSerializer(Producto.objects.get(pk=data_general.producto.id))
            conductor_serializer = ConductoSerializer(Conductor.objects.get(pk=data_general.conductor.id))
            camion_serializer = CamionSerializer(Camion.objects.get(pk=data_general.placa.id))
            rendimiento_data = {}
            rendimiento_instance = Rendimiento.objects.filter(id_datageneral=data_general.id).first()
            if rendimiento_instance:
                rendimiento_serializer = RendimientoSerializer(rendimiento_instance)
                rendimiento_data = rendimiento_serializer.data

            placa_traspaso = camion_serializer.data['placa'] if data_general.traspaso_id else "vacio"

            result.append({
                "id": data_general.id,
                "fecha_creacion": data_general.fecha_creacion,
                "fecha_actualizacion": data_general.fecha_actualizacion,
                "traspaso": data_general.traspaso_id,
                "placa": data_general.placa.id,
                "placa_traspaso": placa_traspaso,
                "placa_nombre": camion_serializer.data['placa'],
                "conductor": data_general.conductor.id,
                "conductor_nombre": conductor_serializer.data['nombre'],
                "conductor_apellido": conductor_serializer.data['apellido'],
                "galones": data_general.galones,
                "producto": data_general.producto.id,
                "producto_nombre": producto_serializer.data['nombre'],
                "documento": data_general.documento,
                "precio": data_general.precio,
                "total": data_general.total,
                "kilometraje": data_general.kilometraje,
                "grifo": data_general.grifo.id,
                "grifo_nombre": grifo_serializer.data['nombre'],
                "cantidad_traspaso": data_general.cantidad_traspaso,
                "Monto_Transpaso": data_general.Monto_Transpaso,
                "estado": data_general.estado,
                "detalle": data_general.detalle,
                "observacion": data_general.observacion,
                "estado_rendimiento": data_general.estado_rendimiento,
                "estado_omitir": data_general.estado_omitir,
                # "origen": data_general.origen,
                # "destino": data_general.destino,
                # "carga": data_general.carga,
                # "peso": data_general.peso,
                "rendimiento": rendimiento_data
            })

        return Response(result)


class ListadoRendimientoView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rendimientos = Rendimiento.objects.all()
        result = []

        for rendimiento in rendimientos:
            data_general = rendimiento.id_datageneral
            grifo_serializer = GrifoSerializer(data_general.grifo)
            producto_serializer = ProductoSerializer(data_general.producto)
            conductor_serializer = ConductoSerializer(data_general.conductor)
            camion_serializer = CamionSerializer(data_general.placa)
            
            placa_traspaso = camion_serializer.data['placa'] if data_general.traspaso_id else "vacio"

            result.append({
                "id": rendimiento.id,
                "fecha_rendimiento": rendimiento.fecha_tanqueo,
                "id_data_general": data_general.id,
                "rend_kmxglp": rendimiento.rend_kmxglp,
                "ren_esperado": rendimiento.ren_esperado,
                "gl_esperado": rendimiento.gl_esperado,
                "km_recorrido": rendimiento.km_recorrido,
                "año": rendimiento.año,
                "periodo": rendimiento.periodo,
                "exceso_real": rendimiento.exceso_real,
                "fecha_creacion": data_general.fecha_creacion,
                "fecha_actualizacion": data_general.fecha_actualizacion,
                "traspaso": data_general.traspaso_id,
                "placa": data_general.placa.id,
                "placa_traspaso": placa_traspaso,
                "placa_nombre": camion_serializer.data['placa'],
                "conductor": data_general.conductor.id,
                "conductor_nombre": conductor_serializer.data['nombre'],
                "conductor_apellido": conductor_serializer.data['apellido'],
                "galones": data_general.galones,
                "producto": data_general.producto.id,
                "producto_nombre": producto_serializer.data['nombre'],
                "documento": data_general.documento,
                "precio": data_general.precio,
                "total": data_general.total,
                "kilometraje": data_general.kilometraje,
                "grifo": data_general.grifo.id,
                "grifo_nombre": grifo_serializer.data['nombre'],
                "cantidad_traspaso": data_general.cantidad_traspaso,
                "Monto_Transpaso": data_general.Monto_Transpaso,
                "estado": data_general.estado,
                "detalle": data_general.detalle,
                "observacion": data_general.observacion,
                "estado_rendimiento": data_general.estado_rendimiento,
                "estado_omitir": data_general.estado_omitir,
                "origen": rendimiento.origen,
                "destino": rendimiento.destino,
                "carga": rendimiento.carga,
                "peso": rendimiento.peso,
            })

        return Response(result)

class BancoViewSet(viewsets.ModelViewSet):
    queryset = Banco.objects.all()
    serializer_class = BancoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class RendimientoViewSet(viewsets.ModelViewSet):
    queryset = Rendimiento.objects.all()
    serializer_class = RendimientoSerializer

class TraspasosViewSet(viewsets.ModelViewSet):
    queryset = traspasos.objects.all()
    serializer_class = TraspasosSerializer

class MaxKilometrajeView(APIView):
    def get(self, request, *args, **kwargs):
        # Obtener la placa de la petición GET
        placa = request.GET.get('placa', None)
        if placa is not None:
            # Filtrar los registros de DataGeneral por placa y estado de rendimiento verdadero
            data_generales = DataGeneral.objects.filter(placa__placa=placa, estado_rendimiento=True)
            if len(data_generales)>0:
                max_kilometraje = data_generales.aggregate(max_kilometraje=models.Max('kilometraje'))['max_kilometraje']
                return Response({'max_kilometraje': max_kilometraje})
            else:
                data_generales = DataGeneral.objects.filter(placa__placa=placa)
                max_kilometraje = data_generales.aggregate(max_kilometraje=models.Max('kilometraje'))['max_kilometraje']
                return Response({'max_kilometraje': max_kilometraje})
        else:
            return Response({'error': 'Debe proporcionar el parámetro placa en la solicitud GET'})
        
