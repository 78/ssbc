from django.contrib import admin
from search.models import Hash, FileList, StatusReport

# Register your models here.
admin.site.register(Hash)
admin.site.register(FileList)
admin.site.register(StatusReport)

