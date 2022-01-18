from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.status import HTTP_203_NON_AUTHORITATIVE_INFORMATION
from rest_framework.response import Response
from news_app.serializers import *
from news_app.models import *
from rest_framework import viewsets
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `user`.
        return obj.user == request.user


class CompanyViewSet(viewsets.ModelViewSet):

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


class CompaniesDetailsViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = CompaniesDetailsSerializer


class MyCompanyPostsViewSet(viewsets.ModelViewSet):

    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user__company_id=self.request.user.company_id)


class UserMeViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserBigSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'id': self.request.user.id}
        return get_object_or_404(queryset, **filter_kwargs)

    def get_me(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)


class UserDetailViewSet(viewsets.ModelViewSet):

    serializer_class = UserBigSerializer
    lookup_field = 'id'

    def get_queryset(self):
#        return User.objects.all()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return User.objects.all()
            elif self.request.user.is_authenticated:
                return User.objects.filter(id=self.request.user.id)
        return User.objects.none()

    def my_create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(status=status.HTTP_201_CREATED)


class UserViewSet(UserDetailViewSet):

    serializer_class = CompanyUserSmallSerializer


class PostViewSet(CompanyViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = (IsAdminUser | IsOwner)

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_authenticated or self.request.user.is_superuser:
            return super().retrieve(self, request, *args, **kwargs)

    def filter_queryset(self, queryset):
        text = self.request.query_params.get('text')
        company_id = self.request.query_params.get('company_id')
        title = self.request.query_params.get('title')
        topic = self.request.query_params.get('topic')
        if text is not None:
            queryset = queryset.filter(text=text)
        if title is not None:
            queryset = queryset.filter(title=title)
        if topic is not None:
            queryset = queryset.filter(topic=topic)
        if company_id is not None:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().create(self, request, *args, **kwargs)


class WhoAmI(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return Response(data={"status": "superuser"})
        elif request.user.is_superuser:
            return Response(data={"status": "admin"})
        elif request.user.is_authenticated:
            return Response(data={"status": "user"})
        else:
            return Response(data={"status": "unauthorized"})
