import json
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Define paths
LLM_RESPONSES_DIR = Path("../data/llm_responses")
OUTPUT_BASE_DIR = Path("../data/distribution_analysis")
OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)

# Reuse color map
COLOR_MAP = {
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

# Initialize an empty DataFrame to store aggregated data
aggregated_data = pd.DataFrame()


def plot_grouped(ax, df, group_col):
    """Helper function to plot grouped bar charts."""
    grouped = df.groupby([group_col, 'answer']).size().unstack(fill_value=0)
    ordered_cols = [col for col in COLOR_MAP.keys() if col in grouped.columns]
    grouped = grouped.reindex(columns=ordered_cols)
    colors = [COLOR_MAP[col] for col in grouped.columns]
    grouped.plot(kind='bar', ax=ax, color=colors)
    ax.set_title(f'Grouped by {group_col.capitalize()}')
    ax.set_xlabel(group_col.capitalize())
    ax.set_ylabel('Number of Answers')
    ax.legend(title='Answer')
    ax.tick_params(axis='x', rotation=45)


def generate_patient_charts(patient_id, question, df, output_dir):
    """Generate charts for individual patient questions."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

    # Plot grouped data
    plot_grouped(axes[0], df, 'gender')
    plot_grouped(axes[1], df, 'race')
    plot_grouped(axes[2], df, 'income')

    # Add titles and footer
    fig.suptitle(f"{question['id']}. {question['question']}",
                 fontsize=18, fontweight='bold', y=1.05)
    fig.text(0.5, -0.02, patient_id, ha='center', fontsize=16, color='black')

    # Save the figure
    output_path = output_dir / f"question_{question['id']}.png"
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close()


def process_patient_file(file_path):
    """Process a single patient file and generate charts."""
    global aggregated_data

    with open(file_path) as f:
        patient_data = json.load(f)

    patient_id = file_path.stem
    output_dir = OUTPUT_BASE_DIR / patient_id
    output_dir.mkdir(parents=True, exist_ok=True)

    for question in patient_data.get("questions", []):
        df = pd.DataFrame(question["answers"])

        # Add data to the aggregated DataFrame
        df["question_id"] = question["id"]
        df["question_text"] = question["question"]
        aggregated_data = pd.concat([aggregated_data, df], ignore_index=True)

        # Generate individual patient charts
        generate_patient_charts(patient_id, question, df, output_dir)


def generate_aggregated_charts():
    """Generate aggregated charts for all patients."""
    if aggregated_data.empty:
        return

    aggregated_output_dir = OUTPUT_BASE_DIR / "aggregated"
    aggregated_output_dir.mkdir(parents=True, exist_ok=True)

    for question_id, question_group in aggregated_data.groupby("question_id"):
        fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

        # Plot grouped data
        plot_grouped(axes[0], question_group, 'gender')
        plot_grouped(axes[1], question_group, 'race')
        plot_grouped(axes[2], question_group, 'income')

        # Add titles and footer
        question_text = question_group["question_text"].iloc[0]
        fig.suptitle(f"{question_id}. {question_text}",
                     fontsize=18, fontweight='bold', y=1.05)
        fig.text(0.5, -0.02, "Data aggregated from all patients",
                 ha='center', fontsize=16, color='black')

        # Save the figure
        output_path = aggregated_output_dir / \
            f"question_{question_id}_aggregated.png"
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches="tight", dpi=150)
        plt.close()


def main():
    """Main function to process patient files and generate charts."""
    # Process all JSON files in the LLM responses directory
    patient_files = list(LLM_RESPONSES_DIR.glob("*.json"))
    for file in patient_files:
        process_patient_file(file)

    # Generate aggregated charts
    generate_aggregated_charts()

    # List output directories created
    output_dirs = sorted([str(p)
                         for p in OUTPUT_BASE_DIR.iterdir() if p.is_dir()])
    print("Output directories created:", output_dirs)


if __name__ == "__main__":
    main()
