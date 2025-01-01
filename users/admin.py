from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expire_at')
    fields = ('code', 'user', 'expire_at', 'created_at')
    readonly_fields = ('created_at', 'code')
