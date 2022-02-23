from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static
import datetime as dt
import dateutil.relativedelta
from jsignature.fields import JSignatureField
from jsignature.mixins import JSignatureFieldsMixin

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="electrodes/profiles/avatars/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static('assets/img/team/default-profile-picture.png')


class Calibration(models.Model):
    c_datetime = models.DateTimeField("日期")
    rfid = models.CharField(max_length=20)
    sensor_sn = models.CharField("序號", max_length=16)
    slope = models.FloatField()
    offset = models.FloatField()
    temperature = models.FloatField("溫度")
    method = models.IntegerField()
    health = models.IntegerField("健康度")
    res_time = models.FloatField()
    act_z = models.FloatField()

    def __str__(self):
        return f"{self.SensorSN}"

    class Meta:
        db_table = "calibrations"
        verbose_name = '校正紀錄'
        verbose_name_plural = "校正紀錄"


class Inspection(models.Model):
    form_id = models.CharField("報告書編號", max_length=20)
    delivery_date = models.DateField("出貨日期")
    client = models.CharField("業主/現場聯絡人", max_length=20)
    incident_date = models.DateField("發生日期")
    lifetime = models.IntegerField("使用壽命")
    hswe_name = models.CharField("負責人", max_length=20)
    online_date = models.DateField("上線日期")
    model = models.CharField("型號", max_length=20, null=True)
    sn = models.CharField("序號", max_length=20)
    return_date = models.DateField("取回日期")
    system = models.CharField("系統", max_length=20)
    tag_no = models.CharField("TagNO", max_length=20, null=True)
    start_date = models.DateField("檢測日期")  # 檢測開始日期
    end_date = models.DateField("檢測結束日期", null=True)
    # error_report = null=False)
    sample_value = models.FloatField("pH值/測值")
    sample_conductivity = models.FloatField("導電度")
    sample_pressure = models.FloatField("壓力")
    sample_temperature = models.FloatField("溫度")
    install_type = models.CharField("安裝方式", max_length=20)
    avg_life = models.IntegerField("電極平均壽命")

    # description =
    # result =
    # system =
    # tag_no =
    class Meta:
        db_table = 'inspections'
        verbose_name = '檢測報告書'
        verbose_name_plural = "檢測報告書"


