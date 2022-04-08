# -*- coding: utf-8 -*-
"""
Create by sandy at 20:02 07/04/2022
Description: ToDo
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from iOSAnalyse.settings import BASE_DIR
from packageAnalyse.common.response import ErrorResponse
from packageAnalyse.models import Publish, Module
import json
import os

from packageAnalyse.serializers import PublishSerializer


def sync_modules_by_publish(publish: Publish):
    try:
        publish_serialized = PublishSerializer(publish).data
        json_file_path = BASE_DIR + publish_serialized.get('jsonfile')
        print(BASE_DIR, json_file_path)
        modules = json.loads(open(json_file_path).read()).get('module_list')

        print(modules)
        simpled_modules = [
            {"module_name": module.get('module_name'), "module_size": module.get('module_size')}
            for module in modules
        ]

        for module in simpled_modules:
            m = Module.objects.create(**module)
            m.publish.add(publish)
            m.save()
    except Exception as error:
        print(error)
        return ErrorResponse(code=10004, msg=error)


@receiver(post_save, sender=Publish)
def publish_saved_callback(sender, **kwargs):
    instance = kwargs.get('instance')
    sync_modules_by_publish(instance)

