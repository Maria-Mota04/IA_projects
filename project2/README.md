# Project 2 - Theatre Production Cost Analysis System

## Project Overview

This project focuses on analysing the different types of costs involved in a theatre production. It aims to identify and structure all relevant expense categories, including logistics, artistic team, production, and unexpected costs. The goal is to provide a clear overview of what influences the total budget of a production.

---

## Project Structure

```bash
.
├── README.md
├── data
│   ├── processed
│   ├── raw
│   └── synthetic
│
├── environment.yml
├── requirements.txt
├── models_saved
│
├── src
│   ├── api
│   │   ├── app.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── data
│   │   ├── dataset_loader.py
│   │   ├── generate_data.py
│   │   └── preprocess.py
│   │
│   ├── features
│   │   └── build_features.py
│   │
│   ├── models
│   │   ├── evaluate.py
│   │   ├── model.py
│   │   ├── predict.py
│   │   └── train_model.py
│   │
│   └── utils
│       ├── config.py
│       ├── helpers.py
│       └── logger.py
│
├── tests
│   ├── test_api.py
│   ├── test_data.py
│   └── test_model.py
│
└── webapp
    ├── app.py
    ├── settings.py
    │
    ├── static
    │   ├── css
    │   ├── images
    │   └── js
    │
    └── templates
        ├── index.html
        ├── layout.html
        └── result.html
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

### 3. Run the Flask application

```bash
cd webapp
python3 app.py
```

---

### 4. Open in browser

```
http://127.0.0.1:5000
```

---

## How it works

The system is organised around different cost categories that are analysed individually and then combined to understand the full production budget.

The main workflow is:

1. Define cost categories
2. Input or estimate values for each category
3. Analyse total production cost and contributing factors

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
* HTML / CSS / JavaScript
* Scikit-learn (optional)
* NumPy / Pandas (optional)
