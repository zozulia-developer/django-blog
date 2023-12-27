from django.contrib.auth import get_user_model
from django.forms import CharField, Form, ModelForm, PasswordInput


class SignUpForm(ModelForm):
    password = CharField(max_length=40, widget=PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')


class LoginRawForm(Form):
    username = CharField(max_length=30)
    password = CharField(max_length=40, widget=PasswordInput(attrs={'class': 'password'}))
