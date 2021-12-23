from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from electrodes.forms import ProfileForm, form_validation_error, CalibrationForm
from electrodes.models import Profile, Calibration, Transaction

@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    profile = None
    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'electrodes/profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')

def addnew(request):
    if request.method == "POST":
        form = CalibrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/transactions1')
            except:
                pass

    else:
        form = CalibrationForm()
    return render(request,'addnew.html',{'form':form})

def edit(request, id):
    calibration = Calibration.objects.get(id=id)
    return render(request,'edit.html', {'calibration':calibration})
def update(request, id):
    calibration = Calibration.objects.get(id=id)
    form = CalibrationForm(request.POST, instance = calibration)
    print(form)
    if form.is_valid():
        form.save()
        print('alre save')
        return redirect("/transactions1")
    return render(request, 'edit.html', {'calibration': calibration})
def destroy(request, id):
    employee = Calibration.objects.get(id=id)
    employee.delete()
    return redirect("/transactions1")

def trans(request):
    calibrations = Calibration.objects.all()
    print(calibrations)
    return render(request,"transactions1.html",{'calibrations':calibrations})

def show_datatable(request):
    records = Calibration.objects.values('c_datetime','Rfid','SensorSN','Slope','Offset')
    return render(request, "datatable-test.html", {'records': records})

def chartjs(request):
    labels = []
    data = []
    data1 = Calibration.objects.order_by('id')[:5].values_list('id', 'Offset','Slope')
    labels, offset, slope= zip(*data1) # zip出來為tuple
    labels = list(labels)
    offset = [float(i) for i in offset]
    slope = [float(i) for i in slope]
    return render(request, 'chartjs.html', {'labels': labels,'offset': offset, 'slope': slope})