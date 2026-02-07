"""
- Machine Learning With Python: 
- Build Core Model And Save And Load Trained Model
- use pandas to load the data
- use sklearn to train the model
- use pickle or joblib to save the model
"""


import pandas as pd
from sklearn import linear_model
import pickle
import joblib

model = None

pickle_model_path = "src/model/core_model.pkl"
joblib_model_path = "src/model/core_model.joblib"
csv_data_path = "src/model/home_prices_by_area.csv"


def get_trained_model():
    """Get the trained model or train it if it doesn't exist."""
    try:
        global model
        if model is not None:
            print("Model already trained")
            return model

        # Load data
        df = pd.read_csv(csv_data_path)
        print("Data head:")
        print(df.head())

        # Train model ( using linear regression, because we are predicting a continuous value )
        model = linear_model.LinearRegression()
        model.fit(df[['area']], df.price)

        # Display model parameters
        print("\nModel coefficient:", model.coef_)
        print("Model intercept:", model.intercept_)

        return model

    except Exception as e:
        print(f"Error training model: {e}")
        return None

# ============================================================================
# * Save Trained Model Using pickle
# ============================================================================

def save_model_using_pickle():
    """Save the trained model using pickle."""
    try:
        model = get_trained_model()
        with open(pickle_model_path, 'wb') as file:
            pickle.dump(model, file)
        print("\nModel saved using pickle")
    except Exception as e:
        print(f"Error saving model using pickle: {e}")


def load_model_using_pickle():
    """Load the trained model using pickle."""
    try:
        with open(pickle_model_path, 'rb') as file:
            model = pickle.load(file)
        print("\nModel loaded using pickle")
        return model

    except Exception as e:
        print(f"Error loading model using pickle: {e}")
        return None

# ============================================================================
# * Save Trained Model Using joblib
# ============================================================================

def save_model_using_joblib():
    """Save the trained model using joblib."""
    # Note: In newer versions of scikit-learn, use: import joblib
    # The old import from sklearn.externals is deprecated
    try:
        model = get_trained_model()
        joblib.dump(model, joblib_model_path)
        print("\nModel saved using joblib")

    except Exception as e:
        print(f"Error saving model using joblib: {e}")


def load_model_using_joblib():
    """Load the trained model using joblib."""
    try:
        model = joblib.load(joblib_model_path)
        print("\nModel loaded using joblib")

        return model

    except Exception as e:
        print(f"Error loading model using joblib: {e}")
        return None


def main():
    """Main function to build the core model and save it using pickle or joblib."""

    while True:
        # If no argument, prompt user
        print("🤖 Model Builder")
        print("💾 1) Save with pickle")
        print("💾 2) Save with joblib")
        print("🔍 3) Test prediction with pickle")
        print("🔍 4) Test prediction with joblib")
        print("🚪 5) Exit")
        choice = input("Enter your choice (1, 2, 3, or 4): ")
        if choice == '1':
            save_model_using_pickle()
        elif choice == '2':
            save_model_using_joblib()
        elif choice == '3':
            print("\nTesting prediction with pickle:")
            model = load_model_using_pickle()

            # Display loaded model parameters
            print("\nLoaded model coefficient:", model.coef_)
            print("Loaded model intercept:", model.intercept_)

            prediction = model.predict(pd.DataFrame({'area': [5000]}))
            print(f"Pickle model prediction for area 5000: {prediction}")

        elif choice == '4':
            print("\nTesting prediction with joblib:")
            model = load_model_using_joblib()

            # Display loaded model parameters
            print("\nLoaded model coefficient:", model.coef_)
            print("Loaded model intercept:", model.intercept_)

            prediction = model.predict(pd.DataFrame({'area': [5000]}))
            print(f"Joblib Prediction for area 5000: {prediction}")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice")
            continue


if __name__ == '__main__':
    main()
