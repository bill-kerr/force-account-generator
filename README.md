# Force Account Generator

Tired of filling out PDF forms? The Force Account Generator is a Python program that processes an Excel template and produces a valid PennDOT force account PDF package.

The Force Account Generator was born out of a desire to quickly fill in proprietary PDF forms with Excel data. As it stands, the PennDOT force account package PDF is cumbersome, requires duplicate efforts, and is inadequate for large datasets. Furthermore, filling in individual form fields on a PDF is tiresome and prone to error. The Force Account Generator fixes all of that. It allows users to easily enter their data into Excel and generate a valid PDF form for submission. It saves time and reduces human error.

## :bookmark_tabs: How to use it

Visit [the application's website](http://example.com). Then, download the Excel template. The template should be familiar to anyone who has created a PennDOT force account before. Simply fill in the required information on each tab and save the file on your computer. Go back to the generator, click the checkbox if you'd like to generate daily sign-off sheets, and drop your Excel file in the file dropzone on the main page. We will do the rest of the work!

## :hammer: How it's built

The generator originated as a Python script with a [Tkinter](https://docs.python.org/3/library/tkinter.html) interface, but evolved to the [Django](https://www.djangoproject.com/)-based application you see today. The Django backend utilizes a pool of [Celery](https://docs.celeryproject.org/en/stable/) workers to asynchronously process the Excel workbook and build the PDF file. The status of the process is continuously queried by the frontend via an API endpoint to allow realtime updates.

The Excel file is read into a large data structure using the [openpyxl](https://openpyxl.readthedocs.io/en/stable/) library. This large data structure is then handed off to the PDF generator portion of the program, which performs intermediary calculations, formats the output, and paginates the data to fit the structure of the PennDOT force account forms. Blank template PDF form pages are then populated with the appropriate data using the [PyPDF2](https://pythonhosted.org/PyPDF2/) library. The pages are merged and the PDF is saved to disk and served to the user. All static, user-uploaded, and generated files are remotely stored in an AWS S3 bucket.

The frontend uses a combination of the Django templating engine for initial rendering and routing along with [AlpineJS](https://github.com/alpinejs/alpine) and [DropzoneJS](https://www.dropzonejs.com/) for the reactive components of the design.
