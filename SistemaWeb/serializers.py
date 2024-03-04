from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Grifo, Producto, Conductor, Camion, DataGeneral, Banco, Rendimiento



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["id", "username", "password", "is_active", "first_name", "last_name","is_superuser","is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
            # Validar first_name y last_name antes de la creación
            #dni= validated_data["dni"]
        username = validated_data.get('username')
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        # if not dni:
        #     raise serializers.ValidationError("El campo 'dni' no puede estar vacío.")

        if not first_name:
            raise serializers.ValidationError("El campo 'first_name' no puede estar vacío.")

        if not last_name:
            raise serializers.ValidationError("El campo 'last_name' no puede estar vacío.")

        if not username:
            raise serializers.ValidationError("El campo 'username' no puede estar vacío.")

        

        # Continuar con la creación del usuario
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        
        first_name = validated_data.get("first_name", instance.first_name)
        last_name = validated_data.get("last_name", instance.last_name)

    

        if not first_name:
            raise serializers.ValidationError("El campo 'first_name' no puede estar vacío.")

        if not last_name:
            raise serializers.ValidationError("El campo 'last_name' no puede estar vacío.")

        # Actualizar los campos relevantes del usuario
        instance.username = validated_data.get("username", instance.username)
        instance.last_name = last_name
        instance.first_name = first_name
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
      
        # Establecer una nueva contraseña si se proporciona en la solicitud
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        # Guardar los cambios
        instance.save()

        return instance
    

class GrifoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Grifo
        fields = ["id","nombre","fecha_actualizacion","precio","estado"]

        def create(self, validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
            
            Grifo = Grifo.objects.create_grifo(**validated_data)
            return Grifo
        
        def update(self, instance, validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
                #Actualizar los campos relevantes
            instance.nombre = validated_data.get("nombre", instance.nombre)
            instance.precio = validated_data.get("precio", instance.precio)
            instance.estado = validated_data.get("estado", instance.estado)
            instance.save()
            return instance
        
class ProductoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id","nombre","estado"]

        def create(self, validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
            
            Producto = Producto.objects.create_Producto(**validated_data)
            return Producto
        
        def update(self, instance, validated_data):
            nombre = validated_data.get('nombre')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacío.")
                #Actualizar los campos relevantes
            instance.nombre = validated_data.get("nombre", instance.nombre)
            instance.estado = validated_data.get("estado", instance.estado)
            instance.save()
            return instance

class ConductoSerializer (serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ["id","nombre","apellido","estado"]

        def create(self, validated_data):
            nombre = validated_data.get('nombre')
            apellido = validated_data.get('apellido')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacio")
            
            if not apellido:
                raise serializers.ValidationError("El campo apellidos no puede estar vacio")
            Conductor = Conductor.objects.create_Conductor(**validated_data)
            return Conductor
        
        def update(self, instance, validated_data):
            nombre = validated_data.get('nombre')
            apellido = validated_data.get('apellido')
            if not nombre:
                raise serializers.ValidationError("El campo 'nombre' no puede estar vacio")
            
            if not apellido:
                raise serializers.ValidationError("El campo apellido no puede estar vacio")
            instance.nombre = validated_data.get("nombre", instance.nombre)
            instance.apellido = validated_data.get("apellido", instance.estado)
            instance.estado = validated_data.get("estado", instance.estado)
            instance.save()
            return instance

class CamionSerializer(serializers.ModelSerializer):
    conductor_id = serializers.IntegerField(write_only=True)
    nombre_apellido_conductor = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Camion
        fields = ['id', 'placa', 'estado', 'conductor_id', 'nombre_apellido_conductor','fecha_actualizacion']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['conductor_id'] = instance.conductor.id if instance.conductor else None
        representation['nombre_apellido_conductor'] = instance.conductor.get_nombre_apellido() if instance.conductor else None
        return representation

    def create(self, validated_data):
        conductor_id = validated_data.pop('conductor_id', None)

        if conductor_id is None:
            raise serializers.ValidationError("El campo conductor_id es obligatorio.")

        try:
            conductor_instance = Conductor.objects.get(id=conductor_id)
        except Conductor.DoesNotExist:
            raise serializers.ValidationError("El conductor especificado no existe.")

        camion_instance = Camion.objects.create(conductor=conductor_instance, **validated_data)
        return camion_instance

    def update(self, instance, validated_data):
        conductor_id = validated_data.pop('conductor_id', None)

        if conductor_id is not None:
            try:
                conductor_instance = Conductor.objects.get(id=conductor_id)
            except Conductor.DoesNotExist:
                raise serializers.ValidationError("El conductor especificado no existe.")
            instance.conductor = conductor_instance

        instance.placa = validated_data.get('placa', instance.placa)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()

        return instance

    def get_nombre_apellido_conductor(self, instance):
        return instance.conductor.get_nombre_apellido() if instance.conductor else None

class DataGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataGeneral
        fields = [
            'id',
            'fecha_creacion',
            'fecha_actualizacion',
            'traspaso_id',
            'cantidad_traspaso',
            'Monto_Transpaso',
            'placa',
            'conductor',
            'galones',
            'producto',
            'documento',
            'precio',
            'total',
            'kilometraje',
            'grifo',
            'estado',
            'detalle',
            'observacion',
            'estado_rendimiento',
        ]

    def create(self, validated_data):
        return DataGeneral.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.fecha_creacion = validated_data.get('fecha_creacion', instance.fecha_creacion)
        instance.traspaso_id= validated_data.get('traspaso_id',instance.traspaso_id)
        instance.cantidad_traspaso= validated_data.get('cantidad_traspaso', instance.cantidad_traspaso)
        instance.Monto_Transpaso = validated_data.get('Monto_Transpaso', instance.Monto_Transpaso)
        instance.placa = validated_data.get('placa', instance.placa)
        instance.conductor = validated_data.get('conductor', instance.conductor)
        instance.galones = validated_data.get('galones', instance.galones)
        instance.producto = validated_data.get('producto', instance.producto)
        instance.documento = validated_data.get('documento', instance.documento)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.kilometraje = validated_data.get('kilometraje', instance.kilometraje)
        instance.grifo = validated_data.get('grifo', instance.grifo)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.detalle = validated_data.get('detalle', instance.detalle)
        instance.observacion = validated_data.get('observacion', instance.observacion)
        # Recalcula el campo 'total' basándose en los nuevos valores
        instance.total = validated_data.get('total', instance.total)
        instance.estado_rendimiento = validated_data.get('estado_rendimiento', instance.estado_rendimiento)

        instance.save()
        return instance
    

class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banco
        fields= [
            'id',
            'nombre',
            'abreviatura',
            'estado',
        ]
    
    def create(self, validated_data):
        return Banco.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre= validated_data.get('nombre',instance.nombre)
        instance.abreviatura= validated_data.get('abreviatura', instance.abreviatura)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.save()
        return instance
    
class RendimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rendimiento
        fields = '__all__'

    def create(self, validated_data):
        # Crea una nueva instancia de Rendimiento con los datos validados
        rendimiento = Rendimiento.objects.create(**validated_data)
        return rendimiento

    def update(self, instance, validated_data):
        # Actualiza una instancia existente de Rendimiento con los datos validados
        instance.id_datageneral = validated_data.get('id_datageneral', instance.id_datageneral)
        instance.fecha_tanqueo = validated_data.get('fecha_tanqueo', instance.fecha_tanqueo)
        instance.año = validated_data.get('año', instance.año)
        instance.periodo = validated_data.get('periodo', instance.periodo)
        instance.ruta = validated_data.get('ruta', instance.ruta)
        instance.carga = validated_data.get('carga', instance.carga)
        instance.peso = validated_data.get('peso', instance.peso)
        instance.km_recorrido = validated_data.get('km_recorrido', instance.km_recorrido)
        instance.rend_kmxglp = validated_data.get('rend_kmxglp', instance.rend_kmxglp)
        instance.gl_esperado = validated_data.get('gl_esperado', instance.gl_esperado)
        instance.ren_esperado = validated_data.get('ren_esperado', instance.ren_esperado)
        instance.exceso_real = validated_data.get('exceso_real', instance.exceso_real)
        instance.save()
        return instance