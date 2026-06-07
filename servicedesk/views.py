from .models import Ticket, Service, User
from .forms import *
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import calendar
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth

def login(request):
    return render(request, "login.html")

def error(request):
    return render(request, "404.html")

def main(request):
    tickets = Ticket.objects.all().order_by('-id') #[:20]
    
    data = {
        "tickets": tickets,
        "summary": tickets.count(),
        "form": TicketListFilterForm()
    }

    return render(request, "main.html", data)

def ticket(request, ticket_id):
    try:
        tic = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return render(request, "404.html", {"message": "Тикет не найден"}, status=404)

    forms = []
    match tic.stage:
        case 0:
            forms.append(ChangeServiceForm())
            forms.append(ApproveServiceForm())
        case 1:
            forms.append(AssignResponsibleForm())
            forms.append(TakeResponsibilityForm())
        case 2:
            forms.append(ChangeResponsibleForm())
            forms.append(CompleteForm())
        case 3:
            forms.append(CloseForm())

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
        "ticket_id": tic.id,
        "ticket_code": f"{tic.fk_service.get_service_type_display()}-{tic.id}",
        "tags": tags,
        "description": description,
        "initiator": initiator,
        "responsible": responsible,
        "datetimes": datetimes,
        'current_datetime': timezone.now(),
        'forms': forms
    }
    # тикет диспетчер поддтверждает класс тикета, то в модальном окне появляются рекомендатьельные параметры по дедлайну и приоритету
    if tic.stage == 0:
        try:
            service = Service.objects.get(id=tic.fk_service.id)
            default_priority = service.default_priority
            default_time_to_solve = service.default_time_to_solve
            deadline_date = timezone.now() + default_time_to_solve
        except Service.DoesNotExist:
            default_priority = 0
            default_time_to_solve = timedelta(days=5)
            deadline_date = timezone.now() + default_time_to_solve
        
        data['service_info'] = {
            "default_priority": default_priority,
            "default_deadline": deadline_date,
        }
    return render(request, "ticket.html", data)

