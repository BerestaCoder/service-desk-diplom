from django import forms
from .models import Service, User
 
class TicketForm(forms.Form):
    service = forms.ChoiceField(
        label="Услуга",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Выберите сервис',
        })
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Опишите вашу проблему подробно...',
        }),
        max_length=1000,
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        services = Service.objects.all().order_by('id')
        choices = [(service.id, service.name) for service in services]
        self.fields['service'].choices = choices

class DiagramForm(forms.Form):
    start = forms.DateField(label="Начало периода", widget=forms.DateInput(attrs={'type': 'date'}))
    end = forms.DateField(label="Конец периода",widget=forms.DateInput(attrs={'type': 'date'}))
    service_type = forms.ChoiceField(
        label="Тип услуги",
        choices=[('all', 'Все типы')] + Service.SERVICE_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Выберите тип услуги',
        })
    )
    service = forms.ChoiceField(
        label="Услуга",
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Выберите услугу',
        })
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        services = Service.objects.all().order_by('id')
        choices = [('all', 'Все услуги')]
        choices += [(service.id, service.name) for service in services]
        self.fields['service'].choices = choices

# ЭТАП 0
# Форма для смены услуги
class ChangeServiceForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Услуга')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        services = Service.objects.all().order_by('id')
        choices = [(service.id, service.name) for service in services]
        self.fields['service'].choices = choices

# Форма для утверждения услуги
class ApproveServiceForm(forms.Form):
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Срок выполнения')
    priority = forms.ChoiceField( choices=[],label='Приоритет',widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        priority_choices = [
            (0, 'Низкий'),
            (1, 'Средний'),
            (2, 'Высокий')
        ]
        self.fields['priority'].choices = priority_choices


# ЭТАП 1
# Форма для назначения ответственного
class AssignResponsibleForm(forms.Form):
    responsible = forms.ModelChoiceField(queryset=User.objects.all(), label='Ответственный')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        users = User.objects.all().order_by('id')
        choices = [(user.id, user.shortname) for user in users]
        self.fields['responsible'].choices = choices


# Форма для взятия ответственности
class TakeResponsibilityForm(forms.Form):
    pass

# ЭТАП 2
# Форма для смены ответственности
class ChangeResponsibleForm(forms.Form):
    new_responsible = forms.ModelChoiceField(queryset=User.objects.all(), label='Новый ответственный')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        users = User.objects.all().order_by('id')
        choices = [(user.id, user.shortname) for user in users]
        self.fields['new_responsible'].choices = choices
    

# Форма для завершения заявки
class CompleteForm(forms.Form):
    solution_code = forms.ChoiceField(label='Код решения', choices=[])
    solution_description = forms.CharField(widget=forms.Textarea, label='Описание решения')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        solution_code_choices = [
            (0, 'Решено'),
            (1, 'Остановлено'),
            (2, 'Провалено')
        ]
        self.fields['solution_code'].choices = solution_code_choices

# ЭТАП 3
# Форма для закрытия заявки
class CloseForm(forms.Form):
    closing_comment = forms.CharField(widget=forms.Textarea, label='Заключительный комментарий')
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1, 'max': 5}), label='Оценка качества (1-5)')