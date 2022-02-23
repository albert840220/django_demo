import random
from random import randrange
from datetime import timedelta
import datetime
import dateutil.relativedelta
def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)



health = [50, 60, 70, 80, 90]

c_datetime=f'{random.randint(2020,2021)}-{"%02d" %random.randint(1,12)}-{"%02d" %random.randint(1,28)} {"%02d" % random.randint(0,23)}:{"%02d" % random.randint(0,59)}:{"%02d" % random.randint(0,59)}'
last_pm=f'{random.randint(2020,2021)}-{"%02d" %random.randint(1,12)}-{"%02d" %random.randint(1,28)}'
cur_day = datetime.datetime.strptime(last_pm, "%Y-%m-%d").date()
print(type(datetime.datetime.strptime(last_pm, "%Y-%m-%d")))
prev_day = (datetime.datetime.strptime(last_pm, "%Y-%m-%d")-dateutil.relativedelta.relativedelta(months=1)).date()
# print(random_date(prev_day, cur_day))
# count = 1
# dic_a ={1:"1083KAA-10103 SK",2:"1084KAA-10116 RA",3:"1091YMS-10103 PL",4:"E1085YCW-10201 LW",5:"1081YYF-11101 EW"}
#
# dic_b ={1:"0000905F0001",2:"0000904F0002",3:"0000803F0003",4:"0000701F0002",5:"0000306F0007"}
#
type_nh = ["E",'F','G']
type_q = ["A",'B','C','D']
#
for i in range(5):
    # last_pm = f'{2022}-{"%02d" % random.randint(8, 12)}-{"%02d" % random.randint(1, 28)}'
    last_pm = f'{2022}-2-{"%02d" % random.randint(4,9)}'
    # prev_day = (datetime.datetime.strptime(last_pm, "%Y-%m-%d") - dateutil.relativedelta.relativedelta(months=1)).date()
    prev_day = (datetime.datetime.strptime(last_pm, "%Y-%m-%d") - dateutil.relativedelta.relativedelta(days=7)).date()
    cur_day = datetime.datetime.strptime(last_pm, "%Y-%m-%d").date()
    # c_datetime = f'{random.randint(2021, 2022)}-{"%02d" % random.randint(1, 12)}-{"%02d" % random.randint(1, 28)} {"%02d" % random.randint(0, 23)}:{"%02d" % random.randint(0, 59)}:{"%02d" % random.randint(0, 59)}'
    c_datetime = f'{2022}-{"%02d" % random.randint(1, 12)}-{"%02d" % random.randint(1, 28)} {"%02d" % random.randint(0, 23)}:{"%02d" % random.randint(0, 59)}:{"%02d" % random.randint(0, 59)}'
#
#     count += 1
    print(f"INSERT INTO `eqpt_ph` (`type`, `sn`, `last_pm`, `standard_a`, `standard_b`, `sv1_ph`, `sv2_ph`, `pump_ph`, `factory_id_id`) VALUES ('100{random.choice(type_q)}', '{'%03d' % random.randint(1, 500)}', '{last_pm}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}','{random.randint(1,3)}');")
#     print(f"INSERT INTO `eqpt_cod` (`type`, `sn`, `last_pm`, `standard_c`, `standard_d`, `sv1_cod`, `sv2_cod`, `sv3_cod`, `pump_cod`, `factory_id_id`) VALUES ('100{random.choice(type_nh)}', '{'%03d' % random.randint(1, 500)}', '{last_pm}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}', '{random_date(prev_day, cur_day)}','{random.randint(1,3)}');")