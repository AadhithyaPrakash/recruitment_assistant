import re
import os
import sys

# Import skill keywords from static file
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from static.screening.skills import SKILL_KEYWORDS


def extract_email(text):
    """More flexible email pattern"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text, re.IGNORECASE)
    return matches[0] if matches else None

def extract_phone(text):
    """More flexible phone pattern"""
    # Remove common separators first
    cleaned = re.sub(r'[^\d+]', ' ', text)
    # Find 10+ digit sequences
    phone_pattern = r'\+?\d[\d\s]{9,}'
    matches = re.findall(phone_pattern, cleaned)
    if matches:
        phone = re.sub(r'\s', '', matches[0])
        if len(phone) >= 10:
            return phone
    return None

def extract_skills(text):
    """
    Extract skills from text by matching against SKILL_KEYWORDS.
    Case-insensitive keyword scan.
    Returns list of matched skills.
    """
    text_lower = text.lower()
    found_skills = []
    
    for skill in SKILL_KEYWORDS:
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates


def extract_metadata(text):
    """
    Main extraction function.
    Returns dictionary with email, phone, and skills.
    """
    return {
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text)
    }