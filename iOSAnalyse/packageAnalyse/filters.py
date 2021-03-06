import django_filters

from packageAnalyse.models import Publish, Module


class PublishFilter(django_filters.FilterSet):
    version = django_filters.CharFilter(field_name='version', lookup_expr='icontains')
    build_no = django_filters.CharFilter(field_name='build_no', lookup_expr='icontains')
    branch = django_filters.CharFilter(field_name='branch', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    start = django_filters.CharFilter(field_name='create_time', lookup_expr='gt')
    end = django_filters.CharFilter(field_name='create_time', lookup_expr='lt')

    class Meta:
        model = Publish
        fields = ('version', 'build_no', 'branch', 'status', 'create_time')


class ModuleFilter(django_filters.FilterSet):
    module_name = django_filters.CharFilter(field_name='module_name', lookup_expr='icontains')
    version = django_filters.CharFilter(field_name='publish', method='filter_version')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    start = django_filters.CharFilter(field_name='create_time', lookup_expr='gt')
    end = django_filters.CharFilter(field_name='create_time', lookup_expr='lt')

    @classmethod
    def filter_version(cls, queryset, name, value):
        return queryset.filter(publish__version__icontains=value)

    class Meta:
        model = Module
        fields = ('module_name', 'version', 'status', 'create_time')
