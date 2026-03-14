import pypandoc
import os

# 1. Download the pandoc binary if it's not present
print("Downloading pandoc binary (this might take a few moments)...")
pypandoc.download_pandoc()

# 2. Paths
md_file = "project_assets/Capstone_Report_CareerPulse.md"
docx_file = "project_assets/Capstone_Report_CareerPulse.docx"

# 3. Convert
print(f"Converting {md_file} to {docx_file}...")
pypandoc.convert_file(md_file, 'docx', outputfile=docx_file)

if os.path.exists(docx_file):
    print(f"Success! Your report is now available at: {os.path.abspath(docx_file)}")
else:
    print("Error: Conversion failed.")
