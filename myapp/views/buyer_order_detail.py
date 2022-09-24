import json

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.utils.decorators import method_decorator

from rest_framework import mixins, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAdminUser

from myapp import serializers
from myapp import models
from myapp.core.pagination import CustomPagination

from myapp.permissions import IsBuyer


class BuyerOrderDetailCreateList(
		mixins.ListModelMixin,
		mixins.CreateModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsBuyer,)

	def get_queryset(self):
		return models.OrderDetail.objects.order_by('id').all()

	def filter_queryset(self, queryset, order=None):
		q = Q()

		# if not order == None:
			# q &= Q(order=order)

		return queryset.filter(q)

	def get_serializer_class(self):
		return serializers.OrderDetailSerializer

	def get_pagination_class(self, request):
		return CustomPagination

	def get(self, request, order):
		
		if request.GET.get('verbose') == "true":
			queryset = self.filter_queryset(self.get_queryset(), order)
			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)

		queryset = self.filter_queryset(self.get_queryset(), order)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class BuyerOrderDetailRetriveUpdateDelete(
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsBuyer,)

	def get_queryset(self):
		return models.OrderDetail.objects.all()

	def filter_queryset(self, queryset, order=None):
		q = Q()

		# if not order == None:
			# q &= Q(order=order)

		return queryset.filter(q)

	def get_object(self, order=None, order_detail=None):

		if  order is None and order_detail is None:
			return True

		queryset = self.get_queryset()
		queryset = self.filter_queryset(queryset, order)
		model = get_object_or_404(queryset, id=order_detail)
		return model

	def get_serializer_class(self):
		return serializers.OrderDetailSerializer

	def get(self, request, order, order_detail):
		model = self.get_object(order, order_detail)
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(model)
		return Response(serializer.data)
