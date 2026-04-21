import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create the directory if it doesn't exist
os.makedirs('project_assets/images', exist_ok=True)

# Professional Color Palette
COLORS = {
    'primary': '#2563eb',    # Blue
    'secondary': '#64748b',  # Slate
    'success': '#10b981',    # Emerald
    'warning': '#f59e0b',    # Amber
    'danger': '#ef4444',     # Red
    'background': '#ffffff',
    'text': '#1e293b',
    'box_fill': '#f8fafc',
    'box_edge': '#cbd5e1',
    'accent': '#8b5cf6'      # Purple
}

def setup_plot(title, figsize=(12, 7)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=COLORS['background'])
    ax.set_title(title, fontsize=16, fontweight='bold', color=COLORS['text'], pad=30)
    ax.axis('off')
    return fig, ax

def add_box(ax, x, y, width, height, text, color=COLORS['primary'], alpha=0.1):
    rect = patches.FancyBboxPatch(
        (x, y), width, height, 
        boxstyle="round,pad=0.02,rounding_size=0.05",
        facecolor=color, alpha=alpha, edgecolor=color, linewidth=2
    )
    ax.add_patch(rect)
    
    ax.text(
        x + width/2, y + height/2, text, 
        ha='center', va='center', fontsize=11, 
        fontweight='bold', color=COLORS['text'],
        linespacing=1.5
    )

def add_arrow(ax, start, end, label="", label_pos='top'):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle='-|>,head_width=0.4,head_length=0.7',
            color=COLORS['secondary'],
            lw=1.5,
            shrinkA=5,
            shrinkB=5
        )
    )
    if label:
        lx, ly = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        offset = 0.03 if label_pos == 'top' else -0.04
        ax.text(lx, ly + offset, label, fontsize=9, color=COLORS['secondary'], ha='center', fontweight='bold')

# --- Existing Visuals (Refined) ---

