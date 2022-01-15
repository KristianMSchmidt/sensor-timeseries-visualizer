from django.contrib import admin
from .models import SensorData, Batch

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp','value', 'sensor')
 
class BatchAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','duration','batch_id')

admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(Batch, BatchAdmin)
