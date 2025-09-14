from django.contrib import admin
from .models import OTPCode
@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user','code','created','expires_at')
    readonly_fields = ('created',)
