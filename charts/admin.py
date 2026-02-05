from django.contrib import admin
from .models import HaradaChart, Pillar, Task, TaskComment

admin.site.register(HaradaChart)
admin.site.register(Pillar)
admin.site.register(Task)
admin.site.register(TaskComment)
