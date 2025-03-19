from django.views import generic
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import login_not_required
from django.utils.decorators import method_decorator

# Step 3: Create views and add the register template
# Create your views here.

@method_decorator(
    login_not_required,
    name="dispatch",
)
class RegisterView(generic.CreateView):
  template_name = 'registration/register.html'
  success_url = reverse_lazy('login')
  form_class = CustomUserCreationForm



