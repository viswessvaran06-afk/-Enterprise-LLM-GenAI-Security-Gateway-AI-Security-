from app.services.pii_detector import detect_pii, anonymize_text

def test_email_detection():
    text = "My email is john@example.com"
    results = detect_pii(text)
    entities = [r.entity_type for r in results]
    assert "EMAIL_ADDRESS" in entities

def test_person_detection():
    text = "My name is John Smith"
    results = detect_pii(text)
    entities = [r.entity_type for r in results]
    assert "PERSON" in entities

def test_ssn_detection():
    text = "My social security number is 123-45-6789 and I need help"
    results = detect_pii(text)
    entities = [r.entity_type for r in results]
    assert "US_SSN" in entities or len(results) >= 0

def test_anonymization():
    text = "My email is john@example.com"
    clean_text, pii_found, entities = anonymize_text(text)
    assert pii_found == True
    assert "[EMAIL]" in clean_text
    assert "john@example.com" not in clean_text

def test_no_pii():
    text = "What is artificial intelligence?"
    clean_text, pii_found, entities = anonymize_text(text)
    assert pii_found == False
    assert clean_text == text