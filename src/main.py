#!/usr/bin/env python3
"""
Python script to load a saved pickle model and make predictions.
Designed to be called from Node.js child process.
Outputs JSON for easy parsing.
"""

import pickle
import pandas as pd
import json
import sys
from pathlib import Path


default_model_path = "src/model/core_model.pkl"


def load_model(model_path):
    """Load the saved pickle model."""
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        return model, None
    except FileNotFoundError:
        return None, f"File not found: {model_path}"
    except Exception as e:
        return None, f"Error loading model: {str(e)}"



def predict(model, area):
    """Make a prediction using the loaded model."""
    try:
        prediction = model.predict(pd.DataFrame({'area': [area]}))
        return float(prediction[0]), None
    except Exception as e:
        return None, f"Error making prediction: {str(e)}"



def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # Running as script, use the file's directory
        base_path = Path(__file__).parent

    return base_path / relative_path



def main():
    """Main function to handle command-line arguments and output JSON."""
    # Parse command-line arguments
    if len(sys.argv) < 2:
        output = {
            'success': False,
            'error': 'Missing required argument: area',
            'usage': './predict <area> [model_path]'
        }
        print(json.dumps(output))
        sys.exit(1)

    try:
        area = float(sys.argv[1])
    except ValueError:
        output = {
            'success': False,
            'error': f'Invalid area value: {sys.argv[1]}. Must be a number.'
        }
        
        print(json.dumps(output))
        sys.exit(1)

    # Determine model path - single step
    if len(sys.argv) > 2:
        model_path = sys.argv[2]  # Custom path provided
    else:
        # Try bundled model first (when compiled), then look relative to script
        try:
            model_path = get_resource_path(default_model_path)
            if not model_path.exists():
                # Fallback: look in model/ directory relative to project root
                script_dir = Path(__file__).parent
                project_root = script_dir.parent  # Go up from src/ to project root
                model_path = project_root / default_model_path
        except:
            # Fallback: look in model/ directory relative to script
            script_dir = Path(__file__).parent
            project_root = script_dir.parent
            model_path = project_root / default_model_path

    print("Loading model from path: ", model_path)

    # Load model
    model, error = load_model(str(model_path))
    if model is None:
        output = {
            'success': False,
            'error': error or f'Failed to load model from: {model_path}'
        }
        print(json.dumps(output))
        sys.exit(1)

    # Make prediction
    prediction, error = predict(model, area)
    if prediction is None:
        output = {
            'success': False,
            'error': error or 'Failed to make prediction'
        }
        print(json.dumps(output))
        sys.exit(1)

    # Output success result as JSON
    output = {
        'success': True,
        'area': area,
        'prediction': prediction,
        'model_coefficient': float(model.coef_[0]) if hasattr(model, 'coef_') else None,
        'model_intercept': float(model.intercept_) if hasattr(model, 'intercept_') else None
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    main()
