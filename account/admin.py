from django.contrib import admin

from account.models import SignupCode, AccountDeletion, Account, EmailAddress


class SignupCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "max_uses", "use_count", "expiry", "created"]
    search_fields = ["code", "email"]
    list_filter = ["created"]


admin.site.register(SignupCode, SignupCodeAdmin)
admin.site.register(AccountDeletion, list_display=["email", "date_requested", "date_expunged"])
admin.site.register(Account, list_display=["user",])
admin.site.register(EmailAddress, list_display=["user", "email"])