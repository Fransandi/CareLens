import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Define paths
llm_responses_dir = Path("../data/llm_responses")
output_base_dir = Path("../data/distribution_analysis")
output_base_dir.mkdir(parents=True, exist_ok=True)

# Reuse color map
color_map = {
    "Yes": "royalblue",
    "No": "tomato",
    "I don't know": "gold",
    "Likely": "mediumorchid",
    "Unlikely": "mediumseagreen",
    "Neutral": "darkorange",
    "Minimal": "darkturquoise",
    "Moderate": "mediumvioletred",
    "High": "firebrick"
}

# Function to process a single patient file


def process_patient_file(file_path: Path):
    with open(file_path) as f:
        patient_data = json.load(f)

    patient_id = file_path.stem
    output_dir = output_base_dir / patient_id
    output_dir.mkdir(parents=True, exist_ok=True)

    for question in patient_data.get("questions", []):
        df = pd.DataFrame(question["answers"])

        fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

        def plot_grouped(ax, group_col):
            grouped = df.groupby([group_col, 'answer']
                                 ).size().unstack(fill_value=0)
            ordered_cols = [col for col in color_map.keys()
                            if col in grouped.columns]
            grouped = grouped.reindex(columns=ordered_cols)
            colors = [color_map[col] for col in grouped.columns]
            grouped.plot(kind='bar', ax=ax, color=colors)
            ax.set_title(f'Grouped by {group_col.capitalize()}')
            ax.set_xlabel(group_col.capitalize())
            ax.set_ylabel('Number of Answers')
            ax.legend(title='Answer')
            ax.tick_params(axis='x', rotation=45)

        plot_grouped(axes[0], 'gender')
        plot_grouped(axes[1], 'race')
        plot_grouped(axes[2], 'income')

        fig.suptitle(f"{question['id']}. {question['question']}",
                     fontsize=18, fontweight='bold', y=1.05)
        plt.tight_layout()

        output_path = output_dir / f"question_{question['id']}.png"
        plt.savefig(output_path, bbox_inches="tight", dpi=150)
        plt.close()


# Process all JSON files in the llm_responses directory
patient_files = list(llm_responses_dir.glob("*.json"))
for file in patient_files:
    process_patient_file(file)

# List output directories created
sorted([str(p) for p in output_base_dir.iterdir() if p.is_dir()])
