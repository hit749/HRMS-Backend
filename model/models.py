from mongoengine import *
from datetime import datetime, date
from config import settings
import certifi

# DB connection (unchanged)
dbhost = settings["DB_HOST"]
dbusername = settings["DATA_DB_USERNAME"]
dbpassword = settings["DATA_DB_PASSWORD"]
dbname = settings["DATA_DB_NAME"]

client = connect(
    host="mongodb+srv://admin:admin@hrms.kt85gff.mongodb.net/hrms?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile=certifi.where()
)


class EmployeeStatus:
    ACTIVE = "Active"
    HOLD = "Hold"
    SEPARATION = "Separation"
    INACTIVE = "Inactive"


STATUS_CHOICES = [
    EmployeeStatus.ACTIVE,
    EmployeeStatus.HOLD,
    EmployeeStatus.SEPARATION,
    EmployeeStatus.INACTIVE
]


# Employee Master Table
class Employee(Document):
    employee_id = IntField(required=True, unique=True)
    status = status = StringField(choices=STATUS_CHOICES, default=EmployeeStatus.ACTIVE)
    category = StringField(required=True)           
    category_code = IntField(required=True)
    state = StringField(required=True)
    employee_name = StringField(required=True, regex=r'^[A-Za-z ]+$')
    first_name = StringField(required=True, regex=r'^[A-Za-z ]+$')
    last_name = StringField(required=True, regex=r'^[A-Za-z ]+$')
    dob = DateTimeField(required=True)
    gender = StringField(required=True, choices=("male", "female", "other"))
    doj = DateTimeField(required=True)
    dos = DateTimeField(required=True)
    groj = DateTimeField()
    email = EmailField(required=True, unique=True)
    phone = StringField(required=True)
    location_code = IntField(required=True)
    location_desc = StringField(required=True)
    department_code = IntField(required=True)
    department_desc = StringField(required=True)
    designation = StringField(required=True, regex=r'^[A-Za-z ]+$')
    grade = StringField(required=True)
    cost_centre_number = IntField(required=True)
    uan_number = LongField(required=True)
    bank_code = IntField(required=True)
    bank_name = StringField(required=True, regex=r'^[A-Za-z ]+$')
    bank_ifsc = StringField(required=True, regex=r'^[A-Za-z0-9]+$')
    bank_account_number = StringField(required=True, regex=r'^[0-9]+$')
    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "employee_master",
        "ordering": ["cr_at"]
    }


class Bank(Document):

    code = IntField(required=True)

    param1 = StringField()
    param2 = StringField()
    param3 = FloatField()
    param4 = FloatField()
    param5 = FloatField()

    arrear = FloatField()
    prorate = FloatField()
    lwp_flag = FloatField()
    taxable = FloatField()
    rfa_prk = FloatField()
    fc_prt = FloatField()

    cap = IntField()
    esic = FloatField()
    lwf = FloatField()
    conv = FloatField()
    pf = FloatField()
    lip = FloatField()
    mediclaim = FloatField()
    notice = FloatField()
    lv_encash = FloatField()
    gratuity = FloatField()
    hra = FloatField()
    da = FloatField()
    ot = FloatField()
    payslip = FloatField()
    reimb_fld = FloatField()

    reimb_cd = IntField()
    legacy_cd = FloatField()
    rate_cd = FloatField()
    mst2pay = FloatField()
    hre = FloatField()
    sec10pyrl = FloatField()
    sec10_med = FloatField()
    pt_flag = FloatField()
    oth_flag = FloatField()

    param6 = FloatField()
    param7 = FloatField()
    param8 = FloatField()
    param9 = FloatField()
    param10 = FloatField()
    param11 = FloatField()
    param12 = FloatField()
    param13 = FloatField()
    param14 = FloatField()
    param15 = FloatField()

    user_log = StringField()
    ytd_total = IntField()

    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "bank",
        "ordering": ["code"]
    }


