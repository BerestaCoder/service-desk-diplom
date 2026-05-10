from collections import namedtuple
from .models import Ticket, Service, User
from .forms import TicketForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone

def login(request):
    return render(request, "login.html")

def ticket(request, ticket_id):
    try:
        tic = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return render(request, "404.html", {"message": "Тикет не найден"}, status=404)

    tags = {
        "stage": tic.stage,
        "priority": tic.priority
    }

    description = {
        "service": tic.fk_service.name,
        "message": tic.description
    }

    initiator = {
        "fullname": tic.fk_initiator.fullname,
        "job": tic.fk_initiator.fk_job.name,
        "department": tic.fk_initiator.fk_job.fk_department.name, 
        "email": tic.fk_initiator.email,
        "phone": tic.fk_initiator.phone,
    }

    if tic.fk_responsible:
        responsible = {
            "fullname": tic.fk_responsible.fullname,
            "job": tic.fk_responsible.fk_job.name,
            "email": tic.fk_responsible.email,
            "phone": tic.fk_responsible.phone,
        }
    else:
        responsible = {}

    datetime_fields = [
        'datetime_registered',
        'datetime_classified', 
        'datetime_assigned',
        'datetime_solved',
        'datetime_closed',
        'datetime_deadlinne'
    ]

    datetimes = {}
    for field in datetime_fields:
        value = getattr(tic, field, None)
        datetimes[field.replace('datetime_', 'time_')] = value

    data = {
        "ticket_code": f"{tic.fk_service.get_service_type_display()}-{tic.id}",
        "tags": tags,
        "description": description,
        "initiator": initiator,
        "responsible": responsible,
        "datetimes": datetimes,
        'current_datetime': timezone.now(),
    }
    return render(request, "ticket.html", data)

def main(request):
    tickets = Ticket.objects.all().order_by('-id') #[:20]
    
    data = {
        "tickets": tickets,
        "summary": tickets.count(),
    }

    return render(request, "main.html", data)

def create_ticket(request):
    if request.method == "POST":
        service_id = request.POST.get("service")
        description = request.POST.get("description")
        
        service = Service.objects.get(id=service_id)
        user = User.objects.get(id=1)
            
        ticket = Ticket(
                stage=0,
                priority=0,
                fk_service=service,
                fk_initiator=user,  # В прототипе без системы пользователей используется самый первый пользователь
                fk_responsible=None,
                description=description,
                datetime_registered=timezone.now(),
                is_stopped=False
            )
        
        ticket.save()

        return redirect('ticket', ticket_id=ticket.id)

    else:
        ticketform = TicketForm()
        return render(request, "create-ticket.html", {"form": ticketform})