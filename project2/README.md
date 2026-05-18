# Project 2 - Theatre Production Cost Analysis System

## Project Overview

This project focuses on analysing the different types of costs involved in a theatre production. It aims to identify and structure all relevant expense categories, including logistics, artistic team, production, and unexpected costs. The goal is to provide a clear overview of what influences the total budget of a production.

---

## Project Structure

```bash
.
├── README.md
├── data
│   └── raw
│       └── data.xlsx
│
├── requirements.txt
├── models_saved
│   ├── model.pkl
│   └── metrics.json
│
├── src
│   ├── data
│   │   ├── dataset_loader.py
│   │   ├── preprocess.py
│   │
│   ├── features
│   │   └── build_features.py
│   │
│   ├── models
│   │   ├── ablation_runner.py
│   │   ├── experiment_results.py
│   │   ├── experiments.py
│   │   ├── model_registry.py
│   │   ├── model_trainer.py
│   │   ├── model_selector.py
│   │   ├── model_evaluator.py
│   │   ├── model_persistence.py
│   │
│   └── utils
│       ├── logger.py
│
├── tests
│   ├── test_api.py
│   ├── test_data.py
│   ├── test_experiments.py
│   ├── test_metrics_models.py
│   ├── test_model.py
│   ├── test_preprocess.py
│   ├── test_build_features.py
│
└── webapp
    ├── app.py
    ├── settings.py
    ├── static
    │   ├── css
    │   └── js
    └── templates
        ├── index.html
        ├── layout.html
        ├── result.html
        └── comparison.html
```

---

## Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## How to Run the Project

### 1. Go to the project root directory

```bash
cd project2
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Train or retrain the model

```bash
python -m src.pipeline.training_pipeline
```

This creates/updates:

```bash
models_saved/model.pkl
models_saved/metrics.json
```

---

### 4. Run the Flask application

```bash
python -m webapp.app
```

---

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## How it works

The system follows a machine learning pipeline:

- Load dataset from Excel
- Preprocess data (cleaning, missing values, encoding)
- Feature engineering
- Split into train and test sets
- Train multiple model pipelines
- Scale features inside each saved model pipeline
- Evaluate models using classification metrics
- Select best model (F1-score)
- Save model and metrics
- Serve predictions via Flask API

---

## Cost Categories Considered

### Transportation

* Distance between the company base and the event location
* Need for a van or private bus (or not)
* Fuel and toll costs
* Transport of scenery and large materials (may require a dedicated vehicle)
* Weight limitations of light vehicles
* Transport of technical crew and artistic team (not only actors), possibly requiring multiple vehicles

---

### Artistic Team

* Cachet (fixed payment for a performance or participation) of external actors or professionals
* Equivalent to a salary for the production
* Includes guest performers not part of the resident company

---

### Set Design and Visual Production

* Construction of sets (materials and labour)
* Set designer fees
* Rental of pre-made scenic elements
* Painting, props, and additional decoration
* Storage or transport of set pieces

---

### Costumes and Characterisation

* Purchase or rental of costumes
* Costume designer or tailor
* Makeup and hair styling if required

---

### Food and Accommodation

* Catering for technical and artistic teams (often provided by the organiser)
* Snacks and water during rehearsals and performances (often provided)
* Accommodation for external members (hotel, hostel, or local lodging), often covered by the organiser

---

### Technical Production

* Some companies already have their own technical system and hired technician
* Lighting equipment and lighting technician
* Sound system (microphones, speakers, sound technician)
* Stage technicians for setup, teardown, and operation

---

### Venue and Logistics

* Licences or authorisations when applicable (e.g. royalties or author rights fees paid to playwright associations such as AAVP when required)

---

### Communication and Promotion

* Marketing and social media campaigns (usually handled by the theatre or production team)
* Paid advertising if needed

---

### Unexpected Costs

* Emergency budget (typically 5% to 15% of total cost)
* Repair or replacement of damaged materials (costumes, props, etc.)
* Delays increasing technician or venue costs

---

## Technologies Used

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy
* HTML / CSS / JavaScript
* Pytest (testing framework)
* Pickle (model persistence)


---

## How to Run Tests

The project includes a full test suite covering data processing, feature engineering, model training, and API endpoints.

### 1. Install test dependencies

If you already installed `requirements.txt`, nothing extra is needed. Otherwise:

```bash
pip install pytest
```

### 2. Run all tests

From the `project2` directory:

```bash
pytest
```


### 3. Run tests with more detail

```bash
pytest -v
```

### 4. Run a specific test file

```bash
pytest tests/test_data.py
```

or

```bash
pytest tests/test_model.py
```

### 5. Run a specific test function

```bash
pytest tests/test_preprocess.py::test_clean_drops_leakage_columns
```


## What is tested

* Dataset loading (Excel ingestion and sheet handling)
* Data preprocessing pipeline
* Feature engineering functions
* Model training and selection logic
* Model registry pipelines, including feature scaling
* Model evaluation metrics
* Flask API endpoints and prediction behavior

---

