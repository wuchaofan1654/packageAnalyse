
from packageAnalyse.common.response import SuccessResponse, ErrorResponse
from packageAnalyse.common.viewsets import CustomModelViewSet
from packageAnalyse.filters import PublishFilter, ModuleFilter
from packageAnalyse.instances import CompareResult, SingleCompareResult
from packageAnalyse.models import Publish, Module
from packageAnalyse.serializers import PublishSerializer, ModuleSerializer
from packageAnalyse.signals import sync_modules_by_publish


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
        try:
            pk1 = kwargs.get('pk1')
            pk2 = kwargs.get('pk2')

            pk1_modules = Module.objects.filter(publish__id=int(pk1))
            pk2_modules = Module.objects.filter(publish__id=int(pk2))

            data = CompareResult(
                pk1_publish=PublishSerializer(Publish.objects.get(pk=int(pk1))).data,
                pk2_publish=PublishSerializer(Publish.objects.get(pk=int(pk2))).data
            )

            for module in pk1_modules:
                result = SingleCompareResult(module_name=module.module_name, pk1_module_size=module.module_size)
                for _module in pk2_modules:
                    if _module.module_name == result.module_name:
                        result.pk2_module_size = _module.module_size

                data.results.append(result.calculate_diff())

            diff_modules = [_module for _module in pk2_modules if _module.module_name
                            not in [module.module_name for module in pk1_modules]]

            data.results.extend(
                [SingleCompareResult(
                    module_name=module.module_name,
                    pk2_module_size=module.module_size).calculate_diff() for module in diff_modules])

            return SuccessResponse(data.sort_by_diff().dict())
        except Exception as err:
            return ErrorResponse(code=201, msg=f'{err}')

    @classmethod
    def get_build_options(cls, request):
        query_sets = Publish.objects.all()
        query_sets = [{'id': query.id, 'version': query.version} for query in query_sets]
        return SuccessResponse(query_sets)

    @classmethod
    def sync_modules(cls, request, pk):
        try:
            publish = Publish.objects.get(pk=pk)
            sync_modules_by_publish(publish)
            return SuccessResponse(msg='同步成功')

        except Exception as error:
            return ErrorResponse(code=10002, msg=error)


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
