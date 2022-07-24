from django.contrib.auth.views import LoginView
from django.contrib import messages

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'user/login.html'

    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了！')
        return super().form_valid(form)