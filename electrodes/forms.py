from django import forms

from electrodes.models import Profile, Calibration, Inspection, PmSchedule, Factory, Customer, EqptPh, EqptCod, CustomerSurvey
from jsignature.forms import JSignatureField
from jsignature.widgets import JSignatureWidget
description_list = [
    ('月保養', '月保養'),
    ('季保養', '季保養'),
    ('半年保', '半年保'),
    ('年保養', '年保養'),
    ('其他', "其他")
]

purpose_list = [
    ('業務拜訪', "業務拜訪"),
    ("場勘", "場勘"),
    ("技術討論", "技術討論"),
    ("產品內容", "產品內容")
]

CHOICE = [
    ('非常滿意', '非常滿意'),
    ('滿意', '滿意'),
    ('尚可', '尚可'),
    ('其他', "其他")
]

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


class CalibrationForm(forms.ModelForm):
    class Meta:
        model = Calibration
        fields = ['c_datetime', 'rfid', 'sensor_sn', 'slope', 'offset', 'temperature', 'method', 'health', 'res_time',
                  'act_z']
        widgets = {
            'c_datetime': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'rfid': forms.TextInput(attrs={'class': 'form-control'}),
            'sensor_sn': forms.TextInput(attrs={'class': 'form-control'}),
            'slope': forms.TextInput(attrs={'class': 'form-control'}),
            'offset': forms.TextInput(attrs={'class': 'form-control'}),
            'temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'method': forms.TextInput(attrs={'class': 'form-control'}),
            'health': forms.TextInput(attrs={'class': 'form-control'}),
            'res_time': forms.TextInput(attrs={'class': 'form-control'}),
            'act_z': forms.TextInput(attrs={'class': 'form-control'}),
        }


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        # fields = ['form_id','delivery_date','sn']
        fields = ['delivery_date', 'client', 'incident_date', 'lifetime', 'hswe_name', 'online_date', 'sn',
                  'return_date', 'system', 'start_date', 'sample_value', 'sample_conductivity', 'sample_pressure',
                  'sample_temperature', 'install_type', 'avg_life']
        # widgets = {
        #     'form_id': forms.DateInput(attrs={'class': 'form-control'}),
        #     'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        #     'sn': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        widgets = {
            # 'form_id': forms.DateInput(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lifetime': forms.NumberInput(attrs={'class': 'form-control'}),
            'hswe_name': forms.TextInput(attrs={'class': 'form-control'}),
            'online_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'model': forms.TextInput(attrs={'class': 'form-control'}),
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'type': 'date'}),
            'system': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # 'end_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sample_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'sample_conductivity': forms.NumberInput(attrs={'class': 'form-control'}),
            'sample_pressure': forms.NumberInput(attrs={'class': 'form-control'}),
            'sample_temperature': forms.NumberInput(attrs={'class': 'form-control'}),
            'install_type': forms.TextInput(attrs={'class': 'form-control'}),
            'avg_life': forms.NumberInput(attrs={'class': 'form-control'})
        }


