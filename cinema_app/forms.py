from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TimeInput, DateInput

from cinema_app.models import User, Hall, Session, Film


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ('name', 'size')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) == 0:
            self.add_error(None, 'Eror')
            messages.eror(self.request, 'name must greater than 0')

    def clean_size(self):
        size = self.cleaned_data.get('size')

        if size <= 0:
            self.add_error(None, 'Eror')
            messages.error(self.request, 'size be greater than 0')
            return size


class FilmForm(ModelForm):
    class Meta:
        model = Film
        fields = ('name', 'description', 'date_start', 'date_finish',)
        widgets = {
            'date_start': DateInput(
                attrs={
                    'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                    'class': 'form-control'
                },
            ),
            'date_finish': DateInput(
                attrs={
                    'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get('date_start')
        date_finish = cleaned_data.get('date_finish')

        if date_start > date_finish:
            self.add_error(None, 'Error')
            messages.error(self.request, 'enter correct date, start date must be less than end date ')

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if len(name) <= 0:
            self.add_error(None, 'Error')
            messages.error(self.request, 'name should be longer')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if len(description) <= 0:
            self.add_error(None, 'Error')
            messages.error(self.request, 'Description should be longer')
        return description


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ('time_start', 'time_end', 'price', 'hall', 'film',)
        widgets = {
            'time_start': TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                },
            ),
            'time_end': TimeInput(
                format='%H:%M',
                attrs={
                    'type': 'time',
                }
            )
        }

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        hall = cleaned_data.get('hall')
        self.size = hall.size

        time_start = self.cleaned_data.get('time_start')
        time_end = self.cleaned_data.get('time_end')

        if time_start > time_end:
            self.add_error(None, 'Error')
            messages.error(self.request, 'time start must by less time end!')

        if time_start and time_end and hall:
            conflicting_sessions = Session.objects.filter(
                hall=hall,
                time_start__lt=time_end,
                time_end__gt=time_start
            )

            if self.instance:
                conflicting_sessions = conflicting_sessions.exclude(pk=self.instance.pk)

            if conflicting_sessions.exists():
                self.add_error(None, 'Error')
                messages.error(self.request, 'This session conflicts with an existing session.')

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price <= 0:
            self.add_error(None, 'Error')
            messages.error(self.request, 'price must be greater than 0')

        return price
