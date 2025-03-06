from django.contrib import admin

from .models import DownloadLink, SoftwareVersion

admin.site.register(DownloadLink)
admin.site.register(SoftwareVersion)

# Register your models here.
