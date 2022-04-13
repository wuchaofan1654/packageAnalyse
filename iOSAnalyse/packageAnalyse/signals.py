# -*- coding: utf-8 -*-
"""
Create by sandy at 20:02 07/04/2022
Description: ToDo
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from iOSAnalyse.settings import BASE_DIR
from packageAnalyse.models import Publish, Module
from packageAnalyse.serializers import PublishSerializer
import json


def sync_modules_by_publish(publish: Publish):
    try:
        json_file_path = BASE_DIR + PublishSerializer(publish).data.get('jsonfile')
        modules = json.loads(open(json_file_path).read()).get('module_list')

        [Module.objects.create(
            module_name=module.get('module_name'),
            module_size=module.get('module_size'),
            publish=publish
        ).save() for module in modules]

    except Exception as error:
        return error


@receiver(post_save, sender=Publish)
def publish_saved_callback(sender, **kwargs):
    instance = kwargs.get('instance')
    sync_modules_by_publish(instance)




