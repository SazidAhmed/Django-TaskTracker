python manage.py shell


from django.contrib.auth.models import User
user = User.objects.get(username="myname")
user.is_staff = True
user.is_admin = True
user.is_superuser = True
user.save()


user.is_superuser = True