from django.contrib import admin
from .models import Temp1, Temp2, Ph1, Ph2, BatchInfo

class Temp1Admin(admin.ModelAdmin):
    list_display = ('timestamp','value')

class Temp2Admin(admin.ModelAdmin):
    list_display = ('timestamp','value')
 
class Ph1Admin(admin.ModelAdmin):
    list_display = ('timestamp','value')
 
class Ph21Admin(admin.ModelAdmin):
    list_display = ('timestamp','value')
 
class BatchInfoAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','duration','batch_id')

admin.site.register(Temp1, Temp1Admin)
admin.site.register(Temp2, Temp1Admin)
admin.site.register(Ph1, Temp1Admin)
admin.site.register(Ph2, Temp1Admin)
admin.site.register(BatchInfo, BatchInfoAdmin)
