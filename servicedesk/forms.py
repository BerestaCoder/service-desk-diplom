from django import forms
 
class TicketForm(forms.Form):
    service = forms.ChoiceField(
        label="Сервис",
        choices=(
            (1, "Восстановление пароля и доступ к учетной записи"),
            (2, "Установка и настройка ПО"),
            (3, "Подключение к Wi-Fi и сети"),
            (4, "Добавить пользователя в группу Active Directory"),
        ),
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