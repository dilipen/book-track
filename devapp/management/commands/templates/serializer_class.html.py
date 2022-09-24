
class {{ serializer_name }}(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {% templatetag openvariable %}my_custom_field_name{% templatetag closevariable %} = serializers.SerializerMethodField()

    # def get_{% templatetag openvariable %}my_custom_field_name{% templatetag closevariable %}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.{{ model_name }}
        fields = '__all__'
        # fields = ( {% for field in fields_list %}{% if field != 'child>' %}'{{ field }}', {% endif %}{% endfor %})
        # exclude = ('{% templatetag openvariable %}my_custom_field_name{% templatetag closevariable %}', )
        # read_only_fields = ( {% for field in readonly_fields_list %}'{{ field }}', {% endfor %})
