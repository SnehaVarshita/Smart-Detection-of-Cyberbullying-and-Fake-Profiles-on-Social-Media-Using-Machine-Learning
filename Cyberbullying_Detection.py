import pickle

def Cyberbullying_Detection(text_input):
    # Load the saved models
    labelencoder = pickle.load(open('Files/CD_labelencoder.pkl', 'rb'))
    vectorizer = pickle.load(open('Files/CD_vectoriser.pkl', 'rb'))
    model = pickle.load(open('Files/CD_logreg.pkl', 'rb'))  # Use the Logistic Regression model here

    # List of possible classes (optional for reference)
    classes = [
        'not_cyberbullying',
        'gender_cyberbullying',
        'religion_cyberbullying',
        'other_cyberbullying',
        'age_cyberbullying',
        'ethnicity_cyberbullying'
    ]

    # Preprocess and transform the input
    text_input = [text_input]  # Wrap in list for vectorizer
    vectorized_input = vectorizer.transform(text_input)  # No .toarray() needed for sparse input

    # Make prediction
    prediction = model.predict(vectorized_input)

    # Decode label
    predicted_label = labelencoder.inverse_transform(prediction)[0]

    return predicted_label


# Example usage
if __name__ == "__main__":
    sample_input = "You people are disgusting and should not exist"
    result = Cyberbullying_Detection(sample_input)
    print("Predicted category:", result)
