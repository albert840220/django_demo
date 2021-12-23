from django import forms

from electrodes.models import Profile, Calibration


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

