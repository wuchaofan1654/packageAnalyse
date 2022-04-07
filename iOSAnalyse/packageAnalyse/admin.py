from django.contrib import admin
from .models import Publish, Module, UploadFile

# Register your models here.

admin.site.register(Publish)
admin.site.register(Module)
admin.site.register(UploadFile)
