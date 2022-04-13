# -*- coding: utf-8 -*-
"""
Create by sandy at 11:12 13/04/2022
Description: ToDo
"""
from iOSAnalyse.settings import BASE_DIR
import os
import logging


logger = logging.getLogger(__name__)


class OneClickUpdate(object):
    """
    todo Docker
    """

    def __init__(self):
        result = os.popen(f'git pull').read()
        logger.info(result)
        self.uwsgi_file_path = os.path.join(BASE_DIR, 'packageAnalyse', 'iOSAnalyse')
        self.update_server()
        self.update_web()

    def update_server(self):
        result = os.popen(f"pkill -9 uwsgi && uwsgi --plugin python3 {self.uwsgi_file_path}")
        logger.info(result.read())

    @classmethod
    def update_web(cls):
        result = os.popen(
            f'cd {BASE_DIR} && cd web/ && npm run build && \\cp -rf dist/ /var/www/site/ && nginx -s reload')
        logger.info(result.read())


if __name__ == '__main__':
    OneClickUpdate()
