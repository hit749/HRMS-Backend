from fastapi import APIRouter, HTTPException, Body
from model.models import Location
from datetime import datetime

router = APIRouter(
    prefix="/api/location",
    tags=["Location Master"]
)

# ---------- helpers ----------
def parse_dt(value):
    if value is None or value == "":
        return None

    if isinstance(value, str) and value.endswith("Z"):
        value = value.replace("Z", "+00:00")

    if isinstance(value, str) and len(value) == 10:  # YYYY-MM-DD
        return datetime.fromisoformat(value + "T00:00:00")

    return datetime.fromisoformat(value)

def to_iso(dt):
    if not dt:
        return None
    return dt.isoformat()

def location_to_dict(x: Location):
    return {
        "ms_code": getattr(x, "ms_code", None),
        "ms_descr": getattr(x, "ms_descr", None),

        "ms_param1": getattr(x, "ms_param1", None),
        "ms_param2": getattr(x, "ms_param2", None),
        "ms_param3": getattr(x, "ms_param3", None),
        "ms_param4": getattr(x, "ms_param4", None),
        "ms_param5": getattr(x, "ms_param5", None),
        "ms_param6": getattr(x, "ms_param6", None),

        "user_log": getattr(x, "user_log", None),

        "esi_perc": getattr(x, "esi_perc", None),
        "esi_end_dt": x.esi_end_dt.isoformat() if getattr(x, "esi_end_dt", None) else None,
        "esi_code": getattr(x, "esi_code", None),

        "cr_at": x.cr_at.isoformat() if getattr(x, "cr_at", None) else None,
        "mo_at": x.mo_at.isoformat() if getattr(x, "mo_at", None) else None,
    }



# ✅ POST – Create Location
@router.post("/")
def create_location(payload: dict = Body(...)):
    try:
        if "ms_code" not in payload:
            raise HTTPException(status_code=400, detail="ms_code is required")

        # parse datetime fields
        if "esi_end_dt" in payload:
            payload["esi_end_dt"] = parse_dt(payload["esi_end_dt"])

        loc = Location(**payload)
        loc.save()

        return {"message": "Location created successfully", "id": str(loc.id)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ALL Locations (FULL JSON for table)
@router.get("/")
def get_locations():
    try:
        items = Location.objects().order_by("ms_code")
        return [location_to_dict(x) for x in items]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ GET – Get ONE Location by ms_code
@router.get("/{ms_code}")
def get_location(ms_code: int):
    x = Location.objects(ms_code=ms_code).first()
    if not x:
        raise HTTPException(status_code=404, detail="Location not found")
    return location_to_dict(x)


# ✅ PUT – Update Location by ms_code
@router.put("/{ms_code}")
def update_location(ms_code: int, payload: dict = Body(...)):
    try:
        x = Location.objects(ms_code=ms_code).first()
        if not x:
            raise HTTPException(status_code=404, detail="Location not found")

        # parse datetime fields if present
        if "esi_end_dt" in payload:
            payload["esi_end_dt"] = parse_dt(payload["esi_end_dt"])

        # update modified date
        payload["mo_at"] = datetime.utcnow()

        # update document fields safely
        for k, v in payload.items():
            if hasattr(x, k):
                setattr(x, k, v)

        x.save()
        return {"message": "Location updated successfully", "location": location_to_dict(x)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ DELETE – Delete Location by ms_code
@router.delete("/{ms_code}")
def delete_location(ms_code: int):
    try:
        x = Location.objects(ms_code=ms_code).first()
        if not x:
            raise HTTPException(status_code=404, detail="Location not found")

        x.delete()
        return {"message": "Location deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
