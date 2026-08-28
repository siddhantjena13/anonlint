from core.findings import (
    CheckResult,
    CheckStatus,
    Finding,
    PdfMetadataLocation,
)

CHECK_ID = "metadata.pdf_author"

KNOWN_SOFTWARE = [
    "latex",
    "pdftex",
    "xetex",
    "luatex",
    "microsoft word",
    "adobe",
    "acrobat",
    "quartz",
    "skia",
    "chromium",
    "libreoffice",
    "openoffice",
    "ghostscript",
]


def looks_like_software(value: str) -> bool:
    """True if the value appears to name a program rather than a person."""
    lowered = value.lower()
    return any(name in lowered for name in KNOWN_SOFTWARE)


def check_pdf_author(metadata: dict[str, str]) -> CheckResult:
    """Flag PDF metadata fields that appear to contain an author's name."""
    findings = []

    for field_name in ["/Author", "/Creator"]:
        value = metadata.get(field_name)
        if not value:
            continue

        if field_name == "/Creator" and looks_like_software(value):
            continue

        confidence = 0.95 if field_name == "/Author" else 0.6

        findings.append(
            Finding(
                check_id=CHECK_ID,
                message=f"PDF {field_name} field is set",
                location=PdfMetadataLocation(field_name=field_name),
                confidence=confidence,
                evidence=value,
                remediation=f"Run: exiftool {field_name[1:]}= paper.pdf",
            )
        )

    if findings:
        return CheckResult(
            check_id=CHECK_ID, status=CheckStatus.FLAGGED, findings=findings
        )

    return CheckResult(check_id=CHECK_ID, status=CheckStatus.CLEAN)