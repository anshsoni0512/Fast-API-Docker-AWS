import pickle


MODEL_VERSION = '1.0.0'   # this comes from MLFlow registry..

with open('Model/model.pkl','rb') as f:   # in f variable the model is stored.
    model = pickle.load(f)        # so now we are loading model.

class_lables = model.classes_.tolist()  # we will get three categories high,medium and low..

def predict(user_input):   # here user_input is a dataframe
    # ✅ Correct — convert to plain Python string


    prediction_of_category = str(model.predict(user_input)[0])
    probabilities = model.predict_proba(user_input)[0].tolist()
    confidence = max(probabilities)

    return {'prediction_of_category': prediction_of_category, 'class_probabilites':probabilities, 'confidence_score':confidence}

   
