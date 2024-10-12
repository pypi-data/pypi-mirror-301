import argparse
import json
import os
import bson
from pathlib import Path

def read_json(file_path):
    """
    Read a JSON file and return the data.
    
    Args:
    file_path (str): Path to the JSON file.
    
    Returns:
    dict: The JSON data loaded into a Python dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_plot_metrics_as_json(overall_metrics, output_dir):
    """Saves each plot's metrics as individual JSON files."""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Iterate over the overall metrics and save each as a separate JSON
    for plot_name, metrics in overall_metrics.items():
        output_file = os.path.join(output_dir, f"{plot_name}.json")
        try:
            with open(output_file, 'w') as f:
                json.dump(metrics, f, indent=4)
        except Exception as e:
            print(f"Could not save metrics for {plot_name} because: {e}")
            
            
def format_metrics(metrics):
    """ Format and print the metrics in a readable way """
    print("\nOverall Highlighted Metrics:\n" + "-"*40)
    for metric, values in metrics['plot_highlighted_overall_metrics']['data'].items():
        print(f"{metric}:")
        for key, value in values.items():
            if isinstance(value, list):  # If it's a confidence interval
                value_str = f"{value[0]:.4f} to {value[1]:.4f}"
            else:
                value_str = f"{value:.4f}"
            print(f"    {key}: {value_str}")
        print("-"*40)
    print("All Graphs and Plots Metrics saved in JSONs.\n" + "-"*40)
