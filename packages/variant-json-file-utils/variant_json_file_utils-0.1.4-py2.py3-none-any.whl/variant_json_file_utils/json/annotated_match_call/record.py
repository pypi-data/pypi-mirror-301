from pydantic import BaseModel, Field
from typing import List, Optional

class Record(BaseModel):
    """Class for the annotated match call record."""
    chr: Optional[str] = Field(None, title="The chromosome.")
    start: Optional[int] = Field(None, title="The start coordinate.")
    end: Optional[int] = Field(None, title="The end coordinate.")
    ref: Optional[str] = Field(None, title="The reference.")
    alt: Optional[str] = Field(None, title="The alternative.")
    sample_name: Optional[str] = Field(None, title="The sample name.")
    alleles: Optional[List[str]] = Field(None, title="The alleles.")
    allele_indices: Optional[List[int]] = Field(None, title="The allele indices.")
    zyg: Optional[str] = Field(None, title="The zygosity.")
    is_phased: Optional[bool] = Field(None, title="Whether the variant is phased.")
    quality: Optional[float] = Field(None, title="The quality.")
    id: Optional[str] = Field(None, title="The variant ID.")
    filters: Optional[List[str]] = Field(None, title="The filters.")
    build: Optional[str] = Field(None, title="The build.")
    total_depth: Optional[int] = Field(None, title="The total depth.")
    alt_depth: Optional[int] = Field(None, title="The alternative depth.")
    ref_depth: Optional[int] = Field(None, title="The reference depth.")
    vaf: Optional[float] = Field(None, title="The variant allele frequency.")
    vaf_alt: Optional[float] = Field(None, title="The variant allele frequency for the alternative allele.")

    @property
    def vcf(self):
        """Get the variant."""
        return f"{self.chr}_{self.start}_{self.end}_{self.ref}_{self.alt}"
