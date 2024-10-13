# Bangla PDF OCR

Bangla PDF OCR is a powerful tool that extracts Bengali text from PDF files. It's designed for simplicity and works on Windows, macOS, and Linux without any extra downloads or configurations.

## Key Features

- Extracts Bengali text from PDFs quickly and accurately
- Works on Windows, macOS, and Linux
- Easy to use from both command line and Python scripts
- Installs all necessary components automatically
- Supports other languages besides Bengali

## Quick Start

1. Install the package:
   ```bash
   pip install bangla-pdf-ocr
   ```

2. Run the setup command to install dependencies:
   ```bash
   bangla-pdf-ocr-setup
   ```

3. Start using it right away!

   From command line:
   ```bash
   bangla-pdf-ocr your_file.pdf
   ```

   In your Python script:
   ```python
   from bangla_pdf_ocr import process_pdf
   text = process_pdf("your_file.pdf")
   print(text)
   ```

That's it! No additional downloads or configurations needed.

## Features

- Extract Bengali text from PDF files
- Support for other languages through Tesseract OCR
- Easy-to-use command-line interface
- Automatic installation of dependencies (OS-specific)
- Multi-threaded processing for improved performance

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Install the package from PyPI:
   ```bash
   pip install bangla-pdf-ocr
   ```

2. Set up system dependencies:
   ```bash
   bangla-pdf-ocr-setup
   ```
   This command installs necessary dependencies based on your operating system:
   - Linux: Installs `tesseract-ocr`, `poppler-utils`, and `tesseract-ocr-ben`
   - macOS: Installs `tesseract`, `poppler`, and `tesseract-lang` via Homebrew
   - Windows: Downloads and installs Tesseract OCR and Poppler, adding them to the system PATH

   Note: On Windows, you may need to run the command prompt as administrator.

3. Verify the installation:
   ```bash
   bangla-pdf-ocr-verify
   ```
   This command checks if all required dependencies are properly installed and accessible.

4. Try a sample PDF extraction:
   ```bash
   bangla-pdf-ocr
   ```
   This command processes a sample Bengali PDF file included with the package, demonstrating the text extraction capabilities.
   
## Usage

### Command-line Interface

Basic usage:
```bash
bangla-pdf-ocr [input_pdf] [-o output_file] [-l language]
```

### Options:
- `input_pdf`: Path to the input PDF file (optional, uses a sample PDF if not provided)
- `-o, --output`: Specify the output file path (default: input filename with `.txt` extension)
- `-l, --language`: Specify the OCR language (default: 'ben' for Bengali)

### Examples:

1. Process the default sample PDF:
   ```bash
   bangla-pdf-ocr
   ```

2. Process a specific PDF:
   ```bash
   bangla-pdf-ocr path/to/my_document.pdf
   ```

3. Specify an output file:
   ```bash
   bangla-pdf-ocr path/to/my_document.pdf -o path/to/extracted_text.txt
   ```


### Using as a Python Module

You can also use Bangla PDF OCR as a module in your Python scripts. Here's an example:

```python
from bangla_pdf_ocr import process_pdf

# Process a PDF file
input_pdf = "path/to/your/document.pdf"
output_file = "path/to/output/extracted_text.txt"
language = "ben"  # Use "ben" for Bengali or other language codes as needed

extracted_text = process_pdf(input_pdf, output_file, language)

# The extracted text is now in the 'extracted_text' variable
# and has also been saved to the output file

print(f"Text extracted and saved to: {output_file}")
```

This allows you to integrate Bangla PDF OCR functionality directly into your Python projects, giving you more control over the OCR process and enabling you to use the extracted text in your applications.

## Troubleshooting

If you encounter any issues:

1. Run the verification command:
   ```bash
   bangla-pdf-ocr-verify
   ```

2. For Windows users:
   - Run `setup/verify` command prompts as administrator if you encounter permission issues.
   - Restart your command prompt or IDE after installation to ensure PATH changes take effect.

3. Check the console output and logs for any error messages.

4. If automatic installation fails, refer to the manual installation instructions provided by the setup command.

5. Ensure you have the latest version of the package:
   ```bash
   pip install --upgrade bangla-pdf-ocr
   ```

6. If problems persist, please open an issue on our GitHub repository with detailed information about the error and your system configuration.


## Reporting Issues

If you encounter any problems or have suggestions for Bangla PDF OCR:

1. Check [existing issues](https://github.com/asiff00/bangla-pdf-ocr/issues) to see if your issue has already been reported.
2. If not, [create a new issue](https://github.com/asiff00/bangla-pdf-ocr/issues/new) on our GitHub repository.
3. Provide detailed information about the problem, including steps to reproduce it.

We appreciate your feedback to help improve Bangla PDF OCR!

Happy OCR processing!
