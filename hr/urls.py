from django.urls import path
from hr import views

urlpatterns=[
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path('employees/',views.employee_list,name='employee_list'),
    path('employees/add/',views.employee_create,name='employee_create'),
    path("employees/<int:id>/edit/",views.employee_update, name="employee_update"),
    path("employees/<int:id>/delete/",views.employee_delete, name="employee_delete"),
    path('leave_approve/',views.leave_approve,name='leave_approve'),
    path('leave_action/<int:id>/action/',views.leave_action,name='leave_action'),
    path('departments',views.department_list,name='department_list'),
    path('departments/add/',views.department_create,name='department_create'),
    path('departments/<int:id>/edit/', views.department_update, name='department_update'),
    path('departments/<int:id>/delete/', views.department_delete, name='department_delete'),
    path('designation',views.designation_list,name='designation_list'),
    path('designation/add/',views.designation_create,name='designation_create'),
    path('designation/<int:id>/edit/', views.designation_update, name='designation_update'),
    path('designation/<int:id>/delete/', views.designation_delete, name='designation_delete'),

    path('calendar/',views.calendar_view,name='calendar'),
    path('calendar/events/',views.calendar_events,name='calendar_events'),
    path('calendar/events/create/',views.create_calendar_event,name='create_calendar_event'),
    path('calendar/events/<int:event_id>/update/',views.update_calendar_event,name='update_calendar_event'),
    path('calendar/events/<int:event_id>/delete/',views.delete_calendar_event,name='delete_calendar_event'),
]