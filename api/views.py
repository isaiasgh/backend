from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
    name = 'Landing API'
    collection_name = 'collection'

    def get(self, request, pk=None):
        """Obtiene todos los elementos o uno específico."""
        try:
            if pk:
                ref = db.reference(f'{self.collection_name}/{pk}')
                data = ref.get()
                if not data:
                    return Response({"error": "Elemento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                ref = db.reference(f'{self.collection_name}')
                data = ref.get()
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
        required_fields = ["email"]

        for field in required_fields:
            if field not in request.data:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ref = db.reference(f'{self.collection_name}/{pk}')
            data = ref.get()

            if not data:
                return Response({'error': 'Element not found'}, status=status.HTTP_404_NOT_FOUND)

            ref.update(request.data)

            return Response({'message': 'Element updated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)