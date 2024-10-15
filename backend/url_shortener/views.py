from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortURL
from .serializers import ShortURLSerializer

class ShortURLView(APIView):
    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data['url']
            existing_url = ShortURL.objects.filter(url=original_url).first()
            if existing_url:
                return Response({'short_url': request.build_absolute_uri(f'/{existing_url.short_url}')})

            short_url = ShortURL.generate_short_url()
            shortened_url = ShortURL.objects.create(url=original_url, short_url=short_url)
            return Response({'short_url': request.build_absolute_uri(f'/{short_url}')})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def redirect_to_original(request, short_url):
    try:
        shortened_url = ShortURL.objects.get(short_url=short_url)
        shortened_url.visits_count += 1
        shortened_url.save()
        return redirect(shortened_url.url)
    except ShortURL.DoesNotExist:
        return Response({'error': 'URL not found'}, status=status.HTTP_404_NOT_FOUND)
