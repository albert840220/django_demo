from django.contrib import admin

from electrodes.models import Calibration

class CalibratoionAdmin(admin.ModelAdmin):
    list_display = ('c_datetime','Rfid','SensorSN','Slope','Offset','Temperature','Method','Health','ResTime','ActZ',)
    list_filter = ('c_datetime','Rfid','SensorSN')
    list_per_page = 5
    search_fields = ('Rfid', 'SensorSN')
admin.site.register(Calibration,CalibratoionAdmin)
# admin.site.register(Profile)