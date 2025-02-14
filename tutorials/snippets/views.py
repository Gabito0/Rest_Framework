# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#   """
#   List all code snippets, or create a new snippet.
#   """
#   if request.method == 'GET':
#     snippets = Snippet.objects.all()
#     serializer = SnippetSerializer(snippets,many=True)
#     return Response(serializer.data)
  
#   elif request.method == 'POST':
#     serializer = SnippetSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#   """
#   Retrieve, update, or delete a code snippet.
#   """
#   try:
#     snippet = Snippet.objects.get(pk=pk)
#   except Snippet.DoesNotExist:
#     return Response(status=status.HTTP_404_NOT_FOUND)
  
#   if request.method == 'GET':
#     serializer = SnippetSerializer(snippet)
#     return Response(serializer.data)
  
#   elif request.method == 'PUT':
#     serializer = SnippetSerializer(snippet, data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#   elif request.method == 'DELETE':
#     snippet.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


###########################Refactoring both views with classed base views.###################################

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  """
  List all snippets, or create a snippet.
  """
  queryset = Snippet.objects.all()

  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  
  def post(self, request,*args, **kwargs):
    return self.create(request, *args, **kwargs)
  
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
  """
  Retrieve, update or delete a snippet instance.
  """
  queryset = Snippet.objects.all()
  serializer_class  = SnippetSerializer

  def get(self, request, *args, **kwargs):
    return self.retrieve(request, *args, **kwargs)
  
  def put(self, request, *args, **kwargs):
    return self.update(request, *args, **kwargs)
  
  def delete(self, request, *args, **kwargs):
    return self.delete(request, *args, **kwargs)

  # def get_object(self, pk):
  #   try:
  #     return Snippet.objects.get(pk=pk)
  #   except Snippet.DoesNotExist:
  #     raise Http404
    
  # def get(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   serializer = SnippetSerializer(snippet)
  #   return Response(serializer.data)
  
  # def put(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   serializer = SnippetSerializer(snippet, data=request.data)
  #   if serializer.is_valid():
  #     serializer.save()
  #     return Response(serializer.data)
  #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # def delete(self, request, pk, format=None):
  #   snippet = self.get_object(pk)
  #   snippet.delete()
  #   return Response(status=status.HTTP_204_NO_CONTENT)

#### Using Generic classed-base views

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework  import permissions
from snippets.permission import isOwnerorReadyOnly
from rest_framework import viewsets
from rest_framework.decorators import action

# class SnippetList(generics.ListCreateAPIView):
#   permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#   def perform_create(self, serializer):
#     serializer.save(owner=self.request.user)

#   queryset = Snippet.objects.all()
#   serializer_class = SnippetSerializer

# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView, isOwnerorReadyOnly):
#   permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#   queryset = Snippet.objects.all()
#   serializer_class = SnippetSerializer


####################Creating views for User


# class UserList(generics.ListAPIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

# Refactoring out UserList and UserDetail classes into a signle UserViewSet

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides `list` and `retrieve` actions.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

################### Creating endpoint for the root of our API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users':reverse('user-list', request=request, format=format),
    'snippets':reverse('snippet-list', request=request, format=format)
  })

# class SnippetHighlight(generics.GenericAPIView):
#   queryset = Snippet.objects.all()
#   renderer_classes = [renderers.StaticHTMLRenderer]

#   def get(self, request, *args, **kwargs):
#     snippet = self.get_object()
#     return Response(snippet.highlighted)


class SnippetViewSet(viewsets.ModelViewSet):
  """
  This ViewSet automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

  Additionally we also provide an extra `highlight` action.
  """

  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = [permissions.IsAuthenticatedOrReadOnly, isOwnerorReadyOnly]

  @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
  def highlight(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)
  
  def perform_create(self,serializer):
    serializer.save(owner=self.request.user)