from django.core.management.base import BaseCommand
from servicedesk.models import Service, Department, Job, User, Ticket
import random
from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Заполняет базу данных начальными данными'

    def handle(self, *args, **kwargs):
        # Очистка данных из таблиц
        Ticket.objects.all().delete()
        User.objects.all().delete()
        Job.objects.all().delete()
        Department.objects.all().delete()
        Service.objects.all().delete()

        # Создание служб (услуги ТОЛЬКО для ИТ отдела)
        services = [
            Service.objects.create(name='Сбой оборудования на линии розлива', service_type=0),
            Service.objects.create(name='Сбой в системе маркировки Честный Знак', service_type=0),
            Service.objects.create(name='Сбой в программе управления производством', service_type=0),
            Service.objects.create(name='Не работает принтер этикеток', service_type=0),
            Service.objects.create(name='Проблемы с доступом к базе данных', service_type=0),
            Service.objects.create(name='Нет доступа к ERP системе', service_type=0),
            Service.objects.create(name='Проблема с сетью в производственном цехе', service_type=0),
            Service.objects.create(name='Не загружается сайт предприятия', service_type=0),
            Service.objects.create(name='Проблема с почтовым сервером', service_type=0),
            Service.objects.create(name='Сбой в системе автоматизации цеха', service_type=0),
            Service.objects.create(name='Не запускается программа управления', service_type=0),
            Service.objects.create(name='Проблема с отчетами в 1С', service_type=0),
            Service.objects.create(name='Запрос на установку ПО', service_type=1),
            Service.objects.create(name='Запрос на настройку оборудования', service_type=1),
            Service.objects.create(name='Запрос на доступ к системе', service_type=1),
            Service.objects.create(name='Настройка рабочей станции', service_type=1),
            Service.objects.create(name='Замена компьютерного оборудования', service_type=1),
            Service.objects.create(name='Обновление программного обеспечения', service_type=1),
            Service.objects.create(name='Изменение прав доступа', service_type=3),
            Service.objects.create(name='Корректировка параметров системы', service_type=3),
            Service.objects.create(name='Изменение настроек сервера', service_type=3),
            Service.objects.create(name='Настройка VPN доступа', service_type=1),
            Service.objects.create(name='Восстановление данных из резервной копии', service_type=0),
        ]

        # Создание отделов
        departments = [
            Department.objects.create(name='ИТ Отдел'),
            Department.objects.create(name='Отдел Качества'),
            Department.objects.create(name='Производственный Отдел'),
            Department.objects.create(name='Отдел Кадров'),
            Department.objects.create(name='Бухгалтерия'),
            Department.objects.create(name='Отдел Продаж'),
            Department.objects.create(name='Юридический Отдел'),
            Department.objects.create(name='Логистический Отдел'),
            Department.objects.create(name='Маркетинговый Отдел'),
            Department.objects.create(name='Административный Отдел'),
            Department.objects.create(name='Технический Отдел'),
            Department.objects.create(name='Лаборатория'),
            Department.objects.create(name='Складской Отдел'),
        ]

        # Создание должностей
        jobs = [
            Job.objects.create(name='Системный администратор', fk_department=departments[0]),  # ИТ
            Job.objects.create(name='Инженер по качеству', fk_department=departments[1]),  # Отдел Качества
            Job.objects.create(name='Оператор линии розлива', fk_department=departments[2]),  # Производственный
            Job.objects.create(name='Менеджер по персоналу', fk_department=departments[3]),  # Отдел Кадров
            Job.objects.create(name='Бухгалтер', fk_department=departments[4]),  # Бухгалтерия
            Job.objects.create(name='Менеджер по продажам', fk_department=departments[5]),  # Отдел Продаж
            Job.objects.create(name='Юрисконсульт', fk_department=departments[6]),  # Юридический
            Job.objects.create(name='Логист', fk_department=departments[7]),  # Логистический
            Job.objects.create(name='Маркетолог', fk_department=departments[8]),  # Маркетинговый
            Job.objects.create(name='Начальник цеха', fk_department=departments[9]),  # Административный
            Job.objects.create(name='Инженер-технолог', fk_department=departments[10]),  # Технический
            Job.objects.create(name='Лаборант', fk_department=departments[11]),  # Лаборатория
            Job.objects.create(name='Кладовщик', fk_department=departments[12]),  # Складской
        ]

        # Создание пользователей с русскими ФИО
        users = []
        
        # ФИО для пользователей
        names = [
            ('Иван', 'Иванов', 'Иванович'), ('Петр', 'Петров', 'Петрович'),
            ('Сергей', 'Сергеев', 'Сергеевич'), ('Андрей', 'Андреев', 'Андреевич'),
            ('Дмитрий', 'Дмитриев', 'Дмитриевич'), ('Алексей', 'Алексеев', 'Алексеевич'),
            ('Михаил', 'Михайлов', 'Михайлович'), ('Владимир', 'Владимиров', 'Владимирович'),
            ('Николай', 'Николаев', 'Николаевич'), ('Евгений', 'Евгеньев', 'Евгеньевич'),
            ('Анна', 'Антонова', 'Антоновна'), ('Елена', 'Еленова', 'Еленовна'),
            ('Мария', 'Мариева', 'Мариевна'), ('Ольга', 'Ольгова', 'Ольговна'),
            ('Татьяна', 'Татищева', 'Татищевна'), ('Наталья', 'Натальева', 'Натальевна'),
            ('Ирина', 'Иринина', 'Иринична'), ('Светлана', 'Светланова', 'Светлановна'),
            ('Ксения', 'Ксеньева', 'Ксеньевна'), ('Виктория', 'Викторова', 'Викторовна'),
        ]
        
        for i, (first, last, middle) in enumerate(names[:20], 1):
            # Исполнители (из ИТ отдела) - отдел с индексом 0
            if random.choice([True, False]):  # Часть пользователей делаем из ИТ
                department = departments[0]  # ИТ Отдел
            else:
                department = random.choice(departments[1:])  # Другие отделы
            
            job = Job.objects.filter(fk_department=department).first()
            
            # Создаём сокращённое ФИО в формате "Фамилия И.О."
            shortname = f"{last} {first[0]}.{middle[0]}."
            
            # Создаём почту на домене milkfactory.ru
            email = f'{first.lower()}.{last.lower()}@milkfactory.ru'
            
            user = User.objects.create(
                email=email,
                fullname=f'{last} {first} {middle}',
                shortname=shortname,
                phone=f'+7999{random.randint(1000000, 9999999)}',
                fk_job=job
            )
            users.append(user)
        
        # Отдельно создаем больше исполнителей из ИТ отдела
        it_job = Job.objects.get(fk_department=departments[0])  # Системный администратор
        it_names = [
            ('Александр', 'Александров', 'Александрович'),
            ('Максим', 'Максимов', 'Максимович'),
            ('Артем', 'Артемов', 'Артемович'),
            ('Роман', 'Романов', 'Романович'),
            ('Олег', 'Олегов', 'Олегович'),
        ]
        
        for first, last, middle in it_names:
            # Создаём сокращённое ФИО в формате "Фамилия И.О."
            shortname = f"{last} {first[0]}.{middle[0]}."
            
            # Создаём почту на домене milkfactory.ru для IT
            email = f'{first.lower()}.{last.lower()}@it.milkfactory.ru'
            
            user = User.objects.create(
                email=email,
                fullname=f'{last} {first} {middle}',
                shortname=shortname,
                phone=f'+7999{random.randint(1000000, 9999999)}',
                fk_job=it_job
            )
            users.append(user)

        # Функция для генерации случайной даты
        def random_dates(start, end):
            return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

        # Получаем пользователей ИТ отдела для исполнителей
        it_users = User.objects.filter(fk_job__fk_department=departments[0])
        non_it_users = User.objects.exclude(fk_job__fk_department=departments[0])

        # Генерация тикетов
        for i in range(200):
            # Генерируем дату создания тикета
            ticket_date = random_dates(datetime(2026, 1, 1), datetime(2026, 12, 31))

            # Определяем стадию в зависимости от возраста тикета
            if i < 100:  # Для первых 100 тикетов
                stage = random.choice([3, 4])  # Решённые или закрытые
                datetime_solved = ticket_date if stage == 3 else None
                datetime_closed = ticket_date if stage == 4 else None
            else:  # Для последних 100 тикетов
                stage = random.choice([0, 1, 2])  # Новые, классифицируемые, назначенные
                datetime_solved = None
                datetime_closed = None

            # Инициатор - из любого отдела, кроме ИТ (или иногда из ИТ)
            if non_it_users:
                initiator = random.choice(non_it_users)
            else:
                initiator = random.choice(users)
                
            # Исполнитель - только из ИТ отдела
            responsible = random.choice(it_users) if it_users else random.choice(users)
            
            # Случайное описание тикета в зависимости от услуги
            descriptions = [
                'Оборудование остановилось, требуется срочное вмешательство',
                'Программа управления не запускается',
                'Нет доступа к базе данных предприятия',
                'Требуется настройка нового оборудования',
                'Проблема с отчетами в 1С',
                'Не работает принтер этикеток',
                'Сбой в системе автоматизации цеха',
                'Требуется помощь по работе с ERP системой',
                'Нужно установить программное обеспечение',
                'Проблема с сетью в производственном цехе',
                'Не загружается сайт предприятия',
                'Проблема с почтовым сервером',
            ]

            Ticket.objects.create(
                stage=stage,
                priority=random.randint(0, 2),
                fk_service=random.choice(services),
                fk_initiator=initiator,
                fk_responsible=responsible,
                description=random.choice(descriptions),
                datetime_registered=ticket_date,
                datetime_classified=random_dates(ticket_date, datetime(2026, 12, 31)) if stage > 0 else None,
                datetime_assigned=random_dates(ticket_date, datetime(2026, 12, 31)) if stage > 1 else None,
                datetime_diagnosed=random_dates(ticket_date, datetime(2026, 12, 31)) if stage == 2 else None,
                datetime_solved=datetime_solved,
                datetime_closed=datetime_closed,
                datetime_deadlinne=random_dates(datetime(2026, 1, 1), datetime(2026, 12, 31)),
                is_stopped=False
            )
        
        self.stdout.write(self.style.SUCCESS('База данных молочного завода успешно заполнена!'))