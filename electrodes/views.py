from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from electrodes.forms import ProfileForm, form_validation_error, CalibrationForm, InspectionForm
from electrodes.models import Profile, Calibration, Inspection, Transaction

# 多條件查詢圖表
from plotly.offline import plot
import plotly.graph_objs as go
from django.db import connection
import pandas as pd

import locale

#下載excel
import openpyxl
from django.utils.http import urlquote
from django.http import HttpResponse


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
    return render(request, 'addnew.html', {'form': form})


def edit(request, id):
    calibration = Calibration.objects.get(id=id)
    return render(request, 'edit.html', {'calibration': calibration})


def update(request, id):
    calibration = Calibration.objects.get(id=id)
    form = CalibrationForm(request.POST, instance=calibration)
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
    return render(request, "transactions1.html", {'calibrations': calibrations})


def show_datatable(request):
    records = Calibration.objects.values('c_datetime', 'Rfid', 'SensorSN', 'Slope', 'Offset')
    return render(request, "calibrations.html", {'records': records})


def chartjs(request):
    labels = []
    data = []
    data1 = Calibration.objects.order_by('c_datetime')[:20].values_list('c_datetime', 'Offset', 'Slope')
    labels, offset, slope = zip(*data1)  # zip出來為tuple
    labels = list(i.strftime("%Y-%m-%d %H:%M:%S") for i in labels)
    offset = [float(i) for i in offset]
    slope = [float(i) for i in slope]
    return render(request, 'chartjs.html', {'labels': labels, 'offset': offset, 'slope': slope})


def multi_condition_plot(request):
    start_date = None
    end_date = None
    plot_div = None
    items = ['Slope','Offset']

    if request.method == 'POST':
        # print(request.POST)
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
            df = df[(df['SensorSN'] == sn_number)]
            print(f"sn_number: {df}")
        # up down show
        data = go.Scatter(x=df['c_datetime'], y=df['Slope'],
                          mode='lines', name='test',
                          opacity=0.8, marker_color='green')
        layout = go.Layout(height=400, title='Slope',
                           legend=dict(x=0.4, y=-0.3, traceorder='normal', font=dict(size=12, ))
                           )
        fig = go.Figure(data=data, layout=layout)
        # 單線 顯示legend
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = f"{request.POST['sn_number']}"
        fig.update_layout(title_x=0.5, hovermode='x')
        plot_div = plot(fig, output_type='div')

        data = go.Scatter(x=df['c_datetime'], y=df['Offset'],
                          mode='lines', name='test',
                          opacity=0.8, marker_color='red')
        layout = go.Layout(height=300, title='Offset')
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(title_x=0.5, hovermode='x')
        plot_div1 = plot(fig, output_type='div')
        # 兩線合併
        Slope = go.Scatter(x=df['c_datetime'], y=df['Slope'],
                           mode='lines', name='Slope',
                           opacity=0.8, marker_color='green')
        Offset = go.Scatter(x=df['c_datetime'], y=df['Offset'],
                            mode='lines', name='Offset',
                            opacity=0.8, marker_color='red')
        data = [Slope, Offset]
        layout = go.Layout(height=400, title='Slope and Offset')
        fig = go.Figure(data=data, layout=layout)
        fig.update_layout(title_x=0.5, hovermode='x')
        plot_compare = plot(fig, output_type='div')

        return render(request, "trends.html", {'plot_div': plot_div,'plot_div1':plot_div1,'plot_compare':plot_compare,'items':items})
    return render(request, "trends.html", {'items':items})


