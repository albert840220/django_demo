from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from electrodes.forms import ProfileForm, form_validation_error, CalibrationForm
from electrodes.models import Profile, Calibration, Transaction

#多條件查詢圖表
from plotly.offline import plot
import plotly.graph_objs as go
from django.db import connection
import pandas as pd

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

def multi_condition(request):
    start_date = None
    end_date = None
    plot_div = None
    if request.method == 'POST':
        # records = Transaction.objects.all()
        cursor = connection.cursor()
        query = f"""SELECT * FROM calibrations"""
        df = pd.read_sql_query(query, connection)
        df = df.sort_values(by=['c_datetime'])
        if bool(request.POST['start_time']) and bool(request.POST['end_time']):
            print('in')
            start_date = request.POST['start_time']
            end_date = request.POST['end_time']
            df = df[
                (df['c_datetime'] > f'{start_date} 00:00:00') & (df['c_datetime'] < f'{end_date} 23:59:59')]
            print(f"{df}")

        if bool(request.POST['sn_number']):
            sn_number = request.POST['sn_number']
            print(sn_number)
            df = df[(df['SensorSN'] == sn_number)]
            print(f"sn_number: {df}")
        # up down show
        data = go.Scatter(x=df['c_datetime'], y=df['Slope'],
                          mode='lines', name='test',
                          opacity=0.8, marker_color='green')
        layout = go.Layout(height=400, title='Slope',
                           legend=dict(x=0.4, y=-0.3, traceorder='normal', font=dict(size=12,))
                           )
        fig = go.Figure(data=data, layout=layout)
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = f"{request.POST['sn_number']}"
        fig.update_layout(title_x=0.5, hovermode='x')
        plot_div = plot(fig, output_type='div')

        return render(request, "query.html", {'plot_div': plot_div})
    return render(request, "query.html")