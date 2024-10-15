"""Top-level package for Variant JSON File Utils."""

__author__ = """Jaideep Sundaram"""
__email__ = 'sundaram.baylorgenetics@gmail.com'
__version__ = '0.1.0'

from .json.file.parser import Parser as VariantJSONFileParser
from .json.annotated_match_call.record import Record as AnnotatedMatchCallRecord
from .json.metadata.record import Record as MetadataRecord
