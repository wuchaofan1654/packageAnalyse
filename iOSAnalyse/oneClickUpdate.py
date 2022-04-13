# -*- coding: utf-8 -*-
"""
Create by sandy at 11:12 13/04/2022
Description: ToDo
"""
from iOSAnalyse.settings import BASE_DIR
import os
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info = print


class OneClickUpdate(object):
    """
    todo Docker
    """

    def __init__(self):
        self.git_pull()
        self.update_server()
        self.update_web()
        logger.info("一键更新执行完毕\n")

    @classmethod
    def git_pull(cls):
        try:
            logger.info('开始拉取最新代码...')
            result = os.popen(f'git pull').read().strip()
            logger.info(result)
        except Exception as error:
            logger.exception(f'拉取最新代码报错：{error}')
        finally:
            logger.info('拉取最新代码执行完毕...\n')

    @classmethod
    def update_server(cls):
        try:
            logger.info('开始更新后端代码...')
            uwsgi_file_path = os.path.join(BASE_DIR, 'iOSAnalyse', 'uwsgi.ini')
            logger.info(f'uwsgi 文件绝对路径: {uwsgi_file_path}')
            result = os.popen(f"pkill -9 uwsgi && uwsgi --plugin python3 {uwsgi_file_path}")
            logger.info(result.read().strip())

        except Exception as error:
            logger.exception(f'更新后端代码报错：{error}')

        finally:
            logger.info('更新后端代码执行完毕...\n')

    @classmethod
    def update_web(cls):
        try:
            logger.info('开始更新前端代码...')
            result = os.popen(
                f'cd {BASE_DIR} && cd web/ && npm run build && \\cp -rf dist/ /var/www/site/ && nginx -s reload')
            logger.info(result.read().strip())
        except Exception as error:
            logger.exception(f'更新前端代码报错：{error}')
        finally:
            logger.info('更新前端代码执行完毕...\n')


if __name__ == '__main__':
    OneClickUpdate()
