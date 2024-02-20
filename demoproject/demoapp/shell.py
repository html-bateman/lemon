from django.contrib.auth.models import User
from .models import Test
#user = User.objects.create_user("mario",'mario@littlelemmon.com','Risotooo22#')
#user_name = User.objects.get(user_name="mario")

Test.objects.create(name='crossaint',price=5)