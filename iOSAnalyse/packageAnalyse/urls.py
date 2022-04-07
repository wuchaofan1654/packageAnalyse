# -*- coding: utf-8 -*-
"""
Create by sandy at 19:53 30/03/2022
Description: ToDo
"""

from django.urls import re_path
from rest_framework.routers import DefaultRouter

from packageAnalyse.views import PublishModelViewSet, ModuleModelViewSet

router = DefaultRouter()
router.register(r'publish', PublishModelViewSet)
router.register(r'module', ModuleModelViewSet)

urlpatterns = [
    re_path('publish/compare/(?P<pk1>.*)/(?P<pk2>.*)/', PublishModelViewSet.as_view({'get': 'compare_by_pk'})),
    re_path('publish/buildOptions/', PublishModelViewSet.as_view({'get': 'get_build_options'})),
    re_path('publish/byJson/', PublishModelViewSet.as_view({'post': 'add_by_json'})),
    re_path('module/moduleOptions/', ModuleModelViewSet.as_view({'get': 'get_module_options'})),
]
urlpatterns += router.urls
