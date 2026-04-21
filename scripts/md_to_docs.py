import pypandoc
import os
import sys
import argparse
from pathlib import Path

def convert_markdown_to_docx(input_path: str, output_path: str = None):
    """
    Converts a single Markdown file or a directory of Markdown files to DOCX.
    """
    input_p = Path(input_path)

    if not input_p.exists():
        print(f"ERROR: Path '{input_path}' does not exist.")
        return

    # Handle Directory
    if input_p.is_dir():
        print(f"Scanning directory: {input_p}")
        md_files = list(input_p.glob("*.md"))
        if not md_files:
            print("No Markdown files found in directory.")
            return
        
        for md_file in md_files:
            target_docx = md_file.with_suffix(".docx")
            _perform_conversion(md_file, target_docx)
            
    # Handle Single File
    else:
        if input_p.suffix.lower() != ".md":
            print(f"WARNING: '{input_p.name}' does not have a .md extension. Proceeding anyway...")
        
        target_docx = Path(output_path) if output_path else input_p.with_suffix(".docx")
        _perform_conversion(input_p, target_docx)

def _perform_conversion(src: Path, dest: Path):
    """
    Internal helper to call pypandoc with professional arguments.
    """
    try:
        print(f"Converting: {src.name} -> {dest.name}...")
        
        # Professional Arguments:
        # --standalone: Creates a full document with headers/metadata
        # --resource-path: Tells Pandoc where to look for images (relative to the input file)
        # --from markdown+raw_attribute: Ensures {=openxml} blocks are parsed correctly
        resource_path = str(src.parent)
        
        extra_args = [
            '--standalone',
            '--wrap=none',
            f'--resource-path=.;{resource_path}',
            '--from=markdown+raw_attribute+backtick_code_blocks'
        ]

        # Use pypandoc to perform the conversion
        pypandoc.convert_file(
            str(src), 
            'docx', 
            format='markdown+raw_attribute', # Explicitly enable raw OpenXML
            outputfile=str(dest),
            extra_args=extra_args
        )
        print(f"SUCCESS: Created {dest}")
        
    except RuntimeError as e:
        print(f"PANDOC ERROR: Ensure Pandoc is installed (winget install JohnMacFarlane.Pandoc).")
        print(f"Details: {e}")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="General Purpose Markdown to DOCX Converter for CareerPulse")
    parser.add_argument("input", help="Path to a .md file or a directory containing .md files")
    parser.add_argument("-o", "--output", help="Optional: specific output path (only for single file conversion)", default=None)

    args = parser.parse_args()
    convert_markdown_to_docx(args.input, args.output)
