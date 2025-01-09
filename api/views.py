from django.shortcuts import render

 # Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'data'

    def get(self, request):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
		    
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)

    
    def post(self, request):
	        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
	        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
	        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

class DetailedLandingAPI(APIView):
    name = 'DETAILED Landing API'

    # Coloque el nombre de su colección en el Realtime Database
    collection_name = 'data'
    def get (self, request, pk):
        """Obtiene un elemento específico identificado por pk."""
        try:
            # Referencia al elemento con la clave primaria (pk)
            ref = db.reference(f'{self.collection_name}/{pk}')

            # Obtiene los datos del elemento
            data = ref.get()

            # Si no se encuentra, devolver un error 404
            if not data:
                return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)

            # Devuelve el elemento encontrado
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            # Manejo de errores generales
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            ref = db.reference(f'{self.collection_name}/{pk}')
            data = ref.get()
            if not data:
                return Response({"error": "Item not Found"}, status=status.HTTP_404_NOT_FOUND)
            ref.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        # Validar que el cuerpo de la solicitud (request.data) contenga los campos necesarios para la actualización.
        required_fields = ["email"]

        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            #    Obtener la referencia al documento con el pk
            doc_ref = db.collection(self.collection_name).document(pk)
            doc = doc_ref.get()

            # Verificar si el documento existe
            if not doc.exists:
                return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

            # Actualizar el documento con los nuevos datos
            doc_ref.update(request.data)

            return Response({'message': 'Document updated successfully'}, status=status.HTTP_200_OK)

        except cloud_firestore.NotFound:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