class PmScheduleForm(forms.ModelForm):
    class Meta:
        model = PmSchedule
        fields = ["next_maintenance_planned_on", 'customer_id', 'factory_id', "equipment_model", 'equipment_sn',
                  'description', 'staff_id']
        labels = {
            "next_maintenance_planned_on": "預計派工時間",
            'customer_id': '客戶名稱',
            'factory_id': '廠區名稱',
            "equipment_model": '機型',
            'equipment_sn': '機台序號',
            'description': '問題情況',
            'staff_id': '作業者',
        }
        widgets = {
            "next_maintenance_planned_on": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            # format=('%Y-%m-%d'),
            'customer_id': forms.Select(attrs={'class': 'form-control'}),
            # "factory_id":forms.TextInput(attrs={'class': 'form-control'}),
            # "factory_id":forms.Select(attrs={'class': 'form-select'},choices=FACTORY_CHOICES),
            "factory_id": forms.Select(attrs={'class': 'form-control'}),  # queryset = Factory.objects.all()),
            "equipment_model": forms.TextInput(attrs={'class': 'form-control'}),
            "equipment_sn": forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Select(attrs={'class': 'form-control'}, choices=description_list),
            'staff_id': forms.Select(attrs={'class': 'form-control'}),
            # "password2": PasswordInput(),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_name", "email", "phone", ]
        labels = {
            "customer_name": "姓名",
            "email": "電子信箱",
            "phone": "手機",
        }
        widgets = {
            "customer_name": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
        }


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = '__all__'
        labels = {
            "name": "廠區名稱",
            "city": "縣市",
            "address": "地址",
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "city": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
        }


class EqptPhForm(forms.ModelForm):
    class Meta:
        model = EqptPh
        fields = [
            "factory_id",
            "model",
            "sn",
            "last_pm",
            "standard_a",
            "standard_b",
            "sv1_ph",
            "sv2_ph",
            "pump_ph",
            "last_pm_staff",
            # "state",
        ]
        labels = {
            "factory_id": "廠區名稱",
            "model": "機型",
            "sn": "機台序號",
            "last_pm": "上次保養日",
            "standard_a": "標準液A 更換日",
            "standard_b": "標準液B 更換日",
            "sv1_ph": "SV1 更換日",
            "sv2_ph": "SV2 更換日",
            "pump_ph": "Pump 更換日",
            "last_pm_staff": "填單人員",
            # "state": "表單狀態",
        }
        widgets = {
            "factory_id": forms.Select(attrs={'class': 'form-control'}),
            "model": forms.TextInput(attrs={'class': 'form-control'}),
            "sn": forms.TextInput(attrs={'class': 'form-control'}),
            "last_pm": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "standard_a": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "standard_b": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "sv1_ph": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "sv2_ph": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "pump_ph": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "last_pm_staff": forms.Select(attrs={'class': 'form-control'}),
            # "state":forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_sn(self):
        sn = self.cleaned_data.get('sn')
        for instantce in EqptPh.objects.all():
            if instantce.sn == sn:
                raise forms.ValidationError("序號已存在")
        return sn


class EqptCodForm(forms.ModelForm):
    class Meta:
        model = EqptCod
        fields = [
            "factory_id",
            "model",
            "sn",
            "last_pm",
            "standard_c",
            "standard_d",
            "sv1_cod",
            "sv2_cod",
            "sv3_cod",
            "pump_cod",
            "last_pm_staff",
            "state",
        ]
        labels = {
            "factory_id": "廠區名稱",
            "model": "機型",
            "sn": "機台序號",
            "last_pm": "上次保養日",
            "standard_c": "標準液C 更換日",
            "standard_d": "標準液D 更換日",
            "sv1_cod": "SV1 更換日",
            "sv2_cod": "SV2 更換日",
            "sv3_cod": "SV3 更換日",
            "pump_cod": "幫浦 更換日",
            "last_pm_staff": '填單人員',
            "state": "表單狀態",
        }
        widgets = {
            "factory_id": forms.Select(attrs={'class': 'form-control'}),
            "model": forms.TextInput(attrs={'class': 'form-control'}),
            "sn": forms.TextInput(attrs={'class': 'form-control'}),
            "last_pm": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "standard_c": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "standard_d": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "sv1_cod": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "sv2_cod": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "sv3_cod": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "pump_cod": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "last_pm_staff": forms.Select(attrs={'class': 'form-control'}),
            "state": forms.TextInput(attrs={'class': 'form-control'}),
        }

class CustomerSurveyForm(forms.ModelForm):
    class Meta:
        model = CustomerSurvey
        fields = '__all__'
        labels = {
            "company": "公司名稱",
            "purpose_of_visit": "拜訪目的",
            "product_description": "產品說明",
            "service_attitude": "服務態度",
            "customer_advice": "客戶建議",
            "signature": "簽名",
        }
        widgets = {
            "company": forms.TextInput(attrs={'class': 'form-control'}),
            "purpose_of_visit": forms.RadioSelect(choices=purpose_list),
            "product_description": forms.RadioSelect(choices=CHOICE),
            "service_attitude": forms.RadioSelect(choices=CHOICE),
            "customer_advice": forms.Textarea(attrs={'class': 'form-control'}),#attrs={'rows': "5", "cols": "70", "maxlength":"30"}), #attrs={'class': 'form-control'}),
            'signature': JSignatureWidget(jsignature_attrs={'height': '200px','width': '500'})# 'color': '#e0b642',
        }