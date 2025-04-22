from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:pk>/mark-finished/', views.mark_project_finished, name='mark_project_finished'),
    path('project/<int:pk>/mark-active/', views.mark_project_active, name='mark_project_active'),
    path('project/<int:project_id>/add-time/', views.add_time_entry, name='add_time_entry'),
    path('project/<int:project_id>/add-material/', views.add_material, name='add_material'),
    path('time-entry/<int:pk>/edit/', views.edit_time_entry, name='edit_time_entry'),
    path('time-entry/<int:pk>/delete/', views.delete_time_entry, name='delete_time_entry'),
    path('material/<int:pk>/edit/', views.edit_material, name='edit_material'),
    path('material/<int:pk>/delete/', views.delete_material, name='delete_material'),
    path('customers/', views.customer_list, name='customer_list'),
    path('projects/archive/', views.project_archive, name='project_archive'),
    path('user/hours/', views.user_hours_overview, name='user_hours_overview'),
]
