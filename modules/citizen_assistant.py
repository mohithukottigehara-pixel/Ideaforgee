"""Citizen applicability and checklist helpers."""

def assess_applicability(analysis: dict, category: str, details: str = "") -> dict:
    criteria = analysis.get("eligibility_criteria")
    if not criteria:
        return {"result": "Eligibility cannot be determined from the available document", "reason": "No eligibility conditions were extracted."}
    if not category or category == "Not specified":
        return {"result": "More information is required", "reason": "Select a citizen category to compare with the stated conditions."}
    criteria_text = str(criteria).casefold()
    supplied = (category + " " + details).casefold()
    if any(term in criteria_text for term in ("all applicant", "any citizen", "all students", "all farmers")):
        return {"result": "Appears eligible based on provided information", "reason": "The document describes broad eligibility. This is guidance, not an official decision."}
    if any(word in criteria_text for word in supplied.split() if len(word) > 4):
        return {"result": "Appears eligible based on provided information", "reason": "Some provided details appear in the stated conditions. Confirm all requirements with the issuing authority."}
    return {"result": "More information is required", "reason": "The document's conditions could not be reliably matched to the information provided."}

def build_checklist(analysis: dict) -> list[str]:
    items = []
    for action in analysis.get("citizen_actions") or []:
        text = str(action).strip()
        if text and text not in items:
            items.append(text)
    for doc in analysis.get("required_documents") or []:
        text = f"Prepare: {doc}"
        if text not in items:
            items.append(text)
    deadline = analysis.get("application_deadline")
    if deadline:
        items.append(f"Confirm the application deadline: {deadline}")
    return items or ["Review the notification and confirm requirements through an official source."]
