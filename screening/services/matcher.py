import os
import sys

# Import skill keywords
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from static.screening.skills import SKILL_KEYWORDS
from .extractor import extract_skills


def extract_jd_skills(job_description):
    """
    Extract required skills from job description text.
    Uses same keyword matching as resume.
    Returns list of skills.
    """
    return extract_skills(job_description)


def compute_match(resume_skills, jd_skills):
    """
    Compute skill match between resume and JD.
    
    Args:
        resume_skills: List of skills from resume
        jd_skills: List of skills from job description
    
    Returns:
        Dictionary with:
        - matched_skills: List of common skills
        - score: Match percentage (0-100)
        - message: Optional message for edge cases
    """
    # Edge case: No skills in JD
    if not jd_skills:
        return {
            'matched_skills': [],
            'score': 0.0,
            'message': 'No skills found in job description'
        }
    
    # Edge case: No skills in resume
    if not resume_skills:
        return {
            'matched_skills': [],
            'score': 0.0,
            'message': 'No skills found in resume'
        }
    
    # Convert to sets for intersection (case-insensitive)
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])
    
    # Find matched skills
    matched = resume_set.intersection(jd_set)
    
    # Preserve original casing from JD for display
    matched_skills = [s for s in jd_skills if s.lower() in matched]
    
    # Calculate match percentage
    score = (len(matched) / len(jd_set)) * 100
    
    return {
        'matched_skills': matched_skills,
        'score': round(score, 2),
        'message': None
    }


def perform_matching(resume_text, job_description):
    """
    Main matching function.
    
    Args:
        resume_text: Extracted resume text
        job_description: Job description text
    
    Returns:
        Dictionary with:
        - resume_skills: List of skills from resume
        - jd_skills: List of skills from JD
        - matched_skills: List of common skills
        - score: Match percentage
        - message: Optional message
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_jd_skills(job_description)
    
    match_result = compute_match(resume_skills, jd_skills)
    
    return {
        'resume_skills': resume_skills,
        'jd_skills': jd_skills,
        'matched_skills': match_result['matched_skills'],
        'score': match_result['score'],
        'message': match_result['message']
    }