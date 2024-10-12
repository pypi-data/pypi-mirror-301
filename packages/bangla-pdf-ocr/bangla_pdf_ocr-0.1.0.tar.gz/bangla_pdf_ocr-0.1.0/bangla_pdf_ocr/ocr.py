import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import argparse
from tqdm import tqdm
from colorama import init, Fore, Style
import platform
import pkgutil

init(autoreset=True)

TESSERACT_PATH: Optional[str] = os.environ.get("TESSERACT_PATH")
POPPLER_PATH: Optional[str] = os.environ.get("POPPLER_PATH")
DEFAULT_LANGUAGE: str = os.environ.get("OCR_LANGUAGE", "ben")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger: logging.Logger = logging.getLogger(__name__)


def type_text(text: str, color: str = Fore.WHITE) -> None:
    print(color + text + Style.RESET_ALL)


class OCRProcessor:
    def __init__(self, language: str = DEFAULT_LANGUAGE) -> None:
        self.language: str = language
        self.tesseract_path: str = TESSERACT_PATH or self.find_tesseract()
        self.poppler_path: str = POPPLER_PATH or self.find_poppler()
        type_text(f"Tesseract path: {self.tesseract_path}", Fore.CYAN)
        type_text(f"Poppler path: {self.poppler_path}", Fore.CYAN)

    @staticmethod
    def find_program(program: str) -> Optional[str]:
        logger.info(f"Searching for {program}")
        if sys.platform.startswith("win"):
            program += ".exe"

        for path in os.environ["PATH"].split(os.pathsep):
            exe_file: Path = Path(path) / program
            if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                logger.info(f"Found {program} in PATH: {exe_file}")
                return str(exe_file)

        common_dirs: List[Path] = [
            Path(os.environ.get("ProgramFiles", "C:/Program Files")),
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")),
            Path(os.environ.get("USERPROFILE", "~")) / "Downloads",
            Path("/usr/bin"),
            Path("/usr/local/bin"),
            Path("/opt"),
            Path.home() / "Downloads",
        ]

        for directory in common_dirs:
            for exe_file in directory.rglob(program):
                if exe_file.is_file() and os.access(str(exe_file), os.X_OK):
                    logger.info(f"Found {program} in common directory: {exe_file}")
                    return str(exe_file)

        logger.warning(f"{program} not found")
        return None

    def find_tesseract(self) -> str:
        tesseract: Optional[str] = self.find_program("tesseract")
        if not tesseract:
            raise EnvironmentError(
                "Tesseract not found. Please install it and make sure it's in your PATH."
            )
        return tesseract

    def find_poppler(self) -> str:
        pdftoppm: Optional[str] = self.find_program("pdftoppm")
        if not pdftoppm:
            raise EnvironmentError(
                "Poppler (pdftoppm) not found. Please install it and make sure it's in your PATH."
            )
        return str(Path(pdftoppm).parent)

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Path]:
        image_prefix: str = f"temp_image_{os.getpid()}"
        pdftoppm_path: str = os.path.join(self.poppler_path, "pdftoppm")
        logger.info(f"Converting PDF to images using {pdftoppm_path}")
        try:
            subprocess.run(
                [pdftoppm_path, "-png", str(pdf_path), image_prefix],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting PDF to images: {e}")
            logger.error(f"pdftoppm stderr: {e.stderr}")
            raise
        return sorted(Path().glob(f"{image_prefix}-*.png"))

    def process_image(self, image_file: Path, page_num: int) -> str:
        try:
            logger.info(f"Processing page {page_num}")
            result: subprocess.CompletedProcess = subprocess.run(
                [self.tesseract_path, str(image_file), "stdout", "-l", self.language],
                capture_output=True,
                check=True,
                encoding="utf-8",
            )
            text: str = result.stdout
            os.remove(image_file)
            return f"\n--- Page {page_num} ---\n{text}"
        except subprocess.CalledProcessError as e:
            logger.error(f"Error processing page {page_num}: {e}")
            logger.error(f"Tesseract stderr: {e.stderr}")
            return f"\n--- Page {page_num} ---\nError: {e}\n"

    def extract_text_from_pdf(
        self, pdf_path: str, output_file: Optional[str] = None
    ) -> str:
        pdf_path_obj: Path = Path(pdf_path)
        output_file_obj: Path = (
            Path(output_file) if output_file else pdf_path_obj.with_suffix(".txt")
        )

        logger.info(f"Extracting text from {pdf_path_obj}")
        images: List[Path] = self.convert_pdf_to_images(pdf_path_obj)
        full_book: List[str] = [""] * len(images)

        with ThreadPoolExecutor() as executor:
            futures: Dict[Future[str], int] = {
                executor.submit(self.process_image, img, i): i
                for i, img in enumerate(images, start=1)
            }
            for future in tqdm(
                as_completed(futures), total=len(futures), desc="Processing pages"
            ):
                page_num: int = futures[future]
                try:
                    page_text: str = future.result()
                    full_book[page_num - 1] = page_text
                except Exception as exc:
                    logger.error(
                        f"Page {page_num} processing generated an exception: {exc}"
                    )
                    full_book[page_num - 1] = (
                        f"\n--- Page {page_num} ---\nError: {exc}\n"
                    )

        full_text: str = "".join(full_book)

        with open(output_file_obj, "w", encoding="utf-8") as file:
            file.write(full_text)

        logger.info(f"Text extracted and saved to {output_file_obj}")
        return full_text


def process_pdf(
    pdf_path: str, output_file: Optional[str] = None, language: str = "ben"
) -> str:
    processor: OCRProcessor = OCRProcessor(language)
    type_text("Starting PDF processing...", Fore.GREEN)
    extracted_text: str = processor.extract_text_from_pdf(pdf_path, output_file)
    type_text(
        f"Extraction completed successfully. Processed file: {pdf_path}",
        Fore.GREEN,
    )
    return extracted_text


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Extract text from PDF using OCR"
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=None,
        help="Path to the input PDF file",
    )
    parser.add_argument(
        "-o", "--output", help="Path to save the extracted text", default=None
    )
    parser.add_argument(
        "-l", "--language", default="ben", help="Language for OCR (default: ben)"
    )

    args: argparse.Namespace
    args, _ = parser.parse_known_args()

    if not args.pdf_path:
        try:
            default_pdf = pkgutil.get_data(__package__, "data/Freedom Fight.pdf")
            if default_pdf is None:
                raise FileNotFoundError(
                    "Default PDF 'Freedom Fight.pdf' not found in package data."
                )
            temp_pdf_path = Path(__file__).parent / "Freedom Fight.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(default_pdf)
            args.pdf_path = str(temp_pdf_path)
            type_text("Using default PDF: Freedom Fight.pdf", Fore.CYAN)
        except Exception as e:
            logger.error(f"Failed to load default PDF: {e}")
            type_text(
                "Default PDF 'Freedom Fight.pdf' not found. Please provide a PDF file.",
                Fore.RED,
            )
            sys.exit(1)

    try:
        type_text("Bangla PDF OCR", Fore.YELLOW)
        type_text("----------------", Fore.YELLOW)
        extracted_text: str = process_pdf(args.pdf_path, args.output, args.language)
        type_text(
            f"Extraction completed successfully. Processed file: {args.pdf_path}",
            Fore.GREEN,
        )
    except Exception as e:
        logger.error(f"An error occurred during extraction: {e}")
        type_text("An error occurred. Please check the log for details.", Fore.RED)


