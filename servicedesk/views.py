from collections import namedtuple
from .models import Ticket
from .forms import TicketForm
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

def login(request):
    return render(request, "login.html")

def ticket(request, ticket_id):
    if ticket_id == 0:
        description = {"service": "Тип услуги", "message": "Сообщение от пользователя"}
        initiator = {"full_name": "Иванов Иван", "job": "Сотрудник отдела продаж", "email": "ivanov.ivan@mail.ru", "phone": "+7 (797) 231-07-63"}
        responsible = {"full_name": "Соколов Дмитрий Андреевич", "job": "Ведущий инженер службы технической поддержки", "email": "d.sokolov@mail.ru", "phone": "+7 (495) 555-12-34"}
        status = {"stage": 0, "priority": 0, }
        datetimes = {"created": "2026-05-06T11:50:00Z", "deadline": "2026-05-06T11:55:00Z", "closed": "2026-05-06T11:59:00Z"}
    
        data = {
            "ticket_code": "INC-00000000",
            "description": description,
            "initiator": initiator,
            "responsible": responsible,
            "status": status,
            "datetimes": datetimes,
            'current_datetime': timezone.now(),
            }
        return render(request, "ticket.html", data)

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
        "full_name": tic.fk_initiator.fulname,
        "job": tic.fk_initiator.fk_job.name,
        "email": tic.fk_initiator.email,
        "phone": tic.fk_initiator.phone,
    }

    # Безопасное получение данных ответственного
    if tic.fk_responsible:
        responsible = {
            "full_name": tic.fk_responsible.fulname,
            "job": tic.fk_responsible.fk_job.name,
            "email": tic.fk_responsible.email,
            "phone": tic.fk_responsible.phone,
        }
    else:
        responsible = {
            "full_name": "Не назначен",
            "job": "",
            "email": "",
            "phone": "",
        }

    # Даты с обработкой NULL
    datetime_fields = [
        'datetime_registered',
        'datetime_classified', 
        'datetime_assigned',
        'datetime_diagnosed',
        'datetime_solved',
        'datetime_closed',
        'datetime_deadlinne'
    ]

    datetimes = {}
    for field in datetime_fields:
        value = getattr(tic, field, None)
        datetimes[field.replace('datetime_', 'time_')] = value

    data = {
        "ticket_code": f"INC-{tic.id}",
        "tags": tags,
        "description": description,
        "initiator": initiator,
        "responsible": responsible,
        "datetimes": datetimes,
        'current_datetime': timezone.now(),
}
    return render(request, "ticket.html", data)

def main(request):
    context = {
        'tickets': tickets_temp,
        'title': 'Тикеты',
    }
    return render(request, "main.html", context)

def create_ticket(request):
    if request.method == "POST":
        service_type_id = request.POST.get("service_type_id")
        description = request.POST.get("description")
        print(service_type_id)
        print(description)
        return HttpResponse(f"<h2>Услуга: {service_type_id}, Описание: {description}</h2>")
    else:
        ticketform = TicketForm()
        return render(request, "create-ticket.html", {"form": ticketform})

TicketTMP = namedtuple('Ticket', ['id', 'topic', 'priority', 'status', 'time', 'responsible'])

tickets_temp = [
    TicketTMP('INC-000245', 'Проблема с авторизацией', 'Высокий', 'Новый', '2026-01-15 09:30', 'Иван Иванов'),
    TicketTMP('INC-000246', 'Не загружается страница', 'Критический', 'В работе', '2026-01-15 11:15', 'Мария Петрова'),
    TicketTMP('REQ-000157', 'Запрос на расширение дискового пространства', 'Средний', 'Новый', '2026-01-16 10:00', 'Алексей Сидоров'),
    TicketTMP('PRB-000089', 'Периодический сбой базы данных', 'Высокий', 'В работе', '2026-01-16 14:20', 'Елена Козлова'),
    TicketTMP('INC-000247', 'Ошибка в отчете', 'Средний', 'На проверке', '2026-01-17 09:45', 'Дмитрий Смирнов'),
    TicketTMP('CHG-000034', 'Плановое обновление сервера', 'Низкий', 'Отложен', '2026-01-17 13:30', 'Иван Иванов'),
    TicketTMP('INC-000248', 'Медленная работа системы', 'Низкий', 'Завершен', '2026-01-18 08:15', 'Мария Петрова'),
    TicketTMP('REQ-000158', 'Доступ к новому серверу', 'Средний', 'В работе', '2026-01-18 11:00', 'Алексей Сидоров'),
    TicketTMP('PRB-000090', 'Проблема с синхронизацией данных', 'Критический', 'Новый', '2026-01-19 09:00', 'Елена Козлова'),
    TicketTMP('INC-000249', 'Не приходит письмо', 'Высокий', 'В работе', '2026-01-19 12:30', 'Дмитрий Смирнов'),
    TicketTMP('CHG-000035', 'Миграция на новую версию', 'Средний', 'Новый', '2026-01-20 10:15', 'Иван Иванов'),
    TicketTMP('INC-000250', 'Ошибка при экспорте данных', 'Средний', 'На проверке', '2026-01-20 14:45', 'Мария Петрова'),
    TicketTMP('TSK-000421', 'Настройка мониторинга', 'Низкий', 'В работе', '2026-01-21 08:30', 'Алексей Сидоров'),
    TicketTMP('REQ-000159', 'Установка дополнительного ПО', 'Средний', 'Новый', '2026-01-21 13:00', 'Елена Козлова'),
    TicketTMP('INC-000251', 'Проблема с API', 'Высокий', 'В работе', '2026-01-22 09:20', 'Дмитрий Смирнов'),
    TicketTMP('PRB-000091', 'Сбой при сохранении формы', 'Критический', 'Новый', '2026-01-22 11:45', 'Иван Иванов'),
    TicketTMP('CHG-000036', 'Обновление безопасности', 'Высокий', 'Отложен', '2026-01-23 10:00', 'Мария Петрова'),
    TicketTMP('INC-000252', 'Долгая загрузка отчета', 'Низкий', 'Завершен', '2026-01-23 14:30', 'Алексей Сидоров'),
    TicketTMP('TSK-000422', 'Бэкап данных', 'Средний', 'На проверке', '2026-01-24 08:45', 'Елена Козлова'),
    TicketTMP('REQ-000160', 'Создание нового пользователя', 'Низкий', 'В работе', '2026-01-24 12:15', 'Дмитрий Смирнов'),
    TicketTMP('INC-000253', 'Ошибка валидации формы', 'Средний', 'Новый', '2026-01-25 09:30', 'Иван Иванов'),
    TicketTMP('PRB-000092', 'Проблема с кэшированием', 'Высокий', 'В работе', '2026-01-25 13:20', 'Мария Петрова'),
    TicketTMP('INC-000254', 'Не работает фильтр поиска', 'Средний', 'Новый', '2026-01-26 10:45', 'Алексей Сидоров'),
    TicketTMP('CHG-000037', 'Изменение конфигурации сети', 'Низкий', 'Отложен', '2026-01-26 15:00', 'Елена Козлова'),
    TicketTMP('INC-000255', 'Ошибка 500 на сервере', 'Критический', 'В работе', '2026-01-27 08:30', 'Дмитрий Смирнов'),
]