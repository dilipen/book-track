from hashlib import pbkdf2_hmac
import json
from operator import mod

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
from rest_framework.views import APIView

from datetime import datetime

from myapp.permissions import IsPublisher

class PublisherPaperBookOrderCreateList(
		mixins.ListModelMixin,
		mixins.CreateModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsPublisher,)

	def get_queryset(self):
		return models.PaperBookOrder.objects.order_by('id').all()

	def filter_queryset(self, queryset, publisher):
		q = Q(publisher=publisher)
		q &= Q(is_handover_to_transporter=False)
		return queryset.filter(q)

	def get_serializer_class(self):
		return serializers.PaperBookOrderSerializer

	def get_pagination_class(self, request):
		return CustomPagination

	def get(self, request):
		
		if request.GET.get('verbose') == "true":
			queryset = self.filter_queryset(self.get_queryset(), request.user.publisher)
			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)

		queryset = self.filter_queryset(self.get_queryset(), request.user.publisher)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class PublisherPaperBookOrderRetriveUpdateDelete(
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsPublisher,)

	def get_queryset(self):
		return models.PaperBookOrder.objects.all()

	def filter_queryset(self, queryset, publisher):
		q = Q(publisher=publisher)
		q &= Q(is_handover_to_transporter=False)
		return queryset.filter(q)

	def get_object(self, paper_book_order=None, publisher=None):

		if  paper_book_order is None:
			return True

		queryset = self.get_queryset()
		queryset = self.filter_queryset(queryset, publisher)
		model = get_object_or_404(queryset, id=paper_book_order)
		return model

	def get_serializer_class(self):
		return serializers.PaperBookOrderSerializer

	def get(self, request, paper_book_order):
		model = self.get_object(paper_book_order, request.user.publisher)
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(model)
		return Response(serializer.data)

	def put(self, request, paper_book_order):
		model = self.get_object(paper_book_order, request.user.publisher)
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True

		serializer = serializer_class(model, data=data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request, paper_book_order):
		model = self.get_object(paper_book_order, request.user.publisher)
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True

		serializer = serializer_class(model, data=data, partial=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)


class BookDispatch(APIView):
	permission_classes = [IsPublisher]

	def post(self, request, paper_book_order, format=None):
		model = models.PaperBookOrder.objects.filter(id=paper_book_order, publisher=request.user.publisher).first()
		if model is not None:
			if model.is_dispatched is True:
				return Response({'status': 'this order already dispatched'})
			model.is_dispatched = True
			model.dispatched_at = datetime.now()
			model.save()

			paper_book_order_track = models.PaperBookOrderTrack()		
			paper_book_order_track.paper_book_order = model
			paper_book_order_track.tracker = "dispatched"
			paper_book_order_track.notes = 'Nil'
			paper_book_order_track.save()
			content = {
				'status': 'dispatched',
			}
			return Response(content)

		content = {
			'status': 'order not found',
		}
		return Response(content, status=400)


class BookHandOverToTransport(APIView):
	permission_classes = [IsPublisher]

	def post(self, request, paper_book_order, format=None):
		model = models.PaperBookOrder.objects.filter(id=paper_book_order, publisher=request.user.publisher).first()
		if model is not None:
			if model.is_handover_to_transporter is True:
				return Response({'status': 'this order already handover to transporter'})
			model.is_handover_to_transporter = True
			model.handover_to_transporter_at = datetime.now()
			model.save()

			paper_book_order_track = models.PaperBookOrderTrack()		
			paper_book_order_track.paper_book_order = model
			paper_book_order_track.tracker = "handover"
			paper_book_order_track.notes = 'Nil'
			paper_book_order_track.save()
			content = {
				'status': 'handover to transporter',
			}
			return Response(content)

		content = {
			'status': 'order not found',
		}
		return Response(content, status=400)


class PublisherPaperBookOrderHandOverList(
		mixins.ListModelMixin,
		mixins.CreateModelMixin,
		generics.GenericAPIView
	):

	permission_classes = (IsPublisher,)

	def get_queryset(self):
		return models.PaperBookOrder.objects.order_by('id').all()

	def filter_queryset(self, queryset, publisher):
		q = Q(publisher=publisher)
		q &= Q(is_handover_to_transporter=True)
		return queryset.filter(q)

	def get_serializer_class(self):
		return serializers.PaperBookOrderSerializer

	def get_pagination_class(self, request):
		return CustomPagination

	def get(self, request):
		
		if request.GET.get('verbose') == "true":
			queryset = self.filter_queryset(self.get_queryset(), request.user.publisher)
			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)

		queryset = self.filter_queryset(self.get_queryset(), request.user.publisher)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
