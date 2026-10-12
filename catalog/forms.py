from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Ваше имя', required=True)
    phone = forms.CharField(max_length=20, label='Телефон', required=True)
    message = forms.CharField(widget=forms.Textarea, label='Сообщение', required=False)