class Location(Document):

    ms_code = IntField(required=True)
    ms_descr = StringField()

    ms_param1 = StringField()
    ms_param2 = StringField()
    ms_param3 = StringField()
    ms_param4 = StringField()
    ms_param5 = StringField()
    ms_param6 = StringField()

    user_log = StringField()

    esi_perc = FloatField()
    esi_end_dt = DateTimeField()
    esi_code = IntField()

    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "location",
        "ordering": ["ms_code"]
    }


class PTMast(Document):

    pt_code = IntField(required=True)
    pt_state = StringField()
    pt_month = IntField()
    pt_descr = StringField()

    pt_slab_fr = FloatField()
    pt_slab_to = FloatField()
    pt_rate = FloatField()
    pt_add_mon = FloatField()
    pt_add = FloatField()

    pt_remark = StringField()
    pt_lgcy_cd = FloatField()

    opt_flag = FloatField()
    opt_ded_mo = FloatField()
    sal_proj = FloatField()
    opt_sal_mo = FloatField()
    opt_slb_fr = FloatField()
    opt_slb_to = FloatField()
    opt_rate = FloatField()

    sal_fld = FloatField()
    user_log = StringField()

    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "pt_mast",
        "ordering": ["pt_code"]
    }


class Tax(Document):

    code = IntField(required=True)

    param1 = StringField()
    param2 = StringField()
    param3 = FloatField()
    param4 = FloatField()
    param5 = FloatField()

    arrear = FloatField()
    prorate = FloatField()
    lwp_flag = FloatField()
    taxable = FloatField()
    rfa_prk = FloatField()
    fc_prt = FloatField()

    cap = FloatField()
    esic = FloatField()
    lwf = FloatField()
    conv = FloatField()
    pf = FloatField()
    lip = FloatField()
    mediclaim = FloatField()
    notice = FloatField()
    lv_encash = FloatField()
    gratuity = FloatField()
    hra = FloatField()
    da = FloatField()
    ot = FloatField()
    payslip = FloatField()
    reimb_fld = FloatField()

    reimb_cd = FloatField()
    legacy_cd = FloatField()
    rate_cd = FloatField()
    mst2pay = FloatField()
    hre = FloatField()
    sec10pyrl = FloatField()
    sec10_med = FloatField()
    pt_flag = FloatField()
    oth_flag = FloatField()

    param6 = FloatField()
    param7 = FloatField()
    param8 = FloatField()
    param9 = FloatField()
    param10 = FloatField()
    param11 = FloatField()
    param12 = FloatField()
    param13 = FloatField()
    param14 = FloatField()
    param15 = FloatField()

    user_log = StringField()
    ytd_total = FloatField()

    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "tax",
        "ordering": ["code"]
    }


class CTC(Document):

    code = IntField(required=True)

    param1 = StringField()
    param2 = StringField()
    param3 = FloatField()
    param4 = FloatField()
    param5 = FloatField()

    arrear = FloatField()
    prorate = FloatField()
    lwp_flag = FloatField()
    taxable = FloatField()
    rfa_prk = FloatField()
    fc_prt = FloatField()

    cap = FloatField()
    esic = FloatField()
    lwf = FloatField()
    conv = FloatField()
    pf = FloatField()
    lip = FloatField()
    mediclaim = FloatField()
    notice = FloatField()
    lv_encash = FloatField()
    gratuity = FloatField()
    hra = FloatField()
    da = FloatField()
    ot = FloatField()
    payslip = FloatField()
    reimb_fld = FloatField()

    reimb_cd = FloatField()
    legacy_cd = FloatField()
    rate_cd = FloatField()
    mst2pay = FloatField()
    hre = FloatField()
    sec10pyrl = FloatField()
    sec10_med = FloatField()
    pt_flag = FloatField()
    oth_flag = FloatField()

    param6 = FloatField()
    param7 = FloatField()
    param8 = FloatField()
    param9 = FloatField()
    param10 = FloatField()
    param11 = FloatField()
    param12 = FloatField()
    param13 = FloatField()
    param14 = FloatField()
    param15 = FloatField()

    user_log = StringField()
    ytd_total = FloatField()

    cr_at = DateTimeField(default=datetime.utcnow)
    mo_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "ctc",
        "ordering": ["code"]
    }
    