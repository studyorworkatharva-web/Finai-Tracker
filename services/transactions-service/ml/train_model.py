import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
import os

# Define file paths
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'sample-data', 'training_data.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')

def train_model():
    print(f"Loading training data from {DATA_PATH}...")
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Training data not found at {DATA_PATH}")
        print("Please ensure 'sample-data/training_data.csv' exists.")
        return

    print(f"Loaded {len(df)} training examples.")
    
    # Simple check for data quality
    if 'Description' not in df.columns or 'Category' not in df.columns:
        print("Error: CSV must have 'Description' and 'Category' columns.")
        return
        
    df.dropna(subset=['Description', 'Category'], inplace=True)
    
    X = df['Description']
    y = df['Category']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Create a pipeline
    # TfidfVectorizer: Converts text descriptions into numerical features.
    # LogisticRegression: A simple, fast, and effective classifier for this task.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
        ('clf', LogisticRegression(solver='liblinear', random_state=42, multi_class='auto')),
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save the trained pipeline
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(pipeline, MODEL_PATH)
    print("Model training complete and saved.")

if __name__ == "__main__":
    train_model()