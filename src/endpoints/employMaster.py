from fastapi import APIRouter, HTTPException, Body
from model.models import Employee
from datetime import datetime

router = APIRouter(
    prefix="/api/employees",
    tags=["Employee Master"]
)

# ---------- helpers ----------
DT_FIELDS = ["dob", "doj", "dos", "groj", "cr_at", "mo_at"]

def parse_dt(value):
    if value is None or value == "":
        return None

    # handle "Z"
    if isinstance(value, str) and value.endswith("Z"):
        value = value.replace("Z", "+00:00")

    # date only -> make it datetime
    if isinstance(value, str) and len(value) == 10:  # "YYYY-MM-DD"
        return datetime.fromisoformat(value + "T00:00:00")

    return datetime.fromisoformat(value)

def to_iso(dt):
    if not dt:
        return None
    return dt.isoformat()

def employee_to_dict(emp: Employee):
    return {
        # "id": str(emp.id),

        "employee_id": emp.employee_id,
        "status": emp.status,

        "category": emp.category,
        "category_code": emp.category_code,
        "state": emp.state,

        "employee_name": emp.employee_name,
        "first_name": emp.first_name,
        "last_name": emp.last_name,

        "dob": to_iso(emp.dob),
        "gender": emp.gender,
        "doj": to_iso(emp.doj),
        "dos": to_iso(emp.dos),
        "groj": to_iso(emp.groj),

        "email": emp.email,
        "phone": emp.phone,

        "location_code": emp.location_code,
        "location_desc": emp.location_desc,

        "department_code": emp.department_code,
        "department_desc": emp.department_desc,

        "designation": emp.designation,
        "grade": emp.grade,

        "cost_centre_number": emp.cost_centre_number,
        "uan_number": emp.uan_number,

        "bank_code": emp.bank_code,
        "bank_name": emp.bank_name,
        "bank_ifsc": emp.bank_ifsc,
        "bank_account_number": emp.bank_account_number,

        "cr_at": to_iso(emp.cr_at),
        "mo_at": to_iso(emp.mo_at),
    }


# ✅ POST – Create Employee
@router.post("/")
def create_employee(payload: dict = Body(...)):
    try:
        print("payload ::", payload)

        # parse datetime fields
        for field in ["dob", "doj", "dos", "groj"]:
            if field in payload:
                payload[field] = parse_dt(payload[field])

        employee = Employee(**payload)
        employee.save()

        return {"message": "Employee created successfully", "id": str(employee.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL Employees (FULL JSON for table)
@router.get("/")
def get_employees():
    try:
        employees = Employee.objects().order_by("employee_name")
        return [employee_to_dict(emp) for emp in employees]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE employee by employee_id
@router.get("/{employee_id}")
def get_employee(employee_id: int):
    emp = Employee.objects(employee_id=employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_to_dict(emp)


# ✅ PUT – Update employee by employee_id
@router.put("/{employee_id}")
def update_employee(employee_id: int, payload: dict = Body(...)):
    try:
        emp = Employee.objects(employee_id=employee_id).first()
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")

        # parse datetime fields if present
        for field in ["dob", "doj", "dos", "groj"]:
            if field in payload:
                payload[field] = parse_dt(payload[field])

        # update modified date
        payload["mo_at"] = datetime.utcnow()

        # update document fields safely
        for k, v in payload.items():
            if hasattr(emp, k):
                setattr(emp, k, v)

        emp.save()
        return {"message": "Employee updated successfully", "employee": employee_to_dict(emp)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete employee by employee_id
@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    try:
        emp = Employee.objects(employee_id=employee_id).first()
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")

        emp.delete()
        return {"message": "Employee deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
