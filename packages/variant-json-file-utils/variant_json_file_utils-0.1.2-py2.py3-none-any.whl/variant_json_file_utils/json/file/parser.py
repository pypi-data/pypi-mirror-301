import json
import gzip
import bz2
import codecs

import logging
import os

from singleton_decorator import singleton
from typing import Any, Dict, List, Optional

from ... import constants
from ..annotated_match_call.record import Record as AnnotatedMatchCallRecord
from ..metadata.parser import Parser as MetadataParser
from ..metadata.record import Record as MetadataRecord


@singleton
class Parser:
    """Class for parsing variant JSON file."""

    def __init__(self, **kwargs):
        """Constructor for class Parser"""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.infile = kwargs.get("infile", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", constants.DEFAULT_OUTDIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self._is_parsed = False
        self._annotated_match_call_records = []

        logging.info(f"Instantiated Parser in {os.path.abspath(__file__)}")

    def get_metadata_record(self, infile: Optional[str]) -> MetadataRecord:
        """Get the metadata record."""
        if not self._is_parsed:
            self.get_annotated_match_call_records(infile)
        return self.metadata_record


    def get_annotated_match_call_records(self, infile: str) -> List[AnnotatedMatchCallRecord]:
        """Get records from the JSON file.

        Args:
            infile (str): The path to the JSON file.

        Returns:
            List[AnnotatedMatchCallRecord]: List of annotated match call record objects.
        """
        if self._is_parsed:
            return self._annotated_match_call_records

        data = self._parse_large_json(infile)

        if data is None:
            raise Exception(f"Error parsing JSON file '{infile}'")

        if "metadata" in data:
            parser = MetadataParser(
                config=self.config,
                config_file=self.config_file,
                infile=self.infile,
                logfile=self.logfile,
                outdir=self.outdir,
                verbose=self.verbose
            )
            self.metadata_record = parser.get_record(data["metadata"])
            # self.metadata_record = self._get_metadata_record(data["metadata"])

        logging.info("Will attempt to parse the variant_annotation_series section for ANNOTATED_MATCH_CALL records")

        if "variant_annotation_series" not in data:
            raise Exception("Did not find 'variant_annotation_series' in JSON data")

        ctr = 0

        for obj in data["variant_annotation_series"]:
            ctr += 1

            if "__type__" not in obj:
                raise Exception(f"Processing object '{ctr}' in variant_annotation_sries but did not find '__type__': {obj}")

            if obj["__type__"] == "HEADER":
                continue

            if obj["__type__"] == "ANNOTATED_MATCH_CALL":
                record = self._get_annotated_match_call_record(obj)
                self._annotated_match_call_records.append(AnnotatedMatchCallRecord(record))

        logging.info("Finished parsing the variant_annotation_series section for ANNOTATED_MATCH_CALL records")

        self._is_parsed = True

        return self._annotated_match_call_records

    def _get_annotated_match_call_record(self, data: Dict[str, Any]) -> AnnotatedMatchCallRecord:
        """Get the annotated match call record.

        Args:
            data (Dict[str, Any]): The data for the annotated match call record.

        Returns:
            AnnotatedMatchCallRecord: The annotated match call record object.
        """
        record = AnnotatedMatchCallRecord(
            batch_flowcell_id=data.get("batch_flowcell_id", None),
            batch_id=data.get("batch_id", None),
            batch_label=data.get("batch_label", None),
            case_id=data.get("case_id", None),
            chromosome=data.get("chromosome", None),
            end=data.get("end", None),
            gene=data.get("gene", None),
            gene_id=data.get("gene_id", None),
            hgvs_c=data.get("hgvs_c", None),
            hgvs_p=data.get("hgvs_p", None),
            lab_number=data.get("lab_number", None),
            midpool=data.get("midpool", None),
            pipeline_run_id=data.get("pipeline_run_id", None),
            r_number=data.get("r_number", None),
            ref=data.get("ref", None),
            refseq=data.get("refseq", None),
            start=data.get("start", None),
            variant_count=data.get("variant_count", None),
            variant_type=data.get("variant_type", None),
            variant_subtype=data.get("variant_subtype", None),
            variant_id=data.get("variant_id", None),
            variant_name=data.get("variant_name", None),
            variant_class=data.get("variant_class", None),
            variant_effect=data.get("variant_effect", None),
            variant_impact=data.get("variant_impact", None),
            variant_transcript=data.get("variant_transcript", None),
        )

        return record
    def _parse_large_json(self, infile: str) -> Dict[str, Any]:
        """Efficiently parses a large JSON file.

        Args:
            infile (str): The path to the JSON file.

        Returns:
            Dict[str, Any]: The parsed JSON data.
        """

        try:
            # Check for compressed file formats
            if infile.endswith(".gz"):
                with gzip.open(infile, "rt", encoding="utf-8") as f:
                    data = json.load(f)

            elif infile.endswith(".bz2"):
                with bz2.open(infile, "rt", encoding="utf-8") as f:
                    data = json.load(f)

            else:
                with codecs.open(infile, "r", encoding="utf-8") as f:
                    data = json.load(f)

            return data

        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            return None