def ticket_change_service(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return render(request, "404.html", {"message": "Тикет не найден"}, status=404)
    
    if request.method == "POST":
        form = ChangeServiceForm(request.POST)
        if form.is_valid():
            ticket.fk_service = form.cleaned_data['service']
            ticket.save()

    return redirect('ticket', ticket_id=ticket_id)

def ticket_approve_service(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return render(request, "404.html", {"message": "Тикет не найден"}, status=404)
    
    if request.method == "POST":
        form = ApproveServiceForm(request.POST)
        if form.is_valid():
            ticket.datetime_deadlinne = form.cleaned_data['deadline']
            ticket.priority = form.cleaned_data['priority']
            ticket.stage = 1
            ticket.save()
    
    return redirect('ticket', ticket_id=ticket_id)

def ticket_assign_responsible(request, ticket_id):
    if request.method == "POST":
        return redirect('ticket', ticket_id=ticket_id)
    
    return redirect('main')

def ticket_take_responsibility(request, ticket_id):
    if request.method == "POST":
        return redirect('ticket', ticket_id=ticket_id)
    
    return redirect('main')

def ticket_change_responsible(request, ticket_id):
    if request.method == "POST":
        return redirect('ticket', ticket_id=ticket_id)
    
    return redirect('main')

def ticket_complete(request, ticket_id):
    if request.method == "POST":
        return redirect('ticket', ticket_id=ticket_id)
    
    return redirect('main')

def ticket_close(request, ticket_id):
    if request.method == "POST":
        return redirect('ticket', ticket_id=ticket_id)
    
    return redirect('main')

def service_list(request):
    services = Service.objects.all()
    
    data = {
        "services": services,
    }

    return render(request, "service-list.html", data)

def service(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
    except Ticket.DoesNotExist:
        return render(request, "404.html", {"message": "Услуга не найдена"}, status=404)
    return render(request, "service.html", {"service": service })

def create_ticket(request):
    if request.method == "POST":
        service_id = request.POST.get("service")
        description = request.POST.get("description")
        
        service = Service.objects.get(id=service_id)
        user = User.objects.first()  # В прототипе без системы пользователей используется самый первый пользователь
        
        if not user:
            user = User.objects.create_user(username='temp_user', password='temp')
        
        ticket = Ticket(
                stage=0,
                #priority=0,
                fk_service=service,
                fk_initiator=user,  
                fk_responsible=None,
                description=description,
                datetime_registered=timezone.now(),
                is_stopped=False
            )
        
        ticket.save()

        return redirect('ticket', ticket_id=ticket.id)

    else:
        ticketform = TicketForm()
        data = {"form": ticketform}
        return render(request, "create-ticket.html", data)

def reports_default(request):
    return redirect('reports', type='chart_one')

def reports(request, type):
    match type:
        case "chart_one":
            return _chart_one(request)
        case "chart_two":
            return _chart_two(request)
        case "chart_three":
            return _chart_three(request)
        case "chart_four":
            return _chart_four(request)
        case _:
            return render(request, "404.html", {"message": "Отчёт не найден"}, status=404)

def _chart_one(request):
    tickets_query = Ticket.objects.all()
    
    date_from = request.GET.get('start')
    date_to = request.GET.get('end')
    service_type = request.GET.get('service_type')
    service_id = request.GET.get('service')
    
    if date_from:
        try:
            date_from_parsed = datetime.strptime(date_from, '%Y-%m-%d')
            tickets_query = tickets_query.filter(datetime_registered__gte=date_from_parsed)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_parsed = datetime.strptime(date_to, '%Y-%m-%d')
            tickets_query = tickets_query.filter(datetime_registered__lte=date_to_parsed)
        except ValueError:
            pass
    
    if service_id and service_id != 'all':
        try:
            service_id_int = int(service_id)
            tickets_query = tickets_query.filter(fk_service_id=service_id_int)
        except ValueError:
            pass
 
    if service_type and service_type != 'all':
        try:
            service_type_int = int(service_type)
            tickets_query = tickets_query.filter(fk_service__service_type=service_type_int)
        except (ValueError, TypeError):
            pass
    
    tickets_by_month_service = tickets_query.annotate(
        month=TruncMonth('datetime_registered')
    ).values(
        'month', 'fk_service__name'
    ).annotate(
        count=Count('id')
    ).order_by('month', 'fk_service__name')
    
    data = []
    for item in tickets_by_month_service:
        if item['month']:
            months_ru = {
                1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр', 5: 'Май', 6: 'Июн',
                7: 'Июл', 8: 'Авг', 9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'
            }
            month_name = months_ru[item['month'].month]
            service_name = item['fk_service__name'] if item['fk_service__name'] else 'Без названия'
            
            data.append({
                'Месяц': month_name,
                'Порядок': item['month'],
                'Услуга': service_name,
                'Количество заявок': item['count'],
            })
    
    df_long = pd.DataFrame(data)
    
    if df_long.empty:
        fig = px.bar(title='Нет данных за выбранный период')
        fig.update_layout(width=800, height=500, margin=dict(t=50, l=50, r=50, b=50))
    else:
        df_wide = df_long.pivot(index=['Месяц', 'Порядок'], 
                                 columns='Услуга', 
                                 values='Количество заявок').reset_index()
        
        df_wide = df_wide.fillna(0)
        df_wide = df_wide.sort_values('Порядок')
        unique_months = df_wide['Месяц'].tolist()
        
        fig = px.bar(
            df_wide,
            x='Месяц',
            y=[col for col in df_wide.columns if col not in ['Месяц', 'Порядок']],
            category_orders={'Месяц': unique_months},
            labels={'value': 'Количество заявок', 'variable': 'Услуга'}
        )
        
        fig.update_layout(
            width=800,
            height=500,
            margin=dict(t=50, l=50, r=50, b=50),
            xaxis_title="Месяц",
            yaxis_title="Количество заявок",
            legend_title="Услуга",
            template='plotly_white'
        )
    
    chart = fig.to_html(full_html=False)
    
    form = DiagramForm(initial={
        'start': date_from if date_from else '',
        'end': date_to if date_to else '',
        'service': service_id if service_id else 'all',
        'service_type': service_type if service_type else 'all'
    })
    
    return render(request, "reports.html", {"chart": chart, "form": form})

def _chart_two(request):
    return "Error 2"

def _chart_three(request):
    return "Error 3"

def _chart_four(request):
    return "Error 4"