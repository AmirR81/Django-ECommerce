from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, full_name, email, password):
        if not phone_number:
            raise ValueError('user most have phone_number')
        
        if not full_name:
            raise ValueError('user must have name')
        
        if not email:
            raise ValueError('user must have email')

        user = self.model(phone_number=phone_number, full_name=full_name, 
                          email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, full_name, email, password):
        user = self.create_user(phone_number, full_name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user



