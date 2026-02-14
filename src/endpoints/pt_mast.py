from fastapi import APIRouter, HTTPException, Body
from model.models import PTMast
from datetime import datetime

router = APIRouter(
    prefix="/api/pt_mast",
    tags=["PT Mast Master"]
)

# ---------- helpers ----------
def to_iso(dt):
    if not dt:
        return None
    return dt.isoformat()

def pt_to_dict(x: PTMast):
    return {
        "pt_code": getattr(x, "pt_code", None),
        "pt_state": getattr(x, "pt_state", None),
        "pt_month": getattr(x, "pt_month", None),
        "pt_descr": getattr(x, "pt_descr", None),

        "pt_slab_fr": getattr(x, "pt_slab_fr", None),
        "pt_slab_to": getattr(x, "pt_slab_to", None),
        "pt_rate": getattr(x, "pt_rate", None),
        "pt_add_mon": getattr(x, "pt_add_mon", None),
        "pt_add": getattr(x, "pt_add", None),

        "pt_remark": getattr(x, "pt_remark", None),
        "pt_lgcy_cd": getattr(x, "pt_lgcy_cd", None),

        "opt_flag": getattr(x, "opt_flag", None),
        "opt_ded_mo": getattr(x, "opt_ded_mo", None),
        "sal_proj": getattr(x, "sal_proj", None),
        "opt_sal_mo": getattr(x, "opt_sal_mo", None),
        "opt_slb_fr": getattr(x, "opt_slb_fr", None),
        "opt_slb_to": getattr(x, "opt_slb_to", None),
        "opt_rate": getattr(x, "opt_rate", None),

        "sal_fld": getattr(x, "sal_fld", None),
        "user_log": getattr(x, "user_log", None),

        "cr_at": x.cr_at.isoformat() if getattr(x, "cr_at", None) else None,
        "mo_at": x.mo_at.isoformat() if getattr(x, "mo_at", None) else None,
    }


# ✅ POST – Create PT Mast
@router.post("/")
def create_pt_mast(payload: dict = Body(...)):
    try:
        if "pt_code" not in payload:
            raise HTTPException(status_code=400, detail="pt_code is required")

        pt = PTMast(**payload)
        pt.save()

        return {"message": "PT Mast created successfully", "id": str(pt.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL PT Mast
@router.get("/")
def get_pt_mast():
    try:
        items = PTMast.objects().order_by("pt_code")
        return [pt_to_dict(x) for x in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE PT Mast by pt_code
@router.get("/{pt_code}")
def get_single_pt_mast(pt_code: int):
    x = PTMast.objects(pt_code=pt_code).first()
    if not x:
        raise HTTPException(status_code=404, detail="PT Mast not found")

    return pt_to_dict(x)


# ✅ PUT – Update PT Mast
@router.put("/{pt_code}")
def update_pt_mast(pt_code: int, payload: dict = Body(...)):
    try:
        x = PTMast.objects(pt_code=pt_code).first()
        if not x:
            raise HTTPException(status_code=404, detail="PT Mast not found")

        payload["mo_at"] = datetime.utcnow()

        for k, v in payload.items():
            if hasattr(x, k):
                setattr(x, k, v)

        x.save()

        return {
            "message": "PT Mast updated successfully",
            "pt_mast": pt_to_dict(x)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete PT Mast
@router.delete("/{pt_code}")
def delete_pt_mast(pt_code: int):
    try:
        x = PTMast.objects(pt_code=pt_code).first()
        if not x:
            raise HTTPException(status_code=404, detail="PT Mast not found")

        x.delete()
        return {"message": "PT Mast deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
