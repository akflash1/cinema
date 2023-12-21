from django.contrib import admin

from cinema_app.models import User, Hall, Film, Session, Purchase

admin.site.register(User)
admin.site.register(Hall)
admin.site.register(Film)
admin.site.register(Session)
admin.site.register(Purchase)