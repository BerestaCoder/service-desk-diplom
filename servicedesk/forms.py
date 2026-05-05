from django import forms
 
class TicketForm(forms.Form):
    service_type_id = forms.ChoiceField(choices=((1, "Восстановление пароля и доступ к учетной записи"), (2, "Установка и настройка ПО"), (3, "Подключение к Wi-Fi и сети"), (4, "Добавить пользователя в группу Active Directory")))
    description = forms.CharField()