class Factory(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'factory'


class Customer(models.Model):
    factory_id = models.ForeignKey(Factory, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    def show_address(self):
        return f"{self.factory_id.city}{self.factory_id.address}" if self.factory_id else None

    class Meta:
        db_table = 'customer'


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"


class Staff(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=20, null=True)
    active = models.CharField(max_length=1, null=True)
    create_Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "staff"


class PmSchedule(models.Model):
    next_maintenance_planned_on = models.DateField()
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    factory_id = models.ForeignKey(Factory, on_delete=models.CASCADE)
    equipment_model = models.CharField(max_length=255, null=True)
    equipment_sn = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    state = models.IntegerField(null=True)

    class Meta:
        db_table = "pm_schedule"


class EqptNh(models.Model):
    factory_id = models.ForeignKey(Factory, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, null=True)
    sn = models.CharField(max_length=255, null=True)
    last_pm = models.DateField()
    sv1_nh = models.DateField()
    sv1_nh_lifetime = models.IntegerField(null=True)
    sv2_nh = models.DateField()
    sv2_nh_lifetime = models.IntegerField(null=True)
    sv3_nh = models.DateField()
    sv3_nh_lifetime = models.IntegerField(null=True)
    last_pm_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    state = models.IntegerField(null=True)

    class Meta:
        db_table = "eqpt_NH"


class EqptPh(models.Model):
    factory_id = models.ForeignKey(Factory, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, null=True)
    sn = models.CharField(max_length=255, null=True, unique=True)
    last_pm = models.DateField(null=True)
    standard_a = models.DateField(null=True)
    standard_b = models.DateField(null=True)
    sv1_ph = models.DateField(null=True)
    sv1_ph_lifetime = models.IntegerField(null=True)
    sv2_ph = models.DateField(null=True)
    sv2_ph_lifetime = models.IntegerField(null=True)
    pump_ph = models.DateField(null=True)
    pump_ph_lifetime = models.IntegerField(null=True)
    last_pm_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    state = models.IntegerField(null=True)

    def days_used_for_standard_a(self):
        return (dt.date.today() - self.standard_a).days if self.standard_a else None

    def days_used_for_standard_b(self):
        return (dt.date.today() - self.standard_b).days if self.standard_b else None

    def days_used_for_sv1_ph(self):
        return (dt.date.today() - self.sv1_ph).days if self.sv1_ph else None

    def days_used_for_sv2_ph(self):
        return (dt.date.today() - self.sv2_ph).days if self.sv2_ph else None

    def days_used_for_pump_ph(self):
        return (dt.date.today() - self.pump_ph).days if self.pump_ph else None

    def sv1_lifetime(self):
        return str((dt.datetime.strptime(str(self.sv1_ph), "%Y-%m-%d") + dateutil.relativedelta.relativedelta(
            months=self.sv1_ph_lifetime)).date()) if self.sv1_ph_lifetime else None

    def sv2_lifetime(self):
        return str((dt.datetime.strptime(str(self.sv2_ph), "%Y-%m-%d") + dateutil.relativedelta.relativedelta(
            months=self.sv2_ph_lifetime)).date()) if self.sv2_ph_lifetime else None

    class Meta:
        db_table = "eqpt_pH"


class EqptCod(models.Model):
    factory_id = models.ForeignKey(Factory, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, null=True)
    sn = models.CharField(max_length=255, null=True)
    last_pm = models.DateField()
    standard_c = models.DateField()
    standard_d = models.DateField()
    sv1_cod = models.DateField()
    sv1_cod_lifetime = models.IntegerField(null=True)
    sv2_cod = models.DateField()
    sv2_cod_lifetime = models.IntegerField(null=True)
    sv3_cod = models.DateField()
    sv3_cod_lifetime = models.IntegerField(null=True)
    pump_cod = models.DateField()
    pump_cod_lifetime = models.IntegerField(null=True)
    last_pm_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    state = models.IntegerField(null=True)

    def days_used_for_standard_c(self):
        return (dt.date.today() - self.standard_c).days if self.standard_c else None

    def days_used_for_standard_d(self):
        return (dt.date.today() - self.standard_d).days if self.standard_d else None

    def days_used_for_sv1_cod(self):
        return (dt.date.today() - self.sv1_cod).days if self.sv1_cod else None

    def days_used_for_sv2_cod(self):
        return (dt.date.today() - self.sv2_cod).days if self.sv2_cod else None

    def days_used_for_pump_cod(self):
        return (dt.date.today() - self.pump_cod).days if self.pump_cod else None

    def sv1_lifetime(self):
        return str((dt.datetime.strptime(str(self.sv1_cod), "%Y-%m-%d") + dateutil.relativedelta.relativedelta(
            months=self.sv1_cod_lifetime)).date())

    def sv2_lifetime(self):
        return str((dt.datetime.strptime(str(self.sv2_cod), "%Y-%m-%d") + dateutil.relativedelta.relativedelta(
            months=self.sv2_cod_lifetime)).date())

    class Meta:
        db_table = "eqpt_COD"


class CustomerSurvey(models.Model):
    company = models.CharField(max_length=30)
    # 工作現場
    purpose_of_visit = models.CharField(max_length=30)
    product_description = models.CharField(max_length=30)
    service_attitude = models.CharField(max_length=30)
    customer_advice = models.TextField(null=True, blank=True)
    signature = JSignatureField()
    class Meta:
        db_table = "customer_survey"


# class BusinessVisit(models.Model):
