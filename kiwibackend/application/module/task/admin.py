from django.contrib import admin 
from task.models import DailyTask, TaskCondition, TaskReward, Task

admin.site.register(DailyTask)
admin.site.register(TaskCondition)
admin.site.register(TaskReward)
admin.site.register(Task)
