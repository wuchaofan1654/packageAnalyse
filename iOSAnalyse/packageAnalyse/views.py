
from packageAnalyse.common.response import SuccessResponse
from packageAnalyse.common.utils import deep_update
from packageAnalyse.common.viewsets import CustomModelViewSet
from packageAnalyse.filters import PublishFilter, ModuleFilter
from packageAnalyse.models import Publish, Module
from packageAnalyse.serializers import PublishSerializer, ModuleSerializer


class PublishModelViewSet(CustomModelViewSet):
    """
    模型的CRUD视图
    """
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer
    update_serializer_class = PublishSerializer
    filter_class = PublishFilter
    ordering = '-create_time'  # 默认排序

    @classmethod
    def compare_by_pk(cls, request, *args, **kwargs):
        pk1 = kwargs.get('pk1')
        pk2 = kwargs.get('pk2')
        modules_1 = Module.objects.filter(publish__id=int(pk1))
        modules_2 = Module.objects.filter(publish__id=int(pk2))

        final_result = {module.module_name: {"old": module.module_size} for module in modules_1}

        for module in modules_2:
            deep_update(_dict=final_result, key=module.module_name, value={"new": module.module_size})

        for key, value in final_result.items():
            deep_update(_dict=final_result, key=key, value={"diff": value['new'] - value['old']})

        final_result_sorted = {
            k: v for k, v in sorted(final_result.items(),
                                    key=lambda item: abs(item[1]['diff']), reverse=True)}

        results = []
        for k, v in final_result_sorted.items():
            v['name'] = k
            results.append(v)

        return SuccessResponse(results)

    @classmethod
    def get_build_options(cls, request):
        query_sets = Publish.objects.all()
        query_sets = [{'id': query.id, 'version': query.version} for query in query_sets]
        return SuccessResponse(query_sets)

    @classmethod
    def add_by_json(cls, request):
        print(request.FILES, request.POST.get('version'))
        return SuccessResponse()


class ModuleModelViewSet(CustomModelViewSet):
    """
    模型的CRUD视图
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    filter_class = ModuleFilter
    ordering = '-create_time'  # 默认排序

    @classmethod
    def get_module_options(cls, request):
        queryset = Module.objects.all()
        result = {}
        for query in queryset:
            if query in result.keys():
                continue

            result[query.module_name] = query

        results = [{"id": res.id, "name": res.module_name} for res in result.values()]

        return SuccessResponse(results)
