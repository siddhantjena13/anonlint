from core.findings import (
    CheckResult,
    CheckStatus,
    Finding,
    PdfMetadataLocation,
)

CHECK_ID = "metadata.pdf_author"

AUTHOR_FIELDS = ["/Author", "/Creator"]


def check_pdf_author(metadata: dict[str, str]) -> CheckResult:
    """Flag PDF metadata fields that appear to contain an author's name."""
    findings = []

    for field_name in AUTHOR_FIELDS:
        value = metadata.get(field_name)
        if not value:
            continue

        findings.append(
            Finding(
                check_id=CHECK_ID,
                message=f"PDF {field_name} field is set",
                location=PdfMetadataLocation(field_name=field_name),
                confidence=0.9,
                evidence=value,
                remediation=f"Run: exiftool {field_name[1:]}= paper.pdf",
            )
        )

    if findings:
        return CheckResult(
            check_id=CHECK_ID, status=CheckStatus.FLAGGED, findings=findings
        )

    return CheckResult(check_id=CHECK_ID, status=CheckStatus.CLEAN)