def report_write(request):
    if request.method == "POST":
        form = InspectionForm(request.POST)
        print(form)
        if form.is_valid():
            # form_id = form.cleaned_data['form_id']
            delivery_date = form.cleaned_data['delivery_date']
            client = form.cleaned_data['client']
            incident_date = form.cleaned_data['incident_date']
            lifetime = form.cleaned_data['lifetime']
            hswe_name = form.cleaned_data['hswe_name']
            online_date = form.cleaned_data['online_date']
            # type = form.cleaned_data['type']
            sn = form.cleaned_data['sn']
            return_date = form.cleaned_data['return_date']
            system = form.cleaned_data['system']
            # tag_no = form.cleaned_data['tag_no']
            start_date = form.cleaned_data['start_date']
            # end_date = form.cleaned_data['end_date']
            # error_report = form.cleaned_data['error_report']
            sample_value = form.cleaned_data['sample_value']
            sample_conductivity = form.cleaned_data['sample_conductivity']
            sample_pressure = form.cleaned_data['sample_pressure']
            sample_temperature = form.cleaned_data['sample_temperature']
            install_type = form.cleaned_data['install_type']
            avg_life = form.cleaned_data['avg_life']
            Inspection.objects.create(form_id=str(incident_date).replace('-','') + '-' + sn, delivery_date=delivery_date, client=client,
                                      incident_date=incident_date, lifetime=lifetime, hswe_name=hswe_name,
                                      online_date=online_date, sn=sn,
                                      return_date=return_date, system=system, start_date=start_date,
                                      sample_value=sample_value, sample_conductivity=sample_conductivity,
                                      sample_pressure=sample_pressure, sample_temperature=sample_temperature,
                                      install_type=install_type, avg_life=avg_life)
            return render(request, 'form_success.html')
    else:
        form = InspectionForm()
    return render(request, 'report_write.html', {'form': form})

def exportToExcel(request,form_id):
    inspection = Inspection.objects.get(form_id=form_id)
    wb = openpyxl.load_workbook(filename='C:/Users/user01/Desktop/檢測與檢討報告書.xlsx')
    sheet = wb.worksheets[0]
    sheet.cell(row=4, column=4, value=f"{inspection.form_id}")  # 報告書編號
    sheet.cell(row=4, column=10, value=f"{inspection.delivery_date}")  # 出貨日期
    sheet.cell(row=5, column=4, value=f"{inspection.client}")  # 業主/現場連絡人
    sheet.cell(row=5, column=10, value=f"{inspection.incident_date}")  # 發生日期
    sheet.cell(row=5, column=13, value=f"{inspection.lifetime}")  # 使用壽命
    sheet.cell(row=6, column=4, value=f"{inspection.hswe_name}")  # 負責人
    sheet.cell(row=6, column=10, value=f"{inspection.online_date}")  # 上線日期
    sheet.cell(row=7, column=4, value=f"{inspection.sn}")  # 型號&序號
    sheet.cell(row=7, column=10, value=f"{inspection.return_date}")  # 取回日期
    sheet.cell(row=8, column=4, value=f"{inspection.system}")  # 系統&TagNO
    sheet.cell(row=8, column=10, value=f"{inspection.start_date}")  # 檢驗日期
    sheet.cell(row=11, column=6, value=f"{inspection.sample_value}")  # ph值
    sheet.cell(row=11, column=11, value=f"{inspection.sample_conductivity}")  # 導電度
    sheet.cell(row=12, column=6, value=f"{inspection.sample_pressure}")  # 壓力
    sheet.cell(row=12, column=11, value=f"{inspection.sample_temperature}")  # 溫度
    sheet.cell(row=13, column=6, value=f"{inspection.install_type}")  # 安裝方式
    sheet.cell(row=13, column=11, value=f"{inspection.avg_life}")  # 電極平均壽命
    # 設定響應頭
    response = HttpResponse(content_type='application/msexcel')
    # 設定下載檔案編碼，需要使用urlquote
    filename = urlquote(f'{inspection.form_id}.xlsx')
    response[
    'Content-Disposition'] = f"attachment;filename*=utf-8'zh_cn'{filename}"
    # 儲存Excel到相應中
    wb.save(response)
    return response


def report_search(request):
    records = Inspection.objects.values('form_id', 'hswe_name')
    return render(request, "report_search.html", {'records': records})






