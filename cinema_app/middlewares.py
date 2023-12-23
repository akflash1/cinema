from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime


class LogoutInactiveUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_superuser:
            return
        now = datetime.now()
        last_action_not_decoded = request.session.get('last_action')
        if last_action_not_decoded:
            last_action = datetime.strptime(last_action_not_decoded, "%H-%M-%S %d/%m/%y")
            if (now - last_action).seconds > 60:
                logout(request)
        request.session['last_action'] = datetime.now().strftime("%H-%M-%S %d/%m/%y")