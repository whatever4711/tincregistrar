from django.contrib import admin

# Register your models here.

from .models import Node
from .models import Network

class NodeAdmin(admin.ModelAdmin):
  list_filter = ('network_name', 'hostname', 'public_IP', 'config_IP', 'private_IP',)
  list_display = ('hostname', 'network_name', 'public_IP', 'config_IP', 'private_IP', )

  def network_name(self, obj):
        return obj.network_set.netname

admin.site.register(Node, NodeAdmin)


admin.site.register(Network)
