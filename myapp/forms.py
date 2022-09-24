from django.forms import ModelForm
from myapp import models


class UploadFileForm(ModelForm):
    class Meta:
        model = models.UploadFile
        fields = ['name', 'file']
