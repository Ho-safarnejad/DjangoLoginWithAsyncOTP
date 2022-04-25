from django.contrib import admin
from .models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'is_staff')
    list_display_links = list_display


admin.site.register(Account, AccountAdmin)
