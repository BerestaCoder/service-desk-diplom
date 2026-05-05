from django.urls import path
from servicedesk import views

urlpatterns = [
    path("", views.main, name='main'),
    path("login", views.login, name='login'),
    path("ticket/<int:ticket_id>", views.ticket),
    path("create-ticket", views.create_ticket, name='create-ticket'),
]
