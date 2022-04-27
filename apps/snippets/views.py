from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from GameBackend.permissions import IsAdminOrCreator, SnippetListPermission
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    authentication_classes = [TokenAuthentication, SessionAuthentication] #Authentification allowed with Session or Token Auth
    permission_classes = [SnippetListPermission] #Normal User is allowed to do a POST, Admin can do anything (including get)
                                                 #SnippetListPermission is written in 'GameBackend/permissions' file
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs): #Get request -> return the users list
        return self.list(request, *args, **kwargs)

    def post(self, request, format=None): #post -> save snippet and the snippet id. 
        if not self.request.user.profile.snippetID:
            serializer = SnippetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                self.request.user.profile.snippetID = serializer.data['id']
                self.request.user.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("invalid request, snippet already exists at snippets/{}".format(self.request.user.profile.snippetID), status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    #Normal User should is allowed to see and change the snippet if he is the creator
                                         
    permission_classes = [IsAdminOrCreator] #Acces for Admin or the creator of the snippet
    authentication_classes = [TokenAuthentication, SessionAuthentication] #Authentification allowed with Session or Token Auth
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((TokenAuthentication, SessionAuthentication))
def game(request): #highscore view (function Based)
    if request.GET.get('highscore') == "":
        all_objects = Snippet.objects.all()
        all_highscores = all_objects.values_list('owner', 'highscore').order_by('-highscore')
        owner_rel_hs = []
        for x in all_highscores:
            if x[1] is not None:
                owner_rel_hs.append([resolveUserId(x[0]), x[1]])
       
        return Response({"data": owner_rel_hs})
    
    else:
        return HttpResponseBadRequest("Wrong keyword")
 
 
def resolveUserId(id):
    return str(get_object_or_404(User, pk=id))