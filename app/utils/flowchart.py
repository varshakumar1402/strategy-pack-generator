import matplotlib.pyplot as plt

def generate_flowchart(planning_type):
    steps = {
        "PD": ["Idea", "Survey", "Drawings", "Submission", "Decision"],
        "Full Planning": ["Survey", "Drawings", "Consultation", "Submission", "Validation", "Decision"],
        "Householder": ["Drawings", "Submission", "Decision"],
        "Pre-App": ["Prep", "Submission", "Advice"],
        "Certificate of Lawfulness": ["Evidence", "Application", "Decision"]
    }

    flow = steps.get(planning_type, ["Start", "Middle", "End"])

    fig, ax = plt.subplots(figsize=(len(flow)*2, 2))
    for i, step in enumerate(flow):
        ax.text(i, 0, step, fontsize=12, ha='center', bbox=dict(facecolor='skyblue', boxstyle='circle'))
        if i < len(flow) - 1:
            ax.annotate('', xy=(i+0.85, 0), xytext=(i+0.15, 0),
                        arrowprops=dict(arrowstyle='->', lw=2))
    ax.axis('off')
    path = "/tmp/flowchart.png"
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    return path