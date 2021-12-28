from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.templatetags.static import static


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
    c_datetime = models.DateTimeField()
    Rfid = models.CharField(max_length=20)
    SensorSN = models.CharField(max_length=16)
    Slope = models.FloatField()
    Offset = models.FloatField()
    Temperature = models.FloatField()
    Method = models.IntegerField()
    Health = models.IntegerField()
    ResTime = models.FloatField()
    ActZ = models.FloatField()

    # def __str__(self):
    #     return self.c_datetime
    class Meta:
        db_table = "calibrations"

class Transaction(models.Model):
    bill_for = models.CharField(max_length=100)
    issue_date = models.DateField()
    due_date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'datatable'
        # verbose_name = 'transaction'
        # verbose_name_plural = ''

class Inspection(models.Model):
    form_id = models.CharField(max_length=20, null=False)
    delivery_date = models.DateField( null=False)
    client = models.CharField(max_length=20, null=False)
    incident_date = models.DateField( null=False)
    lifetime = models.IntegerField(null=False)
    hswe_name = models.CharField(max_length=20, null=False)
    online_date = models.DateField( null=False)
    type = models.CharField(max_length=20, null=False)
    sn = models.CharField(max_length=20, null=False)
    return_date = models.DateField(null=False)
    system = models.CharField(max_length=20, null=False)
    tag_no = models.CharField(max_length=20, null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField( null=False)
    # error_report , null=False)
    sample_value = models.FloatField( null=False)
    sample_conductivity = models.FloatField( null=False)
    sample_pressure = models.FloatField(null=False)
    sample_temperature = models.FloatField( null=False)
    install_type = models.CharField(max_length=20, null=False)
    avg_life = models.IntegerField( null=False)

    # description =
    # result =
    # system =
    # tag_no =
    class Meta:
        db_table = 'inspections'

