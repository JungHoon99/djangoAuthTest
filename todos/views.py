from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
import rules

from .models import Todo
from .serializers import TodoSerializer


class TodoAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def retrieve(self, request, *args, **kwargs):
        todo = Todo.objects.get(pk=self.kwargs['pk'])
        print(rules.has_perm('can_view_todo', request.user, todo))
        return super().retrieve(request, *args, **kwargs)
