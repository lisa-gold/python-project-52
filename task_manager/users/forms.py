from django.contrib.auth.forms import UserCreationForm
from task_manager.users.models import CustomUser


class UserForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username']
    
    def  clean_username(self):
        if 'username' in self.changed_data:
            return super().clean_username()
        return self.cleaned_data.get("username")
