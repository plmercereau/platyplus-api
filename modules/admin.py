from django.contrib import admin

from modules.models import DataElement, TrackedEntityAttribute, TrackedEntity, Module, ObservationForm, Stage, \
    EventDataElement

admin.site.register(DataElement)
admin.site.register(TrackedEntity)
admin.site.register(TrackedEntityAttribute)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    # list_display = ['id', 'name']
    pass


admin.site.register(ObservationForm)
admin.site.register(Stage)
admin.site.register(EventDataElement)
