# -*- coding: utf-8 -*-
"""
Create by sandy at 20:02 07/04/2022
Description: ToDo
"""
from django.db.models.signals import pre_save, post_save, pre_init
from django.dispatch import receiver

from packageAnalyse.models import Publish


@receiver(pre_init, sender=Publish)
def publish_pre_init_callback(sender, **kwargs):
    file_obj = sender.result
    print(file_obj.field.__dict__)
    print(f"publish_pre_init_callback: {sender.result}")


@receiver(pre_save, sender=Publish)
def publish_pre_save_callback(sender, **kwargs):
    print(f"publish_pre_save_callback: {sender.result}")


@receiver(post_save, sender=Publish)
def publish_saved_callback(sender, **kwargs):
    print(f"publish_saved_callback: {sender.result}")

