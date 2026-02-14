from fastapi import APIRouter, HTTPException, Body
from model.models import Tax
from datetime import datetime

router = APIRouter(
    prefix="/api/tax",
    tags=["Tax Master"]
)

# ---------- helpers ----------
def to_iso(dt):
    if not dt:
        return None
    return dt.isoformat()

def tax_to_dict(x: Tax):
    return {
        "id": str(x.id) if x.id else None,

        "code": getattr(x, "code", None),

        "param1": getattr(x, "param1", None),
        "param2": getattr(x, "param2", None),
        "param3": getattr(x, "param3", None),
        "param4": getattr(x, "param4", None),
        "param5": getattr(x, "param5", None),

        "arrear": getattr(x, "arrear", None),
        "prorate": getattr(x, "prorate", None),
        "lwp_flag": getattr(x, "lwp_flag", None),
        "taxable": getattr(x, "taxable", None),
        "rfa_prk": getattr(x, "rfa_prk", None),
        "fc_prt": getattr(x, "fc_prt", None),

        "cap": getattr(x, "cap", None),
        "esic": getattr(x, "esic", None),
        "lwf": getattr(x, "lwf", None),
        "conv": getattr(x, "conv", None),
        "pf": getattr(x, "pf", None),
        "lip": getattr(x, "lip", None),
        "mediclaim": getattr(x, "mediclaim", None),
        "notice": getattr(x, "notice", None),
        "lv_encash": getattr(x, "lv_encash", None),
        "gratuity": getattr(x, "gratuity", None),
        "hra": getattr(x, "hra", None),
        "da": getattr(x, "da", None),
        "ot": getattr(x, "ot", None),
        "payslip": getattr(x, "payslip", None),
        "reimb_fld": getattr(x, "reimb_fld", None),

        "reimb_cd": getattr(x, "reimb_cd", None),
        "legacy_cd": getattr(x, "legacy_cd", None),
        "rate_cd": getattr(x, "rate_cd", None),
        "mst2pay": getattr(x, "mst2pay", None),
        "hre": getattr(x, "hre", None),
        "sec10pyrl": getattr(x, "sec10pyrl", None),
        "sec10_med": getattr(x, "sec10_med", None),
        "pt_flag": getattr(x, "pt_flag", None),
        "oth_flag": getattr(x, "oth_flag", None),

        "param6": getattr(x, "param6", None),
        "param7": getattr(x, "param7", None),
        "param8": getattr(x, "param8", None),
        "param9": getattr(x, "param9", None),
        "param10": getattr(x, "param10", None),
        "param11": getattr(x, "param11", None),
        "param12": getattr(x, "param12", None),
        "param13": getattr(x, "param13", None),
        "param14": getattr(x, "param14", None),
        "param15": getattr(x, "param15", None),

        "user_log": getattr(x, "user_log", None),
        "ytd_total": getattr(x, "ytd_total", None),

        "cr_at": x.cr_at.isoformat() if getattr(x, "cr_at", None) else None,
        "mo_at": x.mo_at.isoformat() if getattr(x, "mo_at", None) else None,
    }


# ✅ POST – Create Tax
@router.post("/")
def create_tax(payload: dict = Body(...)):
    try:
        if "code" not in payload:
            raise HTTPException(status_code=400, detail="code is required")

        tax = Tax(**payload)
        tax.save()

        return {"message": "Tax created successfully", "id": str(tax.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL Tax
@router.get("/")
def get_tax():
    try:
        items = Tax.objects().order_by("code")
        return [tax_to_dict(x) for x in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE Tax
@router.get("/{code}")
def get_single_tax(code: int):
    x = Tax.objects(code=code).first()
    if not x:
        raise HTTPException(status_code=404, detail="Tax not found")

    return tax_to_dict(x)


# ✅ PUT – Update Tax
@router.put("/{code}")
def update_tax(code: int, payload: dict = Body(...)):
    try:
        x = Tax.objects(code=code).first()
        if not x:
            raise HTTPException(status_code=404, detail="Tax not found")

        payload["mo_at"] = datetime.utcnow()

        for k, v in payload.items():
            if hasattr(x, k):
                setattr(x, k, v)

        x.save()

        return {
            "message": "Tax updated successfully",
            "tax": tax_to_dict(x)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete Tax
@router.delete("/{code}")
def delete_tax(code: int):
    try:
        x = Tax.objects(code=code).first()
        if not x:
            raise HTTPException(status_code=404, detail="Tax not found")

        x.delete()
        return {"message": "Tax deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
