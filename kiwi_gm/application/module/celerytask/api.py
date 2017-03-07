# -*- coding:utf8 -*-

def get_task_status(task):
    status = task.state
    progress = 0
    if status == u'SUCCESS':
        progress = 100
    elif status == u'FAILURE':
        progress = 0
    elif status == 'PROGRESS':
        progress = task.info['progress']
    return {'status': status, 'progress': progress}
