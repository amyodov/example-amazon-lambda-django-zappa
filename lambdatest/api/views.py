from .serializers import HumanSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status

from .humans import Human

_HUMANS = {
    1: Human('John', 'Doe'),
    2: Human('Jane', 'Doe'),
}


class HumanViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    def list(self, request):
        humans = _HUMANS.values()
        serializer = HumanSerializer(humans, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        human = _HUMANS.get(int(pk))
        if human is None:
            raise Http404
        serializer = HumanSerializer(human)
        return Response(serializer.data)
    
    def get_queryset(self):
        return None
