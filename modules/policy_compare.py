"""Field-level comparison helpers."""
from .verification import verify_document

def compare_with_reference(analysis, references=None):
    return verify_document(analysis, references)
