from rest_framework import mixins
from rest_framework import status
from rest_framework.request import Request

from packageAnalyse.common.response import SuccessResponse


class CreateModelMixin(mixins.CreateModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    create_serializer_class = None

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=serializer.instance, *args, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return SuccessResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        super().perform_create(serializer)


class ListModelMixin(mixins.ListModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    list_serializer_class = None

    def list(self, request: Request, *args, **kwargs):
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            if getattr(self, 'values_queryset', None):
                return self.get_paginated_response(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if getattr(self, 'values_queryset', None):
            return SuccessResponse(page)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    retrieve_serializer_class = None

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)


class UpdateModelMixin(mixins.UpdateModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    update_serializer_class = None

    def update(self, request: Request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        return SuccessResponse(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(mixins.DestroyModelMixin):
    """
    继承、增强DRF的CreateModelMixin, 标准化其返回值
    """
    destroy_serializer_class = None

    def get_object_list(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {f"{self.lookup_field}__in": self.kwargs[lookup_url_kwarg].split(',')}
        obj = queryset.filter(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request: Request, *args, **kwargs):
        instance = self.get_object_list()
        if hasattr(self, 'handle_logging'):
            self.handle_logging(request, instance=instance, *args, **kwargs)
        self.perform_destroy(instance)
        return SuccessResponse(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
