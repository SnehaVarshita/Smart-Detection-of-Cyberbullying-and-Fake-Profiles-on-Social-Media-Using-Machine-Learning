import pickle

def FakeProfile_Detection(prsence_of_profile_pic,ratio_of_number_len_username,name_username_matching,len_desc,presence_of_extern_url):

    # Load the model and vectorizer
    model = pickle.load(open('Files/FP_dt_model.pkl', 'rb'))
    LE_PP = pickle.load(open('Files/LEPP_model.pkl', 'rb'))
    LE_URL = pickle.load(open('Files/LEURL_model.pkl', 'rb'))
    LE_UN = pickle.load(open('Files/LEUN_model.pkl', 'rb'))
    classes = ['Fake', 'Real']
    
    prsence_of_profile_pic = LE_PP.transform([prsence_of_profile_pic])[0]
    presence_of_extern_url = LE_URL.transform([presence_of_extern_url])[0]
    name_username_matching = LE_UN.transform([name_username_matching])[0]
    
    # Create a feature vector from the input data
    input_data = [[prsence_of_profile_pic, ratio_of_number_len_username,
                   name_username_matching, len_desc, presence_of_extern_url]]

    # Make prediction
    prediction = model.predict(input_data)
    prediction = classes[prediction[0]]

    return prediction
if __name__ == "__main__":
    prsence_of_profile_pic = "Yes" ## 'Yes', 'No'
    ratio_number_len_of_username = 0.15
    name_username_matching = "Full match" ## 'No match', 'Partial match', 'Full match
    len_desc = 50
    presence_of_extern_url = "No" ## 'Yes', 'No'

    result = FakeProfile_Detection(prsence_of_profile_pic,ratio_number_len_of_username,name_username_matching,len_desc,presence_of_extern_url)
   
    print(result)

# Example usage
    ## input: prsence_of_profile_pic = "No" 
    ## input: ratio_number_len_of_username = 0.5
    ## input: name_username_matching = "Partial match" 
    ## input: len_desc = 50
    ## input: presence_of_extern_url = "No" 
    ## Output: Fake
# Example usage
    ## input: prsence_of_profile_pic = "Yes"
    ## input: ratio_number_len_of_username = 0.15
    ## input: name_username_matching = "Full match"
    ## input: len_desc = 50
    ## input: presence_of_extern_url = "No"
    ## Output: Real