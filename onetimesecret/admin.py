from django.contrib import admin

from onetimesecret import models


@admin.register(models.Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ["id", "uuid", "key", "salt", "has_custom_passphrase", "lifetime", "created"]
    readonly_fields = ["key", "uuid", "salt", "has_custom_passphrase", "lifetime", "content"]
    list_filter = ("has_custom_passphrase", "lifetime")
