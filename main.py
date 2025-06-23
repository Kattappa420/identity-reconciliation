from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify_contact(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email = payload.email
    phone = payload.phoneNumber

    # Step 1: Find all matches
    contacts = db.query(models.Contact).filter(
        (models.Contact.email == email) | 
        (models.Contact.phoneNumber == phone)
    ).all()

    if not contacts:
        # if no match, create new primary
        new = models.Contact(email=email, phoneNumber=phone, linkPrecedence="primary")
        db.add(new)
        db.commit()
        db.refresh(new)
        return {
            "primaryContactId": new.id,
            "emails": [new.email] if new.email else [],
            "phoneNumbers": [new.phoneNumber] if new.phoneNumber else [],
            "secondaryContactIds": []
        }

    # collecting linked contacts
    all_contacts = []
    primary = None
    for contact in contacts:
        if contact.linkPrecedence == "primary":
            primary = contact
        if contact.linkedId:
            linked = db.query(models.Contact).filter(models.Contact.id == contact.linkedId).first()
            if linked: all_contacts.append(linked)
    all_contacts += contacts

    # get the oldest primary contact
    primaries = [c for c in all_contacts if c.linkPrecedence == "primary"]
    oldest_primary = sorted(primaries, key=lambda x: x.createdAt)[0]

    # creating secondary contact if it doesn't exist
    if not any(c.email == email and c.phoneNumber == phone for c in all_contacts):
        new_secondary = models.Contact(email=email, phoneNumber=phone, linkPrecedence="secondary", linkedId=oldest_primary.id)
        db.add(new_secondary)
        db.commit()

    # response preparation
    linked_contacts = db.query(models.Contact).filter(
        (models.Contact.id == oldest_primary.id) |
        (models.Contact.linkedId == oldest_primary.id)
    ).all()

    emails = list({c.email for c in linked_contacts if c.email})
    phones = list({c.phoneNumber for c in linked_contacts if c.phoneNumber})
    secondaries = [c.id for c in linked_contacts if c.linkPrecedence == "secondary"]

    return {
        "primaryContactId": oldest_primary.id,
        "emails": emails,
        "phoneNumbers": phones,
        "secondaryContactIds": secondaries
    }
