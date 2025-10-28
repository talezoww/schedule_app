from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('groups/', views.groups_list_view, name='groups_list'),
    path('groups/<int:group_id>/', views.group_detail_view, name='group_detail'),
    path('teachers/', views.teachers_list_view, name='teachers_list'),
    path('my-groups/', views.my_groups_view, name='my_groups'),
    path('subjects/', views.subjects_list_view, name='subjects_list'),
]
