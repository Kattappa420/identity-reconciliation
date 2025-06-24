# Identity Reconciliation API

A FastAPI-based backend to intelligently link contact information (emails and phone numbers) across multiple entries. This helps deduplicate customer data in ecommerce platforms like Zamazon.

## Project Purpose

Moonrider is integrating technology into Zamazon to reconcile customer identities. This service accepts contact details (`email`, `phoneNumber`) and links them if they belong to the same user, even if entered differently across multiple orders.

This enables a unified customer profile and supports better personalization, analytics, and fraud prevention.

## Tech Stack

- FastAPI: Web framework
- SQLite: Lightweight database
- SQLAlchemy: ORM to interact with the database
- Pydantic: Data validation

## Setup Instructions

### 1. Clone this repository
```
git clone https://github.com/Kattappa420/identity-reconciliation.git
cd identity-reconciliation
```
### 2. Setup a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Run the server
```
uvicorn main:app --reload
```
## Sample flow
```
First call with new email & phone creates a primary contact.

Second call with same phone but different email creates a secondary contact.

Subsequent calls return all linked identities under one profile.
```
## Project Structure

```
├── main.py          # FastAPI app and business logic
├── models.py        # Contact table schema
├── database.py      # Database setup and session
├── schemas.py       # Input/output models
├── requirements.txt # Python dependencies
└── .gitignore       # Ignored files and folders
```

