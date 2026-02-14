from fastapi import APIRouter, HTTPException, Body
from model.models import Bank
from datetime import datetime

router = APIRouter(
    prefix="/api/bank",
    tags=["Bank Master"]
)

# ---------- helpers ----------
DT_FIELDS = ["cr_at", "mo_at"]

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

def bank_to_dict(b: Bank):
    return {
        "code": getattr(b, "code", None),

        "param1": getattr(b, "param1", None),
        "param2": getattr(b, "param2", None),
        "param3": getattr(b, "param3", None),
        "param4": getattr(b, "param4", None),
        "param5": getattr(b, "param5", None),

        "arrear": getattr(b, "arrear", None),
        "prorate": getattr(b, "prorate", None),
        "lwp_flag": getattr(b, "lwp_flag", None),
        "taxable": getattr(b, "taxable", None),
        "rfa_prk": getattr(b, "rfa_prk", None),
        "fc_prt": getattr(b, "fc_prt", None),

        "cap": getattr(b, "cap", None),
        "esic": getattr(b, "esic", None),
        "lwf": getattr(b, "lwf", None),
        "conv": getattr(b, "conv", None),
        "pf": getattr(b, "pf", None),
        "lip": getattr(b, "lip", None),
        "mediclaim": getattr(b, "mediclaim", None),
        "notice": getattr(b, "notice", None),
        "lv_encash": getattr(b, "lv_encash", None),
        "gratuity": getattr(b, "gratuity", None),
        "hra": getattr(b, "hra", None),
        "da": getattr(b, "da", None),
        "ot": getattr(b, "ot", None),
        "payslip": getattr(b, "payslip", None),
        "reimb_fld": getattr(b, "reimb_fld", None),

        "reimb_cd": getattr(b, "reimb_cd", None),
        "legacy_cd": getattr(b, "legacy_cd", None),
        "rate_cd": getattr(b, "rate_cd", None),
        "mst2pay": getattr(b, "mst2pay", None),
        "hre": getattr(b, "hre", None),
        "sec10pyrl": getattr(b, "sec10pyrl", None),
        "sec10_med": getattr(b, "sec10_med", None),
        "pt_flag": getattr(b, "pt_flag", None),
        "oth_flag": getattr(b, "oth_flag", None),

        "param6": getattr(b, "param6", None),
        "param7": getattr(b, "param7", None),
        "param8": getattr(b, "param8", None),
        "param9": getattr(b, "param9", None),
        "param10": getattr(b, "param10", None),
        "param11": getattr(b, "param11", None),
        "param12": getattr(b, "param12", None),
        "param13": getattr(b, "param13", None),
        "param14": getattr(b, "param14", None),
        "param15": getattr(b, "param15", None),

        "user_log": getattr(b, "user_log", None),
        "ytd_total": getattr(b, "ytd_total", None),

        "cr_at": b.cr_at.isoformat() if getattr(b, "cr_at", None) else None,
        "mo_at": b.mo_at.isoformat() if getattr(b, "mo_at", None) else None,
    }


# ✅ POST – Create Bank (ONLY code + param1 if you want minimum, else accept full payload)
@router.post("/")
def create_bank(payload: dict = Body(...)):
    try:
        # if you want only code + param1 mandatory, keep these checks
        if "code" not in payload:
            raise HTTPException(status_code=400, detail="code is required")

        bank = Bank(**payload)
        bank.save()

        return {"message": "Bank created successfully", "id": str(bank.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL Banks (FULL JSON for table)
@router.get("/")
def get_banks():
    try:
        items = Bank.objects().order_by("code")
        return [bank_to_dict(x) for x in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE bank by code
@router.get("/{code}")
def get_bank(code: int):
    b = Bank.objects(code=code).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank_to_dict(b)


# ✅ PUT – Update bank by code
@router.put("/{code}")
def update_bank(code: int, payload: dict = Body(...)):
    try:
        b = Bank.objects(code=code).first()
        if not b:
            raise HTTPException(status_code=404, detail="Bank not found")

        # update modified date
        payload["mo_at"] = datetime.utcnow()

        # update document fields safely
        for k, v in payload.items():
            if hasattr(b, k):
                setattr(b, k, v)

        b.save()
        return {"message": "Bank updated successfully", "bank": bank_to_dict(b)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete bank by code
@router.delete("/{code}")
def delete_bank(code: int):
    try:
        b = Bank.objects(code=code).first()
        if not b:
            raise HTTPException(status_code=404, detail="Bank not found")

        b.delete()
        return {"message": "Bank deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
