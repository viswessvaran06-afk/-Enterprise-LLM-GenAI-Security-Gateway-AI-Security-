from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

PII_ENTITIES = [
    "CREDIT_CARD",
    "US_SSN",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "PERSON",
    "LOCATION",
    "US_BANK_NUMBER",
    "IBAN_CODE",
    "IP_ADDRESS",
]

def detect_pii(text: str):
    results = analyzer.analyze(
        text=text,
        entities=PII_ENTITIES,
        language="en"
    )
    return results

def anonymize_text(text: str):
    results = detect_pii(text)
    
    if not results:
        return text, False, None
    
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators={
            "CREDIT_CARD": OperatorConfig("replace", {"new_value": "[CREDIT_CARD]"}),
            "US_SSN": OperatorConfig("replace", {"new_value": "[SSN]"}),
            "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "[EMAIL]"}),
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "[PHONE]"}),
            "PERSON": OperatorConfig("replace", {"new_value": "[PERSON]"}),
            "LOCATION": OperatorConfig("replace", {"new_value": "[LOCATION]"}),
            "US_BANK_NUMBER": OperatorConfig("replace", {"new_value": "[BANK_NUMBER]"}),
            "IBAN_CODE": OperatorConfig("replace", {"new_value": "[IBAN]"}),
            "IP_ADDRESS": OperatorConfig("replace", {"new_value": "[IP_ADDRESS]"}),
        }
    )
    
    entities_found = [r.entity_type for r in results]
    return anonymized.text, True, entities_found