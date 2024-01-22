from django.contrib.auth.base_user import BaseUserManager

class Mycustommannager(BaseUserManager):
    def create_user(self,username,email,password,**extra_fields):
        if not username:
            raise ValueError('the username must be sets')
        if not email:
            raise ValueError('the email must be sets')
        if not password:
            raise ValueError('the password must be sets')
        
        email=self.normalize_email(email)
        user=self.model(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('the superuser must be is_staff true ')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('the superuser must be is_superuser true ')
           
        return self.create_user(
            username,
            email,
            password,
            **extra_fields,
        )
        
        
        