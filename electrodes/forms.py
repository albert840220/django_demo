from django import forms

from electrodes.models import Profile, Calibration, Inspection

# class DateInput(forms.DateInput):
#     input_type = 'date'

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
        fields = ['c_datetime', 'Rfid', 'SensorSN', 'Slope', 'Offset', 'Temperature', 'Method', 'Health', 'ResTime',
                  'ActZ']
        widgets = {
            'c_datetime': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'Rfid': forms.TextInput(attrs={'class': 'form-control'}),
            'SensorSN': forms.TextInput(attrs={'class': 'form-control'}),
            'Slope': forms.TextInput(attrs={'class': 'form-control'}),
            'Offset': forms.TextInput(attrs={'class': 'form-control'}),
            'Temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'Method': forms.TextInput(attrs={'class': 'form-control'}),
            'Health': forms.TextInput(attrs={'class': 'form-control'}),
            'ResTime': forms.TextInput(attrs={'class': 'form-control'}),
            'ActZ': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        # fields = ['form_id','delivery_date','sn']
        fields = ['delivery_date','client','incident_date','lifetime','hswe_name','online_date','sn','return_date','system','start_date','sample_value','sample_conductivity','sample_pressure','sample_temperature','install_type','avg_life']
        # widgets = {
        #     'form_id': forms.DateInput(attrs={'class': 'form-control'}),
        #     'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        #     'sn': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        widgets = {
            # 'form_id': forms.DateInput(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'incident_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'lifetime': forms.TextInput(attrs={'class': 'form-control'}),
            'hswe_name': forms.TextInput(attrs={'class': 'form-control'}),
            'online_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            # 'type': forms.TextInput(attrs={'class': 'form-control'}),
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'type': 'date'}),
            'system': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            # 'end_date': forms.DateInput(attrs={'class': 'form-control','type':'date'}),
            'sample_value' : forms.TextInput(attrs={'class': 'form-control'}),
            'sample_conductivity' : forms.TextInput(attrs={'class': 'form-control'}),
            'sample_pressure' : forms.TextInput(attrs={'class': 'form-control'}),
            'sample_temperature': forms.TextInput(attrs={'class': 'form-control'}),
            'install_type' : forms.TextInput(attrs={'class': 'form-control'}),
            'avg_life' : forms.TextInput(attrs={'class': 'form-control'})
        }

