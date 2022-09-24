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

from {{ app_name }} import serializers
from {{ app_name }} import models
from {{ app_name }}.core.pagination import CustomPagination
