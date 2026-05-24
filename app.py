from fastapi.middleware.cors import CORSMiddleware



from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
import pandas as pd
from Model.predict import MODEL_VERSION, predict, model


from schema.pydantic_model import Insurance   # you have to import the class as in predict endpoint we are using object of Insurance class.

app = FastAPI()



# ✅ Add this to backend app.py

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {'message':'This is the home page of Insurance Premium Prediction website.'}

@app.get('/health')   # this is for AWS Kubernets or elastic load balancer they will run this endpoint
def health():
    return {'status':'OK', 'model_version':MODEL_VERSION, 'model_loaded': model is not None}

@app.post('/predict')
def predict_insurance(person:Insurance):  # person is a object of Insurance class..

    # person variable has all fields like bmi, lifestye_risk, city_tier all that..
    
    input_data = pd.DataFrame([{
        'bmi':person.bmi,
        'age_group':person.age_group,
        'lifestyle_risk':person.lifestyle_risk,
        'city_tier':person.city_tier,
        'income_lpa':person.income_lpa,
        'occupation':person.occupation
    }])

    prediction = predict(input_data)   # this predict funciton is in predict.py file...
    
    return JSONResponse(status_code = 200, content={'predicted_category': prediction})


# Without [0]        → ['High']       (array)
# With [0]           → 'High'         (single value)


