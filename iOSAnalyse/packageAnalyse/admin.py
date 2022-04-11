from django.contrib import admin
from .models import Publish, Module

# Register your models here.


class PublishAdmin(admin.ModelAdmin):
    list_display = ('version', 'build_no', 'branch', 'create_time')
    search_fields = ('version',)
    inlines = [Publish]  # Inline
    fieldsets = (
        ['Main', {
            'fields': ('version', 'build_no'),
        }],
        ['Advance', {
            'classes': ('version',),
            'fields': ('branch',),
        }]

    )


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'module_size', 'create_time')  # list
    search_fields = ('module_name',)
    inlines = [Module]  # Inline
    fieldsets = (
        ['Main', {
            'fields': ('module_name', 'module_size'),
        }],
    )


admin.site.register(Publish, PublishAdmin)
admin.site.register(Module, ModuleAdmin)
