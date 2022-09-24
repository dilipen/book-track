from django.http import Http404
from rest_framework import mixins
from rest_framework import status, generics
from rest_framework.response import Response

from myapp import models
from myapp import serializers
from myapp.core.pagination import CustomPagination


class UploadFileCreateListView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):

    permission_classes = ()

    def get_queryset(self):
        return models.UploadFile.objects.order_by('id').all()

    def filter_queryset(self, request, queryset):
        return self.get_queryset()

    def get_serializer_class(self):
        return serializers.UploadFileSerializer

    def get_pagination_class(self, request):
        return CustomPagination

    def get(self, request):
        # queryset = self.filter_queryset(request, self.get_queryset())
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        queryset = self.filter_queryset(request, self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadFileRetriveUpdateDeleteView(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):

    permission_classes = ()

    def get_queryset(self):
        return models.UploadFile.objects.all()

    def get_serializer_class(self):
        return serializers.UploadFileSerializer

    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except models.UploadFile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(model)
        return Response(serializer.data)

    def put(self, request, pk):
        model = self.get_object(pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(model, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        model = self.get_object(pk)
        model.delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)
