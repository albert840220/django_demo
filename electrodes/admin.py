from django.contrib import admin

from electrodes.models import Calibration, Inspection, Staff


class CalibratoionAdmin(admin.ModelAdmin):
    list_display = (
        'c_datetime', 'rfid', 'sensor_sn', 'slope', 'offset', 'temperature', 'method', 'health', 'res_time', 'act_z',)
    list_filter = ('c_datetime', 'rfid', 'sensor_sn')
    list_per_page = 20
    search_fields = ('Rfid', 'SensorSN')

    def get_list_display(self, request):
        default_list_display = super(CalibratoionAdmin, self).get_list_display(request)
        if request.user.groups.all()[0].name in ('網站管理員', '技術部'):
            return default_list_display
        return ('rfid', 'sensor_sn')


class InspectionAdmin(admin.ModelAdmin):
    list_display = ('form_id',
                    'delivery_date',
                    'client',
                    'incident_date',
                    'lifetime',
                    'hswe_name',
                    'online_date',
                    #'model',
                    'sn',
                    'return_date',
                    'system',
                    #'tag_no',
                    'start_date',
                    'sample_value',
                    'sample_conductivity',
                    'sample_pressure',
                    'sample_temperature',
                    'install_type',
                    'avg_life',
                    )

    list_filter = ('form_id', 'hswe_name')  # 右邊過濾器
    list_per_page = 10
    search_fields = ('form_id', 'hswe_name')  # 放大鏡搜尋欄


# TODO class StaffAdmin

admin.site.register(Calibration, CalibratoionAdmin)
admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Staff)
