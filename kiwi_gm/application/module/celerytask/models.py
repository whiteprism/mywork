# -*- coding:utf8 -*-

from celerybeatredis.schedulers import RedisScheduler
from django.conf import settings
from celerybeatredis import Crontab
from datetime import timedelta

class TaskScheduler(RedisScheduler):
    """
    定时任务
    """

    @classmethod
    def _redis_key(cls, key="ALL"):
        return "%s-%s" % (settings.CELERY_REDIS_SCHEDULER_KEY_PREFIX, key)

    def delete(self, key):
        key = self.__class__._redis_key(key)
        self.rdb.delete(key)

    def add(self, *args, **argvs):
        name = argvs["name"]
        super(TaskScheduler, self).add(*args, **argvs)
        self.rdb.set(name, self.schedule[name].jsondump())


    def add_crontab_scheduler(self, task_name, cron_params, task_params):
        """
        定时任务
        schedule_params:
        {
            minute:0, 
            hour  :0,
            day_of_week  :None, 
            day_of_month :None, 
            month_of_year:None
        }

        task_params: tuple
        """

        name = "%s-%s" % (task_name, "-".join([str(p) for p in task_params]))
        cron = Crontab(**cron_params)
        task = self.add(
            name = self.__class__._redis_key(name),
            task = task_name,
            schedule = cron,
            args = task_params
        )
        #self.reserve(task)
        #self.sync()


    def add_interval_scheduler(self, task_name, seconds, task_params):
        """
        循环任务
        task_params: tuple
        """

        name = "%s-%s" % (task_name, "-".join([str(p) for p in task_params]))
        task = self.add(
            name = self.__class__._redis_key(name),
            task = task_name,
            schedule = timedelta(seconds=seconds),
            args = task_params
        )
#        self.reserve(task)
#        self.sync()

if hasattr(settings, "celery_app"):
    TaskSchedulerObj = TaskScheduler(app=settings.celery_app)
else:
    TaskSchedulerObj = None

