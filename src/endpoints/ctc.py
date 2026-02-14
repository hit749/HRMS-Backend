from fastapi import APIRouter, HTTPException, Body
from model.models import CTC
from datetime import datetime

router = APIRouter(
    prefix="/api/ctc",
    tags=["CTC Master"]
)

# ---------- helpers ----------
def to_iso(dt):
    if not dt:
        return None
    return dt.isoformat()

def ctc_to_dict(c: CTC):
    return {
        "code": getattr(c, "code", None),

        "param1": getattr(c, "param1", None),
        "param2": getattr(c, "param2", None),
        "param3": getattr(c, "param3", None),
        "param4": getattr(c, "param4", None),
        "param5": getattr(c, "param5", None),

        "arrear": getattr(c, "arrear", None),
        "prorate": getattr(c, "prorate", None),
        "lwp_flag": getattr(c, "lwp_flag", None),
        "taxable": getattr(c, "taxable", None),
        "rfa_prk": getattr(c, "rfa_prk", None),
        "fc_prt": getattr(c, "fc_prt", None),

        "cap": getattr(c, "cap", None),
        "esic": getattr(c, "esic", None),
        "lwf": getattr(c, "lwf", None),
        "conv": getattr(c, "conv", None),
        "pf": getattr(c, "pf", None),
        "lip": getattr(c, "lip", None),
        "mediclaim": getattr(c, "mediclaim", None),
        "notice": getattr(c, "notice", None),
        "lv_encash": getattr(c, "lv_encash", None),
        "gratuity": getattr(c, "gratuity", None),
        "hra": getattr(c, "hra", None),
        "da": getattr(c, "da", None),
        "ot": getattr(c, "ot", None),
        "payslip": getattr(c, "payslip", None),
        "reimb_fld": getattr(c, "reimb_fld", None),

        "reimb_cd": getattr(c, "reimb_cd", None),
        "legacy_cd": getattr(c, "legacy_cd", None),
        "rate_cd": getattr(c, "rate_cd", None),
        "mst2pay": getattr(c, "mst2pay", None),
        "hre": getattr(c, "hre", None),
        "sec10pyrl": getattr(c, "sec10pyrl", None),
        "sec10_med": getattr(c, "sec10_med", None),
        "pt_flag": getattr(c, "pt_flag", None),
        "oth_flag": getattr(c, "oth_flag", None),

        "param6": getattr(c, "param6", None),
        "param7": getattr(c, "param7", None),
        "param8": getattr(c, "param8", None),
        "param9": getattr(c, "param9", None),
        "param10": getattr(c, "param10", None),
        "param11": getattr(c, "param11", None),
        "param12": getattr(c, "param12", None),
        "param13": getattr(c, "param13", None),
        "param14": getattr(c, "param14", None),
        "param15": getattr(c, "param15", None),

        "user_log": getattr(c, "user_log", None),
        "ytd_total": getattr(c, "ytd_total", None),

        "cr_at": c.cr_at.isoformat() if getattr(c, "cr_at", None) else None,
        "mo_at": c.mo_at.isoformat() if getattr(c, "mo_at", None) else None,
    }



# ✅ POST – Create CTC
@router.post("/")
def create_ctc(payload: dict = Body(...)):
    try:
        if "code" not in payload:
            raise HTTPException(status_code=400, detail="code is required")

        ctc = CTC(**payload)
        ctc.save()

        return {"message": "CTC created successfully", "id": str(ctc.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL CTC
@router.get("/")
def get_ctc():
    try:
        items = CTC.objects().order_by("code")
        return [ctc_to_dict(x) for x in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE CTC by code
@router.get("/{code}")
def get_single_ctc(code: int):
    c = CTC.objects(code=code).first()
    if not c:
        raise HTTPException(status_code=404, detail="CTC not found")

    return ctc_to_dict(c)


# ✅ PUT – Update CTC
@router.put("/{code}")
def update_ctc(code: int, payload: dict = Body(...)):
    try:
        c = CTC.objects(code=code).first()
        if not c:
            raise HTTPException(status_code=404, detail="CTC not found")

        payload["mo_at"] = datetime.utcnow()

        for k, v in payload.items():
            if hasattr(c, k):
                setattr(c, k, v)

        c.save()

        return {
            "message": "CTC updated successfully",
            "ctc": ctc_to_dict(c)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete CTC
@router.delete("/{code}")
def delete_ctc(code: int):
    try:
        c = CTC.objects(code=code).first()
        if not c:
            raise HTTPException(status_code=404, detail="CTC not found")

        c.delete()
        return {"message": "CTC deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
