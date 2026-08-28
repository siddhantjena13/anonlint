from core.checks import check_pdf_author
from core.findings import CheckStatus


def test_clean_metadata_returns_clean():
    result = check_pdf_author({"/Producer": "pdfTeX"})
    assert result.status == CheckStatus.CLEAN
    assert result.findings == []


def test_author_field_is_flagged():
    result = check_pdf_author({"/Author": "Jane Smith"})
    assert result.status == CheckStatus.FLAGGED
    assert len(result.findings) == 1


def test_finding_carries_the_offending_value():
    result = check_pdf_author({"/Author": "Jane Smith"})
    assert result.findings[0].evidence == "Jane Smith"


def test_empty_string_is_not_flagged():
    result = check_pdf_author({"/Author": ""})
    assert result.status == CheckStatus.CLEAN


def test_both_fields_produce_two_findings():
    result = check_pdf_author({"/Author": "Jane Smith", "/Creator": "Jane Smith"})
    assert len(result.findings) == 2

def test_known_software_in_creator_is_not_flagged():
    result = check_pdf_author({"/Creator": "LaTeX with hyperref"})
    assert result.status == CheckStatus.CLEAN


def test_unknown_creator_value_is_flagged():
    result = check_pdf_author({"/Creator": "Jane Smith"})
    assert result.status == CheckStatus.FLAGGED


def test_author_field_is_flagged_regardless_of_value():
    result = check_pdf_author({"/Author": "LaTeX with hyperref"})
    assert result.status == CheckStatus.FLAGGED