#;encoding=utf-8
# Example file to redact Social Security Numbers from the
# text layer of a PDF and to demonstrate metadata filtering.

import re
from datetime import datetime

import pdf_redactor

## Set options.

options = pdf_redactor.RedactorOptions()

# options.metadata_filters = {
# 	# Perform some field filtering --- turn the Title into uppercase.
# 	"Title": [lambda value : value.upper()],

# 	# Set some values, overriding any value present in the PDF.
# 	"Producer": [lambda value : "My Name"],
# 	"CreationDate": [lambda value : datetime.utcnow()],

# 	# Clear all other fields.
# 	"DEFAULT": [lambda value : None],
# }

# Clear any XMP metadata, if present.
options.xmp_filters = [lambda xml : None]
options.content_filters = [
	(
		re.compile(r"comment!"),
		lambda m : "annotation?"
	),
]

pdf_redactor.redactor(options)
