from pydantic import BaseModel, Field

from typing import Optional


class Record(BaseModel):
    """Class for metadata record."""
    batch_flowcell_id: Optional[str] = Field(None, title="Batch Flowcell ID")
    batch_label: Optional[str] = Field(None, title="Batch Label")
    bg_due_date: Optional[str] = Field(None, title="BG Due Date")
    bill_type: Optional[str] = Field(None, title="Bill Type")
    client_test_code: Optional[str] = Field(None, title="Client Test Code")
    family_id: Optional[str] = Field(None, title="Family ID")
    gender: Optional[str] = Field(None, title="The patient gender.")
    is_hold: Optional[str] = Field(None, title="Is hold")
    lab_number: Optional[str] = Field(None, title="Lab Number")
    batch_id: Optional[str] = Field(None, title="Batch ID")
    case_id: Optional[str] = Field(None, title="Case ID")
    midpool: Optional[str] = Field(None, title="Midpool")
    note: Optional[str] = Field(None, title="Note")
    original_lab_number: Optional[str] = Field(None, title="Original Lab Number")
    pipeline: Optional[str] = Field(None, title="Pipeline")
    pipeline_run_id: Optional[str] = Field(None, title="Pipeline Run ID")
    r_number: Optional[str] = Field(None, title="R Number")
    reflex_lab_number: Optional[str] = Field(None, title="Reflex Lab Number")
    sample_name: Optional[str] = Field(None, title="Sample Name")
    specimen_type: Optional[str] = Field(None, title="Specimen Type")
    test_code: Optional[str] = Field(None, title="Test Code")
    test_name: Optional[str] = Field(None, title="Test Name")
    time_json_generated: Optional[str] = Field(None, title="Time JSON Generated")
    variant_count: Optional[str] = Field(None, title="Variant Count")
    version: Optional[str] = Field(None, title="Version")
    variant_type: Optional[str] = Field(None, title="Variant Type")
    variant_subtype: Optional[str] = Field(None, title="Variant Subtype")

