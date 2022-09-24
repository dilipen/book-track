from itertools import permutations
import json
from sys import path_importer_cache

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
from rest_framework.views import APIView

from myapp import serializers
from myapp import models
from myapp.core.pagination import CustomPagination

from myapp.permissions import IsBuyer

from datetime import datetime

class BuyerCartCreateList(
		mixins.ListModelMixin,
		mixins.CreateModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsBuyer,)

	def get_queryset(self):
		return models.Cart.objects.order_by('id').all()

	def filter_queryset(self, queryset, user):
		q = Q(user=user)
		return queryset.filter(q)

	def get_serializer_class(self):
		return serializers.CartSerializer

	def get_pagination_class(self, request):
		return CustomPagination

	def get(self, request):
		
		if request.GET.get('verbose') == "true":
			queryset = self.filter_queryset(self.get_queryset(), request.user)
			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)

		queryset = self.filter_queryset(self.get_queryset(), request.user)
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

		serializer = serializer_class(data=data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class BuyerCartRetriveUpdateDelete(
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsBuyer,)

	def get_queryset(self):
		return models.Cart.objects.all()

	def filter_queryset(self, queryset, user):
		q = Q(user=user)
		return queryset.filter(q)

	def get_object(self, cart=None, user=None):

		if  cart is None:
			return True

		queryset = self.get_queryset()
		queryset = self.filter_queryset(user)
		model = get_object_or_404(queryset, id=cart)
		return model

	def get_serializer_class(self):
		return serializers.CartSerializer

	def get(self, request, cart):
		model = self.get_object(cart)
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(model)
		return Response(serializer.data)

	def put(self, request, cart):
		model = self.get_object(cart)
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True

		serializer = serializer_class(model, data=data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request, cart):
		model = self.get_object(cart)
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True

		serializer = serializer_class(model, data=data, partial=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def delete(self, request, cart):
		model = self.get_object(cart)
		# model.delete()
		model.deleted = True
		model.save()
		return Response(status=status.HTTP_205_RESET_CONTENT)

class CartSubmit(APIView):
	permission_classes = [IsBuyer]

	def post(self, request, user_address=None, format=None):
		user = request.user

		user_address = models.UserAddress.objects.filter(user=user,id=user_address).first()
		if user_address is None:
			content = {
				'status': 'please create at one user address',
			}
			return Response(content, status=400)

		carts = models.Cart.objects.filter(user=user)
		order = models.Order()
		order.created_at = datetime.now()
		order.modified_at = datetime.now()
		order.user = user
		order.save()
		for cart in carts:
			book = models.Book.objects.filter(id=cart.book.id).first()
			order_detail = models.OrderDetail()
			order_detail.order = order
			order_detail.book = cart.book
			order_detail.book_type = cart.book_type
			if order_detail.book_type == 'ebook':
				order_detail.rate = book.ebook_rate

			if order_detail.book_type == 'paper':
				order_detail.rate = book.paperbook_rate

			order_detail.save()

		order_details = models.OrderDetail.objects.filter(order=order, book_type='paper')
		transporter = models.Transporter.objects.first()
		for order_detail in order_details:
			paper_book_order = models.PaperBookOrder()
			paper_book_order.order_detail = order_detail
			paper_book_order.publisher = order_detail.book.publisher
			paper_book_order.user_address = user_address
			paper_book_order.transporter = transporter
			paper_book_order.save()

			paper_book_order_track = models.PaperBookOrderTrack()
			paper_book_order_track.paper_book_order = paper_book_order
			paper_book_order_track.tracker = 'preparing'
			paper_book_order_track.notes = 'Nil'
			paper_book_order_track.save()

		models.Cart.objects.filter(user=user).delete()

		content = {
			'status': 'orders created',
		}
		return Response(content)