def setup_dependencies():
    system = platform.system().lower()
    scripts_dir = os.path.join(os.path.dirname(__file__), "scripts")

    print(Fore.YELLOW + Style.BRIGHT + "\nSystem Information:")
    print(
        Fore.WHITE
        + f"OS: {platform.system()} {platform.release()} {platform.version()}"
    )
    print(Fore.WHITE + f"Python: {platform.python_version()}")
    print(Fore.WHITE + f"Architecture: {platform.machine()}")

    print(Fore.YELLOW + Style.BRIGHT + "\nInstalling system dependencies:")

    if system.startswith("linux"):
        install_linux_dependencies(scripts_dir)
    elif system.startswith("darwin"):
        install_macos_dependencies(scripts_dir)
    elif system.startswith("win"):
        show_windows_instructions()
    else:
        print(
            Fore.YELLOW
            + f"Automatic dependency installation not supported for {system}."
        )

    print(Fore.YELLOW + "\nPlease ensure all required dependencies are installed.")
    print(
        Fore.WHITE
        + "For detailed instructions, visit: "
        + Fore.GREEN
        + "https://github.com/asiff00/bangla-pdf-ocr"
    )


def install_linux_dependencies(scripts_dir):
    script_path = os.path.join(scripts_dir, "install_linux_dependencies.sh")
    if os.path.exists(script_path):
        print(Fore.CYAN + "Installing dependencies for Linux...")
        try:
            subprocess.run(["bash", script_path], check=True)
            print(Fore.GREEN + "Linux dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error installing Linux dependencies: {e}")
    else:
        print(
            Fore.RED
            + f"Linux dependency installation script not found at {script_path}"
        )


def install_macos_dependencies(scripts_dir):
    script_path = os.path.join(scripts_dir, "install_macos_dependencies.sh")
    if os.path.exists(script_path):
        print(Fore.CYAN + "Installing dependencies for macOS...")
        try:
            subprocess.run(["bash", script_path], check=True)
            print(Fore.GREEN + "macOS dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Error installing macOS dependencies: {e}")
    else:
        print(
            Fore.RED
            + f"macOS dependency installation script not found at {script_path}"
        )


def show_windows_instructions():
    print(Fore.CYAN + "For Windows users:")
    print(
        Fore.WHITE
        + "1. Download and install Tesseract: "
        + Fore.GREEN
        + "https://github.com/UB-Mannheim/tesseract/wiki"
    )
    print(
        Fore.WHITE
        + "2. Download and install Poppler: "
        + Fore.GREEN
        + "https://github.com/oschwartz10612/poppler-windows/releases"
    )
    print(
        Fore.WHITE
        + "3. Add the bin directories of both Tesseract and Poppler to your system PATH."
    )
    print(Fore.WHITE + "4. Download Bengali language data file (ben.traineddata) from:")
    print(
        Fore.GREEN
        + "   https://github.com/tesseract-ocr/tessdata/blob/main/ben.traineddata"
    )
    print(Fore.WHITE + "   and place it in the Tesseract 'tessdata' directory.")
    print(
        Fore.YELLOW
        + "5. Restart your command prompt or IDE after making these changes."
    )


if __name__ == "__main__":
    main()