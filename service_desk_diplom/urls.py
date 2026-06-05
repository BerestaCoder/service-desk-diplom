from django.urls import path
from servicedesk import views

urlpatterns = [
    path("", views.main, name='main'),
    path("login", views.login, name='login'),
    path("create-ticket", views.create_ticket, name='create-ticket'),
    path("services", views.service_list, name='service-list'),
    path("service/<int:service_id>", views.service, name='service'),
    path("diagram", views.diagram, name='diagram'),

    path("ticket/<int:ticket_id>", views.ticket, name='ticket'),
    path('ticket/<int:ticket_id>/change-service/', views.ticket_change_service, name='change-service'),
    path('ticket/<int:ticket_id>/approve-service/', views.ticket_approve_service, name='approve-service'),
    path('ticket/<int:ticket_id>/assign-responsible/', views.ticket_assign_responsible, name='assign-responsible'),
    path('ticket/<int:ticket_id>/take-responsibility/', views.ticket_take_responsibility, name='take-responsibility'),
    path('ticket/<int:ticket_id>/change-responsible/', views.ticket_change_responsible, name='change-responsible'),
    path('ticket/<int:ticket_id>/complete/', views.ticket_complete, name='complete-ticket'),
    path('ticket/<int:ticket_id>/close/', views.ticket_close, name='close-ticket'),

    path("error", views.error, name='error'),
]
