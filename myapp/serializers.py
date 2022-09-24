from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.User
        fields = '__all__'
        # fields = ( 'logentry>', 'cart>', 'order>', 'orderdetail>', 'application>', 'grant>', 'accesstoken>', 'refreshtoken>', 'idtoken>', 'id', 'password', 'last_login', 'is_superuser', 'email', 'first_name', 'last_name', 'date_joined', 'is_active', 'avatar', 'is_publisher', 'is_buyer', 'groups', 'user_permissions', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( )

class UploadFileSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.UploadFile
        fields = '__all__'
        # fields = ( 'id', 'name', 'file', 'created_at', 'modified_at', 'deleted', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( 'created_at', 'modified_at', )

class PublisherSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Publisher
        fields = '__all__'
        # fields = ( 'book>', 'paperbookorder>', 'id', 'name', 'created_at', 'modified_at', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( 'created_at', 'modified_at', )

class BookSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Book
        fields = '__all__'
        # fields = ( 'cart>', 'orderdetail>', 'id', 'name', 'created_at', 'modified_at', 'ebook_rate', 'paperbook_rate', 'publisher', )
        # exclude = ('{{my_custom_field_name}}', )
        # exclude = ('publisher', )
        # read_only_fields = ( 'created_at', 'modified_at', )

class CartSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Cart
        fields = '__all__'
        # fields = ( 'id', 'created_at', 'modified_at', 'user', 'book', 'book_type', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( 'created_at', 'modified_at', )

class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.UserAddress
        fields = '__all__'
        # fields = ( 'id', 'address_line1', 'address_line2', 'address_line3', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( )

class OrderSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    extra_order_details = serializers.SerializerMethodField()

    def get_extra_order_details(self, model):
        order_details = models.OrderDetail.objects.filter(order=model)
        return OrderDetailSerializer(order_details, many=True).data

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.Order
        fields = '__all__'
        # fields = ( 'orderdetail>', 'paperbookorder>', 'paperbookordertrack>', 'id', 'user', 'created_at', 'modified_at', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( 'created_at', 'modified_at', )

class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()
    extra_track_details = serializers.SerializerMethodField()
    def get_extra_track_details(self, model):
        try:
            order_details = models.PaperBookOrderTrack.objects.filter(paper_book_order__order_detail=model)
            return PaperBookOrderTrackSerializer(order_details, many=True).data
        except:
            return []

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.OrderDetail
        fields = '__all__'
        # fields = ( 'id', 'order', 'user', 'book', 'book_type', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( )

class PaperBookOrderSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    extra_paper_book_order_transport = serializers.SerializerMethodField()

    def get_extra_paper_book_order_transport(self, model):
        paper_book_order_transport_models = models.PaperBookOrderTrack.objects.filter(paper_book_order=model)
        return PaperBookOrderTrackSerializer(paper_book_order_transport_models, many=True).data

    extra_user_address = serializers.SerializerMethodField()

    def get_extra_user_address(self, model):
        user_address_model = model.user_address
        return UserAddressSerializer(user_address_model).data

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.PaperBookOrder
        fields = '__all__'
        # fields = ( 'id', 'order_detail', 'publisher', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( )

class PaperBookOrderTrackSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    # {{my_custom_field_name}} = serializers.SerializerMethodField()

    # def get_{{my_custom_field_name}}(self, model):
        # return NewModel.objects.all().filter(model=model).count()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = models.PaperBookOrderTrack
        fields = '__all__'
        # fields = ( 'id', 'order', 'tracker', 'notes', 'created_at', 'modified_at', )
        # exclude = ('{{my_custom_field_name}}', )
        # read_only_fields = ( 'created_at', 'modified_at', )
