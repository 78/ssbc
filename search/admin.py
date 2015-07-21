from django.contrib import admin
from search.models import Hash, FileList, StatusReport, RecKeywords


# Register your models here.
admin.site.register(Hash)
admin.site.register(FileList)
admin.site.register(StatusReport)
admin.site.register(RecKeywords)
