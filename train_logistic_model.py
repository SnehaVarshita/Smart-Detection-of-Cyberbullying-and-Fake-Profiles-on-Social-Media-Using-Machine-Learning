import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os

# Load Kaggle dataset
df = pd.read_csv('Files/cyberbullying_tweets.csv')  # Replace with your actual file path

# Drop missing
df.dropna(subset=['tweet_text', 'cyberbullying_type'], inplace=True)

# Rename labels to match your app's categories
label_mapping = {
    'gender': 'gender_cyberbullying',
    'religion': 'religion_cyberbullying',
    'ethnicity': 'ethnicity_cyberbullying',
    'age': 'age_cyberbullying',
    'other_cyberbullying': 'other_cyberbullying',  # Already same
    'not_cyberbullying': 'not_cyberbullying'
}

df['label'] = df['cyberbullying_type'].map(label_mapping)
df = df[df['label'].notnull()]  # Filter out unknowns

# Encode labels
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(df['label'])

# Vectorize text
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(df['tweet_text'])

# Train/test split and model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train, y_train)

# Save everything
os.makedirs('Files', exist_ok=True)

with open('Files/CD_logreg.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('Files/CD_vectoriser.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

with open('Files/CD_labelencoder.pkl', 'wb') as f:
    pickle.dump(labelencoder, f)

print("Model trained and all files saved successfully.")
