"""Deterministic reference matching and discrepancy reporting."""
import json
from pathlib import Path
from rapidfuzz.fuzz import token_set_ratio

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "official_references.json"

def load_references():
    try:
        with DATA_FILE.open(encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []

def _value(obj, key):
    value = obj.get(key)
    return str(value).strip() if value is not None else ""

def verify_document(analysis: dict, references=None) -> dict:
    references = load_references() if references is None else references
    if not references:
        return {"status": "Unverified", "reference": None, "matches": [], "differences": [], "summary": "No curated reference documents are available."}
    candidates = []
    for ref in references:
        score = 0
        for key in ("notification_number", "document_title", "department", "issuing_authority"):
            a, b = _value(analysis, key).casefold(), _value(ref, {"document_title":"title", "issuing_authority":"issuer"}.get(key, key)).casefold()
            if a and b:
                score += 4 if a == b else (1 if token_set_ratio(a, b) >= 82 else 0)
        candidates.append((score, ref))
    score, ref = max(candidates, key=lambda item: item[0])
    if score == 0:
        return {"status": "Unverified", "reference": None, "matches": [], "differences": [], "summary": "No suitable reference was found. This does not mean the document is fake."}
    pairs = [("notification_number", "notification_number"), ("publication_date", "publication_date"),
             ("effective_date", "effective_date"), ("application_deadline", "deadline")]
    matches, differences = [], []
    for uploaded_key, reference_key in pairs:
        left, right = _value(analysis, uploaded_key), _value(ref, reference_key)
        if left and right:
            row = {"field": uploaded_key.replace("_", " ").title(), "uploaded": left, "reference": right}
            (matches if left.casefold() == right.casefold() else differences).append(row)
    title_left, title_right = _value(analysis, "document_title"), _value(ref, "title")
    issuer_left, issuer_right = _value(analysis, "issuing_authority"), _value(ref, "issuer")
    identity_match = ((title_left and token_set_ratio(title_left, title_right) >= 85) or
                      (_value(analysis, "notification_number") and _value(analysis, "notification_number").casefold() == _value(ref, "notification_number").casefold()))
    meaningful = [d for d in differences if d["field"] in ("Notification Number", "Application Deadline", "Effective Date")]
    if identity_match and meaningful:
        status = "Inconsistent"
    elif identity_match and (not title_left or not title_right or not issuer_left or not issuer_right):
        status = "Corroborated"
    elif identity_match:
        status = "Official Match"
    else:
        status = "Corroborated"
    if status == "Official Match":
        summary = "Identifying details matched this curated reference. This is a database comparison, not a guarantee of authenticity."
    elif status == "Inconsistent":
        summary = "One or more key fields differ from the matching reference. A discrepancy does not by itself establish fraud."
    else:
        summary = "Some identifying details are supported by a reference, but a complete match was not established."
    return {"status": status, "reference": ref, "matches": matches, "differences": differences, "summary": summary}

def compare_versions(reference: dict, analysis: dict) -> dict:
    if not reference:
        return {"available": False, "message": "Version history could not be established because no reference matched."}
    related = reference.get("related_document_ids") or []
    if not related:
        return {"available": False, "message": "The curated database contains no related versions, so version history could not be established."}
    return {"available": True, "message": "Related version records are listed in the reference database.", "related_document_ids": related}
