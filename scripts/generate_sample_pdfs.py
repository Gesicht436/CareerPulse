from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

def create_pdf(md_file, pdf_file):
    print(f"Converting {md_file} to {pdf_file}...")
    
    # Read Markdown content
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found.")
        return

    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=12
    )
    
    sub_title_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=12,
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )

    header_style = styles['Heading2']
    normal_style = styles['Normal']

    story = []

    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
            
        # Very basic markdown parsing
        if line.startswith("# "):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith("**") and line.endswith("**") and "Engineer" in line: # Header/Subtitle detection
             story.append(Paragraph(line.replace("**", ""), sub_title_style))
        elif line.startswith("## "):
            story.append(Spacer(1, 12))
            story.append(Paragraph(line[3:], header_style))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], styles['Heading3']))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph("• " + line[2:], normal_style))
        else:
            story.append(Paragraph(line, normal_style))

    doc.build(story)
    print(f"Successfully created: {pdf_file}")

if __name__ == "__main__":
    os.makedirs("project_assets/sample_resumes", exist_ok=True)
    create_pdf("project_assets/sample_resumes/resume_elite_ai_engineer.md", "project_assets/sample_resumes/resume_elite_ai_engineer.pdf")
    create_pdf("project_assets/sample_resumes/resume_moderate_web_dev.md", "project_assets/sample_resumes/resume_moderate_web_dev.pdf")
