
from django.urls import path

from .api import api_start_timer, api_stop_timer, api_discard_timer, api_get_tasks

from .views import projectList, projectEdit, projectDelete, taskList, taskDetails, taskEdit, taskDelete, entryEdit, entryDelete, untrackedEntryDelete, track_entry

#name Space
app_name = 'project'

urlpatterns = [
    path('projectList/', projectList, name='projectList'),
    path('projectEdit/<int:project_id>/', projectEdit, name='projectEdit'),
    path('projectDelete/<int:project_id>/', projectDelete, name='projectDelete'),

    path('taskList/<int:project_id>', taskList, name='taskList'),
    path('taskDetails/<int:project_id>/<int:task_id>', taskDetails, name='taskDetails'),
    path('taskEdit/<int:project_id>/<int:task_id>', taskEdit, name='taskEdit'),
    path('taskDelete/<int:project_id>/<int:task_id>', taskDelete, name='taskDelete'),

    path('entryEdit/<int:project_id>/<int:task_id>/<int:entry_id>', entryEdit, name='entryEdit'),
    path('entryDelete/<int:project_id>/<int:task_id>/<int:entry_id>', entryDelete, name='entryDelete'),

    path('untrackedEntryDelete/<int:entry_id>/', untrackedEntryDelete, name='untrackedEntryDelete'),
    path('track_entry/<int:entry_id>/', track_entry, name='track_entry'),

    # API

    path('api/start_timer/', api_start_timer, name='api_start_timer'),
    path('api/stop_timer/', api_stop_timer, name='api_stop_timer'),
    path('api/discard_timer/', api_discard_timer, name='api_discard_timer'),
    path('api/get_tasks/', api_get_tasks, name='api_get_tasks'),
]