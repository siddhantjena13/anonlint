from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

class Severity(str, Enum):
    """How much a venue cares. Set by the judge, never by a check."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class CheckStatus(str, Enum):
    """Whether the check could do its job — separate from what it found."""

    CLEAN = "clean"        # ran, found nothing
    FLAGGED = "flagged"    # ran, found something
    SKIPPED = "skipped"    # didn't apply (no metadata, not a repo)
    ERRORED = "errored"    # tried and failed (encrypted, corrupt)

class PdfMetadataLocation(BaseModel):
    """A field in the PDF's hidden info, e.g. /Author."""

    kind: Literal["pdf_metadata"] = "pdf_metadata"
    field_name: str


class PdfTextLocation(BaseModel):
    """A character range on a page of extracted PDF text."""

    kind: Literal["pdf_text"] = "pdf_text"
    page: int = Field(ge=1)
    char_start: int = Field(ge=0)
    char_end: int = Field(ge=0)


class FileLocation(BaseModel):
    """A line in a source file."""

    kind: Literal["file"] = "file"
    path: str
    line: int | None = Field(default=None, ge=1)


Location = PdfMetadataLocation | PdfTextLocation | FileLocation


class Finding(BaseModel):
    """One identity leak found in a document."""

    check_id: str
    message: str
    location: Location
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: str | None = None
    remediation: str | None = None
    severity: Severity | None = None

class CheckResult(BaseModel):
    """The outcome of running one check."""

    check_id: str
    status: CheckStatus
    findings: list[Finding] = []
    detail: str | None = None