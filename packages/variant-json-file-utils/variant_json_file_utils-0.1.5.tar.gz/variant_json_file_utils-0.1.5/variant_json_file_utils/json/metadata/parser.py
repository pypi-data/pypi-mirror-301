import logging
import os

from typing import Any, Dict, List, Optional

from ... import constants
from .record import Record as MetadataRecord


class Parser:
    """Class for parsing the JSON object containing the metadata."""

    def __init__(self, **kwargs):
        """Constructor for class Parser"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", constants.DEFAULT_OUTDIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        logging.info(f"Instantiated Parser in {os.path.abspath(__file__)}")

    def get_record(self, data: Dict[str, Any]) -> MetadataRecord:
        """Get the metadata record."""
        record = MetadataRecord(
            batch_flowcell_id=data.get("batch_flowcell_id", None),
            batch_labe=data.get("batch_label", None),
            bg_due_date=data.get("bg_due_date", None),
            bill_type=data.get("bill_type", None),
            client_test_code=data.get("client_test_code", None),
            family_id=data.get("family_id", None),
            gender=data.get("gender", None),
            is_hold=data.get("is_hold", None),
            lab_number=data.get("lab_number", None),
            batch_id=data.get("batch_id", None),
            case_id=data.get("case_id", None),
            midpool=data.get("midpool", None),
            note=data.get("note", None),
            original_lab_number=data.get("original_lab_number", None),
            pipeline=data.get("pipeline", None),
            pipeline_run_id=data.get("pipeline_run_id", None),
            r_number=data.get("r_number", None),
            relfex_lab_number=data.get("relfex_lab_number", None),
            sample_name=data.get("sample_name", None),
            specimen_type=data.get("specimen_type", None),
            test_code=data.get("test_code", None),
            test_name=data.get("test_name", None),
            time_json_generated=data.get("time_json_generated", None),
            variant_count=data.get("variant_count", None),
        )

        if "caller_info" in data:
            if "DRAGEN" in data["caller_info"]:
                record.version = data["caller_info"]["DRAGEN"].get("version", None)
                record.variant_type = data["caller_info"]["DRAGEN"].get("variant_type", None)
                record.variant_subtype = data["caller_info"]["DRAGEN"].get("variant_subtype", None)

        return record
