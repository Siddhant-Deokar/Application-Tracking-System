import re
import json
import spacy
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text
import os
from spacy.cli import download


class ResumePreprocessor:
    def __init__(self):
        try:
            # Attempt to load the model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If the model is not available, download and then load it
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        self.matcher = Matcher(self.nlp.vocab)

    def extract_text_from_pdf(self, pdf_path):
        """Extracts text from a PDF file."""
        return extract_text(pdf_path)

    def extract_contact_number_from_resume(self, text):
        """Extracts the contact number from the resume text."""
        contact_number = None
        pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
        match = re.search(pattern, text)
        if match:
            contact_number = match.group()
        return contact_number

    def extract_email_from_resume(self, text):
        """Extracts the email address from the resume text."""
        email = None
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        match = re.search(pattern, text)
        if match:
            email = match.group()
        return email

    def extract_name(self, resume_text):
        """Extracts the name from the resume text using spaCy."""
        matcher = Matcher(self.nlp.vocab)

        # Define name patterns
        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # Four names
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # Three names
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}]  # Two names
        ]

        for pattern in patterns:
            matcher.add('NAME', [pattern])

        doc = self.nlp(resume_text)
        matches = matcher(doc)

        for match_id, start, end in matches:
            span = doc[start:end]
            return span.text

        return None

    def extract_education_from_resume(self, text):
        """Extracts education information from the resume text."""
        education = []

        # Use regex pattern to find education information
        pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"

        matches = re.findall(pattern, text)
        for match in matches:
            education.append(match.strip())    

        return education

    def remove_extracted(self, text, education, email, phone):
        """Removes extracted information from the text."""
        for edu in education:
            text = text.replace(edu, "")
        if email:
            text = text.replace(email, "")
        if phone:
            text = text.replace(phone, "")
        return text

    def load_skills_from_json(self, file_path):
        """Loads skill patterns from a JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)

    def extract_skills(self, text, patterns):
        """Extracts skills from the resume text using defined patterns."""
        doc = self.nlp(text.lower())
        matcher = Matcher(self.nlp.vocab)

        # Add patterns to the matcher
        for pattern in patterns:
            matcher.add(pattern['label'], [pattern['pattern']])
        
        matches = matcher(doc)
        found_skills = set()

        for match_id, start, end in matches:
            span = doc[start:end]
            found_skills.add(span.text)

        return list(set(found_skills))
