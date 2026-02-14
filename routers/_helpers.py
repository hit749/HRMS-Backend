def to_dict(doc):
    data = {"id": str(doc.id)}

    for field in doc._fields:
        if field == "id":
            continue
        value = getattr(doc, field, None)

        # convert datetime to iso
        if hasattr(value, "isoformat"):
            data[field] = value.isoformat()
        else:
            data[field] = value

    return data
