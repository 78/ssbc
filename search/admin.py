from django.contrib import admin
from search.models import Hash, FileList, StatusReport, RecKeywords, Extra, ContactEmail


# Register your models here.
class ExtraInline(admin.StackedInline):
    model = Extra


class HashAdmin(admin.ModelAdmin):
    inlines = [ExtraInline]


class ExtraAdmin(admin.ModelAdmin):
    raw_id_fields = ['hash']
    list_display = ('hash', 'status', 'update_time')


class ContactEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'mail_from', 'receive_time', 'is_complaint')


admin.site.register(Hash, HashAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(FileList)
admin.site.register(ContactEmail, ContactEmailAdmin)
admin.site.register(StatusReport)
admin.site.register(RecKeywords)
