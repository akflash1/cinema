from datetime import timedelta, date
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView
from cinema_app.forms import UserForm, HallForm, SessionForm, FilmForm
from cinema_app.models import Session, Film


class AdminPassedMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class Login(LoginView):
    template_name = 'login.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class Register(CreateView):
    form_class = UserForm
    template_name = 'register.html'
    success_url = '/'


class HallCreateView(AdminPassedMixin, CreateView):
    form_class = HallForm
    template_name = 'create_hall.html'
    success_url = '/'
    login_url = 'login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {'request': self.request}
        )
        return kwargs


class SessionCreateView(AdminPassedMixin, CreateView):
    form_class = SessionForm
    template_name = 'create_session.html'
    success_url = '/'
    login_url = 'login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.rest_of_seats = form.size

        date_start = obj.film.date_start
        date_finish = obj.film.date_finish

        delta = timedelta(days=1)
        date = date_start
        while date <= date_finish:
            session = Session(
                date=date,
                time_start=obj.time_start,
                time_end=obj.time_end,
                price=obj.price,
                rest_of_seats=form.size,
                hall=obj.hall,
                film=obj.film
            )
            session.save()
            date += delta

        obj.save()
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return redirect('/')


class FilmCreateView(AdminPassedMixin, CreateView):
    form_class = FilmForm
    template_name = 'create_film.html'
    success_url = '/'
    login_url = 'login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(
            {"request": self.request}
        )
        return kwargs

    def form_invalid(self, form):
        return redirect('/')


class FilmListView(ListView):
    model = Film
    context_object_name = 'films'
    template_name = 'film_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        tomorrow = today + timedelta(days=1)

        day_selected = self.request.GET.get('day', 'today')
        sort_by_selected = self.request.GET.get('sort_by', 'default')

        if day_selected == 'tomorrow':
            selected_date = tomorrow
        else:
            selected_date = today

        films_selected_day = Film.objects.filter(session__date=selected_date).distinct()
        sessions_selected_day = Session.objects.filter(date=selected_date)

        if sort_by_selected == 'price':
            films_selected_day = films_selected_day.order_by('session__price')
        elif sort_by_selected == 'time':
            films_selected_day = films_selected_day.order_by('session__time_start')

        context['films'] = films_selected_day
        context['sessions'] = sessions_selected_day
        context['sort_by'] = sort_by_selected
        context['day'] = day_selected
        context['today_date'] = today
        context['tomorrow_date'] = tomorrow

        return context

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', 'default')
        today = date.today()

        if sort_by == 'price':
            queryset = Film.objects.filter(session__date=today).order_by('session__price')
        elif sort_by == 'time':
            queryset = Film.objects.filter(session__date=today).order_by('session__time_start')
        else:
            queryset = Film.objects.filter(session__date=today)

        return queryset
