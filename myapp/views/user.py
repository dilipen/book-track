from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, generics
from rest_framework.response import Response

from myapp import serializers
from myapp import models
from myapp.core.pagination import CustomPagination

from django.contrib.auth import logout as _logout
from django.contrib.auth.hashers import make_password

from django.shortcuts import render, redirect


class UserCreateList(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):

    permission_classes = ()

    def get_queryset(self):
        return models.User.objects.order_by('id').all()

    def filter_queryset(self, queryset):
        q = Q()

        return queryset.filter(q)

    def get_serializer_class(self):
        return serializers.UserSerializer

    def get_pagination_class(self, request):
        return CustomPagination

    def get(self, request):
        # queryset = self.filter_queryset(self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        data = request.data
        if type(data) is not dict:
            data._mutable = True
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = serializer_class(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetriveUpdateDelete(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    permission_classes = ()

    def get_queryset(self):
        return models.User.objects.all()

    def filter_queryset(self, queryset):
        q = Q()

        return queryset.filter(q)

    def get_object(self, user):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        model = get_object_or_404(queryset, id=user)
        return model

    def get_serializer_class(self):
        return serializers.UserSerializer

    def get(self, request, user):
        model = self.get_object(user)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(model)
        return Response(serializer.data)

    def put(self, request, user):
        model = self.get_object(user)
        serializer_class = self.get_serializer_class()
        data = request.data
        if type(data) is not dict:
            data._mutable = True
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = serializer_class(model, data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user):
        model = self.get_object(user)
        model.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)


def logout(request):
    try:
        _logout(request)
    except:
        return redirect('/api-auth/login/')
    return redirect('/api-auth/login/')