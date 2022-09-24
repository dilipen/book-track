
class {{class_name}}CreateList(
		mixins.ListModelMixin,
		mixins.CreateModelMixin,
		generics.GenericAPIView
	):

	permission_classes = ()

	def get_queryset(self):
		return models.{{entity}}.objects.order_by('id').all()

	def filter_queryset(self, queryset{{ arguments_as_string_without_last_with_default_none_value }}):
		q = Q()
{% for argument in arguments_as_list_without_last %}
		# if not {{argument}} == None:
			# q &= Q({{ argument }}={{argument}})
{% endfor %}
		return queryset.filter(q)

	def get_serializer_class(self):
		return serializers.{{serializer}}

	def get_pagination_class(self, request):
		return CustomPagination

	def get(self, request{{ arguments_as_string_without_last }}):
		
		if request.GET.get('verbose') == "true":
			queryset = self.filter_queryset(self.get_queryset(){{ arguments_as_string_without_last }})
			serializer = self.get_serializer(queryset, many=True)
			return Response(serializer.data)

		queryset = self.filter_queryset(self.get_queryset(){{ arguments_as_string_without_last }})
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def post(self, request{{ arguments_as_string_without_last }}):
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True
{% for argument in arguments_as_list_without_last %}
		data['{{ argument }}'] = {{ argument }}{% endfor %}
		serializer = serializer_class(data=data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
