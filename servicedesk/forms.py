from django import forms
from .models import Service
 
class TicketForm(forms.Form):
    service = forms.ChoiceField(
        label="Сервис",
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