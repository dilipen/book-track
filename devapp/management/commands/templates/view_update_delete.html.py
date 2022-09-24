
class {{class_name}}RetriveUpdateDelete(
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin,
		mixins.DestroyModelMixin,
		generics.GenericAPIView
	):

	permission_classes = ()

	def get_queryset(self):
		return models.{{entity}}.objects.all()

	def filter_queryset(self, queryset{{ arguments_as_string_without_last_with_default_none_value }}):
		q = Q()
{% for argument in arguments_as_list_without_last %}
		# if not {{argument}} == None:
			# q &= Q({{ argument }}={{argument}})
{% endfor %}
		return queryset.filter(q)

	def get_object(self{{ arguments_as_string_with_default_none_value }}):
{% if arguments_as_list|length > 0%}
		if {% for argument in arguments_as_list %} {{ argument }} is None{% if not forloop.last %} and{% endif %}{% endfor %}:
			return True
{% endif %}
		queryset = self.get_queryset()
		queryset = self.filter_queryset(queryset{{ arguments_as_string_without_last }})
		model = get_object_or_404(queryset, {{ last_primary_key }}={{ last_argument }})
		return model

	def get_serializer_class(self):
		return serializers.{{ serializer }}

	def get(self, request{{ arguments_as_string }}):
		model = self.get_object({{ parameters_as_string }})
		serializer_class = self.get_serializer_class()
		serializer = serializer_class(model)
		return Response(serializer.data)

	def put(self, request{{ arguments_as_string }}):
		model = self.get_object({{ parameters_as_string }})
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True
{% for argument in arguments_as_list_without_last %}
		data['{{ argument }}'] = {{ argument }}{% endfor %}
		serializer = serializer_class(model, data=data)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def patch(self, request{{ arguments_as_string }}):
		model = self.get_object({{ parameters_as_string }})
		serializer_class = self.get_serializer_class()
		data = request.data

		if type(data) is not dict:
			data._mutable = True
{% for argument in arguments_as_list_without_last %}
		data['{{ argument }}'] = {{ argument }}{% endfor %}
		serializer = serializer_class(model, data=data, partial=True)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)

	def delete(self, request{{ arguments_as_string }}):
		model = self.get_object({{ parameters_as_string }})
		# model.delete()
		model.deleted = True
		model.save()
		return Response(status=status.HTTP_205_RESET_CONTENT)
