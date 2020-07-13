
# pdf_parser_n_editor
A repository for taking in pdfs and executing the markers to detect pii markers and then redact them

This repository uses the base code of [JoshData/pdf-redactor](https://github.com/JoshData/pdf-redactor)

I read and understood the complete code of this pdf redaction and then changed it so as to suit our needs.
It uses our PII markers,identifies them in the pdf input,and then generates a new pdf with 'u' * (size of word) in place of the identfied PII markers, and in this way, we do not lose the formatting of the input pdf, as well as the other contents.

To use it, clone this repositoryand then install the requirements (by using pip install command) , that is, requirements_pdf_parser.txt and requirements_spotlight.txt .

In the main.py file,adjust the directory of the file you wish to parse,and the name of the file.
After this ,just run the following code -

`python main.py `

Although example.py contains a few regex expressions, they have got nothing to do, since i changed the code in the main file, that is, pdf-redactor.py. 
This is the first version, and hence a bit bulky with a lot of files and a lot of code. In due course of time, I'll reduce the number of files and and remove redundant code.

The code has the same limitations as the base repository.
