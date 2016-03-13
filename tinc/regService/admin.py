from django.contrib import admin

# Register your models here.

from .models import Node

class NodeAdmin(models.ModelAdmin):
  list_display
  list_filter = ('network', 'hostname', 'public_IP', 'config_IP', 'private_IP',)
  list_display = ('hostname', 'public_IP', 'config_IP', 'private_IP', )

admin.site.register(Node, NodeAdmin)


admin.site.register(Network)
