from django.contrib import admin
from .models import EmailMessage


@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'created_at']
    list_filter = ['email', 'subject', 'created_at']
    search_fields = ['email', 'subject', 'created_at']
    readonly_fields = ['email', 'subject', 'body', 'created_at']
    fieldsets = (
        (None, {
            'fields': ('email', 'subject', 'body', 'created_at')
        }),
    )
    ordering = ['-created_at', ]
    date_hierarchy = 'created_at'
    save_as = True
    list_per_page = 10