def generate_vram_graph():
    labels = ['Qwen-1.5B', 'Llama-3.2-3B', 'Qwen-7B (4-bit)']
    vram_usage = [3.5, 4.8, 5.0]
    usable_vram, total_vram = 4.8, 6.0
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS['background'])
    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    ax.axhline(y=total_vram, color=COLORS['danger'], linestyle='-', linewidth=2, label='Total VRAM (6GB)')
    ax.axhline(y=usable_vram, color=COLORS['warning'], linestyle='--', linewidth=2, label='Usable Budget (~4.8GB)')
    bars = ax.bar(labels, vram_usage, color=[COLORS['success'], COLORS['primary'], COLORS['danger']], alpha=0.7, zorder=3, width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{bar.get_height()}GB', ha='center', fontweight='bold')
    ax.set_ylabel('VRAM Usage (GB)', fontweight='bold', color=COLORS['secondary'])
    ax.set_title('Hardware Constraint: VRAM Consumption', fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon=False)
    plt.savefig('project_assets/images/vram_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_latency_graph():
    models = ['Qwen-1.5B', 'Llama-3.2-3B', 'Qwen-7B (4-bit)']
    latency = [1.0, 3.5, 7.5]
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=COLORS['background'])
    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    bars = ax.bar(models, latency, color=[COLORS['success'], COLORS['primary'], COLORS['danger']], alpha=0.7, zorder=3, width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f'{bar.get_height()}s', ha='center', fontweight='bold')
    ax.set_ylabel('Latency (Seconds)', fontweight='bold', color=COLORS['secondary'])
    ax.set_title('Inference Speed Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig('project_assets/images/latency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_arch_diagram():
    fig, ax = setup_plot("CareerPulse: System Architecture")
    bw, bh = 0.22, 0.12 
    add_box(ax, 0.05, 0.45, bw, bh, "Web Interface\n(Next.js 15+)", COLORS['primary'])
    add_box(ax, 0.38, 0.45, bw, bh, "Backend Core\n(FastAPI)", COLORS['warning'])
    add_box(ax, 0.72, 0.65, bw, bh, "Security Service\n(Adversarial Check)", COLORS['danger'])
    add_box(ax, 0.72, 0.25, bw, bh, "Intelligence Layer\n(RAG / Vector)", COLORS['success'])
    add_arrow(ax, (0.27, 0.51), (0.38, 0.51)) 
    add_arrow(ax, (0.6, 0.55), (0.72, 0.68))  
    add_arrow(ax, (0.6, 0.47), (0.72, 0.32))  
    plt.savefig('project_assets/images/system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_security_flow():
    fig, ax = setup_plot("Security Pipeline: Sequential Analysis", figsize=(9, 8))
    steps = [("PDF Ingestion", "pdfplumber Extraction"), ("Adversarial Scan", "Hidden Text Detection"), ("Privacy Filter", "spaCy PII Redaction"), ("Vectorization", "SBERT Embedding")]
    bw, bh, start_y = 0.6, 0.1, 0.8
    for i, (title, desc) in enumerate(steps):
        curr_y = start_y - (i * 0.18)
        add_box(ax, 0.2, curr_y, bw, bh, f"{title}\n{desc}", COLORS['secondary'], alpha=0.05)
        if i < len(steps) - 1:
            ax.annotate("", xy=(0.5, curr_y - 0.08), xytext=(0.5, curr_y - 0.01), arrowprops=dict(arrowstyle='-|> ,head_width=0.4', color=COLORS['secondary'], lw=2))
    plt.savefig('project_assets/images/security_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_rag_diagram():
    fig, ax = setup_plot("Retrieval-Augmented Generation (RAG) Workflow", figsize=(12, 6))
    bw, bh = 0.18, 0.15
    add_box(ax, 0.02, 0.4, bw, bh, "Resume\nEmbedding", COLORS['primary'])
    add_box(ax, 0.28, 0.4, bw, bh, "Vector DB\n(Qdrant)", COLORS['warning'])
    add_box(ax, 0.54, 0.4, bw, bh, "Context\nEnrichment", COLORS['success'])
    add_box(ax, 0.80, 0.4, bw, bh, "Local LLM\n(Qwen 1.5B)", COLORS['danger'])
    add_arrow(ax, (0.20, 0.475), (0.28, 0.475), "Search", 'top')
    add_arrow(ax, (0.46, 0.475), (0.54, 0.475), "Retrieve", 'top')
    add_arrow(ax, (0.72, 0.475), (0.80, 0.475), "Prompt", 'top')
    plt.savefig('project_assets/images/rag_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()

# --- NEW VISUALS ---

# 6. Keyword Fallacy vs Semantic Matching (Chapter 1.4)
def generate_semantic_v_keyword():
    fig, ax = setup_plot("The Semantic Gap: Keyword vs. Meaning", figsize=(12, 6))
    
    # Keyword approach (Left)
    ax.text(0.25, 0.8, "Traditional ATS (Keyword)", ha='center', fontsize=12, fontweight='bold', color=COLORS['danger'])
    add_box(ax, 0.1, 0.5, 0.3, 0.2, "Query: 'Data Scientist'\nMatch: 'Data Scientist'", COLORS['danger'], alpha=0.05)
    ax.text(0.25, 0.4, "X Fail: 'ML Engineer'\nX Fail: 'AI Expert'", ha='center', fontsize=10, color=COLORS['danger'])

    # Semantic approach (Right)
    ax.text(0.75, 0.8, "CareerPulse (Semantic)", ha='center', fontsize=12, fontweight='bold', color=COLORS['success'])
    add_box(ax, 0.6, 0.5, 0.3, 0.2, "Query: 'Data Scientist'\nMatch: Conceptual Cluster", COLORS['success'], alpha=0.05)
    ax.text(0.75, 0.4, "✓ Match: 'ML Engineer'\n✓ Match: 'AI Expert'", ha='center', fontsize=10, color=COLORS['success'])
    
    add_arrow(ax, (0.45, 0.6), (0.55, 0.6), "Better Accuracy")
    
    plt.savefig('project_assets/images/semantic_gap.png', dpi=300, bbox_inches='tight')
    plt.close()

# 7. Cosine Similarity in Vector Space (Chapter 2.2)
def generate_cosine_similarity():
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=COLORS['background'])
    ax.set_title("Cosine Similarity: Angular Distance in Vector Space", fontsize=14, fontweight='bold', pad=20)
    
    # Draw axes
    ax.arrow(0, 0, 0.9, 0, head_width=0.03, color=COLORS['secondary'], alpha=0.5)
    ax.arrow(0, 0, 0, 0.9, head_width=0.03, color=COLORS['secondary'], alpha=0.5)
    ax.text(0.95, 0, "Dim 1", ha='center')
    ax.text(0, 0.95, "Dim 2", ha='center')

    # Vectors
    ax.quiver([0, 0], [0, 0], [0.8, 0.7], [0.2, 0.4], color=[COLORS['primary'], COLORS['success']], angles='xy', scale_units='xy', scale=1, width=0.015)
    ax.text(0.8, 0.25, "Resume Vector", fontweight='bold', color=COLORS['primary'])
    ax.text(0.7, 0.45, "Job Vector", fontweight='bold', color=COLORS['success'])
    
    # Angle arc
    theta = np.linspace(np.arctan(0.2/0.8), np.arctan(0.4/0.7), 100)
    ax.plot(0.3 * np.cos(theta), 0.3 * np.sin(theta), color=COLORS['accent'], lw=2)
    ax.text(0.35, 0.15, r"$\theta$ (Similarity)", fontsize=12, color=COLORS['accent'], fontweight='bold')

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.axis('off')
    
    plt.savefig('project_assets/images/cosine_similarity.png', dpi=300, bbox_inches='tight')
    plt.close()

# 8. PII Redaction Example (Chapter 5.2)
def generate_pii_redaction():
    fig, ax = setup_plot("Privacy-First Processing: NER Redaction", figsize=(10, 6))
    
    # Original Text
    ax.text(0.25, 0.8, "Raw Resume Text", ha='center', fontsize=12, fontweight='bold', color=COLORS['secondary'])
    raw_text = "John Doe\nEmail: john.doe@email.com\nLocation: Patna, India\nSkills: Python, React"
    add_box(ax, 0.05, 0.4, 0.4, 0.3, raw_text, COLORS['secondary'], alpha=0.05)

    # Redacted Text
    ax.text(0.75, 0.8, "Sanitized AI Input", ha='center', fontsize=12, fontweight='bold', color=COLORS['success'])
    redacted_text = "[PERSON]\nEmail: [EMAIL]\nLocation: [GPE]\nSkills: Python, React"
    add_box(ax, 0.55, 0.4, 0.4, 0.3, redacted_text, COLORS['success'], alpha=0.05)
    
    add_arrow(ax, (0.47, 0.55), (0.53, 0.55), "spaCy NER")
    
    plt.savefig('project_assets/images/pii_redaction.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating comprehensive professional visuals...")
    generate_vram_graph()
    generate_latency_graph()
    generate_arch_diagram()
    generate_security_flow()
    generate_rag_diagram()
    generate_semantic_v_keyword()
    generate_cosine_similarity()
    generate_pii_redaction()
    print("All visuals saved to project_assets/images/")
