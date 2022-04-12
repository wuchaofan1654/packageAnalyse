# -*- coding: utf-8 -*-
"""
Create by sandy at 20:02 07/04/2022
Description: ToDo
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from iOSAnalyse.settings import BASE_DIR
from packageAnalyse.common.response import ErrorResponse
from packageAnalyse.models import Publish, Module
import json

from packageAnalyse.serializers import PublishSerializer


def sync_modules_by_publish(publish: Publish):
    try:
        publish_serialized = PublishSerializer(publish).data
        json_file_path = BASE_DIR + publish_serialized.get('jsonfile')
        modules = json.loads(open(json_file_path).read()).get('module_list')

        simpled_modules = [
            {"module_name": module.get('module_name'), "module_size": module.get('module_size')}
            for module in modules
        ]

        for module in simpled_modules:
            m = Module.objects.create(**module)
            m.publish = publish
            m.save()

        return True

    except Exception as error:
        return error


@receiver(post_save, sender=Publish)
def publish_saved_callback(sender, **kwargs):
    instance = kwargs.get('instance')
    sync_modules_by_publish(instance)




