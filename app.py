"""CivicProof AI — evidence-based government notification assistant."""
from datetime import date
import streamlit as st
from modules.document_reader import extract_pdf_text, MAX_UPLOAD_BYTES
from modules.ai_analyzer import analyze_document, explain_document
from modules.verification import verify_document, compare_versions
from modules.citizen_assistant import assess_applicability, build_checklist

st.set_page_config(page_title="CivicProof AI", page_icon="🏛️", layout="wide")
st.markdown("""
<style>
 .stApp {background:#f5f7fa;color:#172b4d}
 .hero {background:linear-gradient(120deg,#102a43,#087e8b);padding:2rem;border-radius:18px;color:white;margin-bottom:1rem}
 .hero h1,.hero p {color:white}
 div[data-testid="stMetric"] {background:white;padding:1rem;border:1px solid #e4eaf0;border-radius:12px}
 .disclaimer {background:#fff7e6;border-left:4px solid #d99b22;padding:1rem;border-radius:8px}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🏛️ CivicProof AI</h1><p>Understand public notifications, compare available references, and see what you may need to do next.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="disclaimer"><b>Important:</b> CivicProof AI provides informational assistance. A reference match is not proof of authenticity, and a discrepancy is not proof of fraud. Confirm decisions and deadlines with the issuing authority.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("CivicProof AI")
    section = st.radio("Navigate", ["Home", "Analyze Document", "Verify Document", "Compare Versions", "Citizen Assistant", "About CivicProof"], label_visibility="collapsed")
    st.divider()
    language = st.selectbox("Explanation language", ["English", "Kannada", "Hindi"])
    st.caption("Supported input: text PDFs up to 10 MB, or pasted text. Scanned PDF OCR is not included.")

if "analysis" not in st.session_state: st.session_state.analysis = None
if "verification" not in st.session_state: st.session_state.verification = None
if "source_text" not in st.session_state: st.session_state.source_text = ""

def run_analysis(text):
    if not text.strip():
        st.error("Add readable notification text before analyzing.")
        return
    with st.spinner("Analyzing notification with Gemini…"):
        try:
            result = analyze_document(text)
            st.session_state.analysis = result
            st.session_state.source_text = text
            st.session_state.verification = verify_document(result)
            st.success("Analysis complete.")
        except Exception as exc:
            st.error(str(exc))

if section in ("Home", "Analyze Document"):
    st.subheader("Analyze a notification")
    st.write("Upload a PDF or paste the notification text. The app extracts key information and checks it against its locally curated reference collection.")
    uploaded = st.file_uploader("Upload government notification (PDF, maximum 10 MB)", type=["pdf"], help=f"Maximum size: {MAX_UPLOAD_BYTES // (1024*1024)} MB")
    pdf_text = ""
    if uploaded is not None:
        st.caption(f"Selected file: {uploaded.name}")
        try:
            pdf_text = extract_pdf_text(uploaded)
            with st.expander("Preview extracted PDF text"):
                st.text(pdf_text[:12000] + ("…" if len(pdf_text) > 12000 else ""))
        except ValueError as exc:
            st.error(str(exc))
    pasted = st.text_area("Or paste notification text", height=220, placeholder="Paste the text of a government notification here…")
    if st.button("Analyze notification", type="primary", use_container_width=True):
        run_analysis(pasted.strip() or pdf_text)
    st.markdown("#### What you can explore")
    a,b,c = st.columns(3)
    a.info("**Understand**\n\nGet key details and a plain-language explanation.")
    b.info("**Compare**\n\nCheck for differences against curated references.")
    c.info("**Act**\n\nReview dates, eligibility, evidence, and a checklist.")

analysis = st.session_state.analysis
verification = st.session_state.verification
if analysis:
    st.divider()
    st.header("Analysis results")
    overview = [analysis.get("document_title"), analysis.get("issuing_authority"), analysis.get("notification_number"), analysis.get("publication_date"), analysis.get("effective_date")]
    cols = st.columns(5)
    for col, label, val in zip(cols, ["Title", "Issuing authority", "Notification no.", "Published", "Effective"], overview):
        col.metric(label, str(val) if val else "Not specified")
    results_tab, verify_tab, eligibility_tab, dates_tab, explanation_tab, checklist_tab, evidence_tab = st.tabs(["Overview", "Verification", "Eligibility", "Important dates", "Simple explanation", "Action checklist", "Evidence & sources"])
    with results_tab:
        for heading, key in [("Scheme or policy", "scheme_or_policy_name"), ("Who is affected", "people_affected"), ("Eligibility criteria", "eligibility_criteria"), ("Main provisions", "main_provisions"), ("Warnings", "important_warnings")]:
            value = analysis.get(key)
            if value:
                st.markdown(f"**{heading}**")
                if isinstance(value, list):
                    for item in value: st.write(f"- {item}")
                else: st.write(value)
        if analysis.get("uncertainties"):
            st.warning("Uncertain or inferred information: " + "; ".join(map(str, analysis["uncertainties"])))
    with verify_tab:
        if verification:
            st.subheader(verification["status"])
            st.write(verification["summary"])
            ref = verification.get("reference")
            if ref:
                st.markdown(f"**Reference:** {ref.get('title','Untitled')} · {ref.get('document_id','')}")
                st.caption(f"Status in database: {ref.get('status','Not specified')}")
                if ref.get("official_url"):
                    st.link_button("Open stored reference source", ref["official_url"])
                else: st.caption("No official link is available for this reference.")
            for label, items in [("Matching fields", verification.get("matches", [])), ("Differences", verification.get("differences", []))]:
                st.markdown(f"**{label}**")
                if items: st.dataframe(items, use_container_width=True, hide_index=True)
                else: st.caption("No comparable fields found.")
    with eligibility_tab:
        category = st.selectbox("Your category", ["Not specified", "Student", "Farmer", "Job Seeker", "Senior Citizen", "Business Owner", "Other"], key="category")
        details = st.text_input("Relevant details (optional)", placeholder="Only include details relevant to the stated conditions")
        if st.button("Check applicability", key="check_applicability"):
            st.session_state.applicability = assess_applicability(analysis, category, details)
        if st.session_state.get("applicability"):
            result = st.session_state.applicability
            st.info(f"**{result['result']}**\n\n{result['reason']}")
            st.caption("This is an informational comparison, not an official eligibility decision.")
    with dates_tab:
        date_rows = [("Publication date", analysis.get("publication_date")), ("Effective date", analysis.get("effective_date")), ("Application deadline", analysis.get("application_deadline"))]
        for label, value in date_rows:
            value = value or "Not specified"
            st.write(f"**{label}:** {value}")
            if value != "Not specified" and label == "Application deadline":
                try:
                    deadline = date.fromisoformat(str(value)[:10])
                    st.warning("Deadline has passed." if deadline < date.today() else "Deadline is approaching." if (deadline-date.today()).days <= 30 else "Deadline is not within the next 30 days.")
                except ValueError: st.caption("Deadline status could not be calculated because its date format is ambiguous.")
    with explanation_tab:
        if st.button(f"Generate explanation in {language}", type="primary"):
            with st.spinner("Preparing a plain-language explanation…"):
                try: st.session_state.explanation = explain_document(analysis, language)
                except Exception as exc: st.error(str(exc))
        if st.session_state.get("explanation"): st.markdown(st.session_state.explanation)
    with checklist_tab:
        st.caption("Checklist items are derived from extracted notification content. Verify each step with the source authority.")
        for i, item in enumerate(build_checklist(analysis)):
            st.checkbox(item, key=f"checklist_{i}")
    with evidence_tab:
        passages = analysis.get("source_passages") or []
        if passages:
            for passage in passages:
                if isinstance(passage, dict): st.markdown(f"**{passage.get('field','Source passage')}**\n\n> {passage.get('quote','')}")
                else: st.write(passage)
        else: st.caption("No supporting passages were returned by the analyzer.")
        if verification and verification.get("reference"):
            ref = verification["reference"]
            st.markdown(f"**Reference document:** {ref.get('title','Untitled')}")
            st.markdown(f"> {ref.get('content','No reference passage is available.')}")
            if ref.get("official_url"): st.link_button("Open official source", ref["official_url"])
            else: st.caption("No official link is available.")

if section == "Verify Document":
    st.subheader("Verify against curated references")
    st.write("Run analysis above to see the deterministic reference comparison and supporting fields.")
if section == "Compare Versions":
    st.subheader("Compare versions")
    comparison = compare_versions(verification.get("reference") if verification else None, analysis or {})
    st.write(comparison["message"])
    if comparison.get("related_document_ids"): st.write("Related records:", ", ".join(comparison["related_document_ids"]))
if section == "Citizen Assistant":
    st.subheader("Citizen assistant")
    st.write("Analyze a notification to see its eligibility comparison, important dates, explanation, and checklist here.")
if section == "About CivicProof":
    st.subheader("About CivicProof AI")
    st.write("CivicProof AI helps make complex notifications easier to understand. It compares documents only against references maintained in its local database; it does not perform live government source discovery or issue official decisions.")
    st.markdown("**Supported languages:** English, Kannada, Hindi  \n**PDF limit:** 10 MB  \n**Privacy:** Uploaded text is sent to Google Gemini for analysis when configured and is not stored by this app on disk.")
