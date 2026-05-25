# 🏥 Insurance Premium Prediction API

A production-ready **Machine Learning REST API** built with **FastAPI** that predicts insurance premium categories based on personal and lifestyle information. Deployed using **Docker** on **AWS EC2**.

---

## 📌 What does this project do?

This API takes a person's basic details as input and predicts which **insurance premium category** they fall into:

| Category      | Meaning                  |
| ------------- | ------------------------ |
| 🔴 **High**   | High insurance premium   |
| 🟡 **Medium** | Medium insurance premium |
| 🟢 **Low**    | Low insurance premium    |

The ML model also returns:

- **Confidence Score** — how confident the model is
- **Class Probabilities** — probability for each category

---

## 🧠 How it Works

```
User sends details (age, weight, height, city, income, etc.)
                    ↓
API auto-computes derived features:
  ├── BMI            = weight / height²
  ├── Age Group      = young / adult / middle_aged / senior
  ├── Lifestyle Risk = High / Medium / Low (based on BMI + smoker)
  └── City Tier      = 1 / 2 / 3 (based on Indian city classification)
                    ↓
ML Model (scikit-learn) predicts premium category
                    ↓
Returns: prediction + probabilities + confidence score
```

---

## 🗂️ Project Structure

```
Insurance Premium Prediction/
│
├── app.py                        # FastAPI main application
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
│
├── Model/
│   ├── predict.py                # ML model loading & prediction logic
│   └── model.pkl                 # Trained scikit-learn model
│
├── schema/
│   ├── pydantic_model.py         # Input validation schema (Insurance class)
│   └── prediction_response.py    # Output response schema
│
└── config/
    └── cities.py                 # Tier 1 & Tier 2 Indian cities list
```

---

## 🚀 API Endpoints

### `GET /`

Home page of the API.

**Response:**

```json
{
  "message": "This is the home page of Insurance Premium Prediction website."
}
```

---

### `GET /health`

Health check endpoint (used by AWS Load Balancer / Kubernetes).

**Response:**

```json
{
  "status": "OK",
  "model_version": "1.0.0",
  "model_loaded": true
}
```

---

### `POST /predict`

Main prediction endpoint.

**Request Body:**

```json
{
  "age": 35,
  "weight": 75.0,
  "height": 1.75,
  "income_lpa": 12.5,
  "smoker": "False",
  "city": "Mumbai",
  "occupation": "Engineer"
}
```

**Response:**

```json
{
  "predicted_category": "Medium",
  "class_probabilities": [0.1, 0.7, 0.2],
  "confidence_score": 0.7
}
```

---

## 📥 Input Fields Explained

| Field        | Type   | Description                      |
| ------------ | ------ | -------------------------------- |
| `age`        | int    | Age of the person                |
| `weight`     | float  | Weight in kg (must be > 0)       |
| `height`     | float  | Height in meters (must be > 0)   |
| `income_lpa` | float  | Annual income in Lakhs per annum |
| `smoker`     | string | `"True"` or `"False"`            |
| `city`       | string | City of residence (max 30 chars) |
| `occupation` | string | Occupation (max 30 chars)        |

### Auto-computed Fields (no need to send these):

| Field            | How it's computed                    |
| ---------------- | ------------------------------------ |
| `bmi`            | `weight / height²`                   |
| `age_group`      | young / adult / middle_aged / senior |
| `lifestyle_risk` | Based on smoker status + BMI         |
| `city_tier`      | 1 (Metro) / 2 (Tier-2) / 3 (Other)   |

---

## 🏙️ City Tier Classification

| Tier       | Cities                                                       |
| ---------- | ------------------------------------------------------------ |
| **Tier 1** | Mumbai, Delhi, Bangalore, Chennai, Kolkata, Hyderabad, Pune  |
| **Tier 2** | Jaipur, Lucknow, Indore, Chandigarh, Surat, Nagpur, and more |
| **Tier 3** | All other cities                                             |

---

## 🐳 Docker

### Docker Image

The Docker image is publicly available on Docker Hub:

```
ansh0273/insurance_api
```

### Pull & Run the Docker Image

```bash
# Pull the image
docker pull ansh0273/insurance_api

# Run the container
docker run -p 8000:8000 ansh0273/insurance_api
```

Access the API at: **http://localhost:8000**

Access the interactive docs at: **http://localhost:8000/docs**

### Build Locally

```bash
# Clone the repo
git clone https://github.com/anshsoni0512/Fast-API-Advance.git
cd Fast-API-Advance

# Build Docker image
docker build -t insurance-app .

# Run Docker container
docker run -p 8000:8000 insurance-app
```

---

## ☁️ AWS Deployment

This API is deployed on **AWS** using Docker.

### Infrastructure Details:

| Detail             | Value                       |
| ------------------ | --------------------------- |
| **Cloud Provider** | Amazon Web Services (AWS)   |
| **Service**        | EC2 (Elastic Compute Cloud) |
| **Instance Type**  | `t3.micro`                  |
| **Deployment**     | Docker Container            |
| **Docker Image**   | `ansh0273/insurance_api`    |

### Deployment Steps on AWS EC2:

```bash
# 1. SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-ec2-ip

# 2. Install Docker on EC2
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# 3. Pull the Docker image
docker pull ansh0273/insurance_api

# 4. Run the container
docker run -d -p 8000:8000 ansh0273/insurance_api
```

- The `/health` endpoint is configured for **AWS Elastic Load Balancer** health checks
- The app runs on `0.0.0.0` to accept traffic from all incoming sources
- Port `8000` is exposed via EC2 **Security Group** inbound rules

---

## 🛠️ Tech Stack

| Technology             | Purpose                   |
| ---------------------- | ------------------------- |
| **FastAPI**            | REST API framework        |
| **Pydantic**           | Input validation & schema |
| **scikit-learn**       | ML model (prediction)     |
| **pandas**             | Data processing           |
| **uvicorn**            | ASGI server               |
| **Docker**             | Containerization          |
| **AWS EC2 (t3.micro)** | Cloud deployment          |

---

## ⚙️ Run Locally (Without Docker)

```bash
# Clone the repo
git clone https://github.com/anshsoni0512/Fast-API-Advance.git
cd Fast-API-Advance

# Create virtual environment
python -m venv myvenv
myvenv\Scripts\activate        # Windows
# source myvenv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the API at: **http://localhost:8000**

Access Swagger UI docs at: **http://localhost:8000/docs**

---

## 📖 Interactive API Documentation

FastAPI provides **automatic interactive documentation**:

| Tool           | URL                         |
| -------------- | --------------------------- |
| **Swagger UI** | http://localhost:8000/docs  |
| **ReDoc**      | http://localhost:8000/redoc |

---

## 👨‍💻 Author

**Ansh Soni**

- GitHub: [@anshsoni0512](https://github.com/anshsoni0512)
- Email: anshsoni0512@gmail.com
