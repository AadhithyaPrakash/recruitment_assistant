import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import Resume, Job, MatchResult
from .services.parser import parse_resume
from .services.extractor import extract_metadata
from .services.matcher import perform_matching


def analyze_view(request):
    """
    Handles resume upload and job description input.
    GET: Display form
    POST: Process resume and perform matching
    """
    if request.method == 'POST':
        # Validate inputs
        if 'resume_file' not in request.FILES:
            messages.error(request, 'Please upload a resume file')
            return render(request, 'screening/analyze.html')
        
        job_description = request.POST.get('job_description', '').strip()
        if not job_description:
            messages.error(request, 'Please enter job description')
            return render(request, 'screening/analyze.html')
        
        resume_file = request.FILES['resume_file']
        job_title = request.POST.get('job_title', 'Untitled Position').strip()
        
        # Validate file type
        file_ext = os.path.splitext(resume_file.name)[1].lower()
        if file_ext not in ['.pdf', '.docx', '.doc']:
            messages.error(request, 'Only PDF and DOCX files are supported')
            return render(request, 'screening/analyze.html')
        
        # Validate file size (5MB limit)
        if resume_file.size > 5 * 1024 * 1024:
            messages.error(request, 'File size must be under 5MB')
            return render(request, 'screening/analyze.html')
        
        try:
            # Save resume file
            resume = Resume.objects.create(resume_file=resume_file)
            file_path = resume.resume_file.path
            
            # Parse resume
            extracted_text = parse_resume(file_path, file_ext)
            resume.extracted_text = extracted_text
            
            # Extract metadata
            metadata = extract_metadata(extracted_text)
            resume.email = metadata['email']
            resume.phone = metadata['phone']
            resume.save()
            
            # Create or get job
            job = Job.objects.create(
                job_title=job_title,
                description=job_description
            )
            
            # Perform matching
            match_data = perform_matching(extracted_text, job_description)
            
            # Store match result
            matched_skills_str = ', '.join(match_data['matched_skills'])
            match_result = MatchResult.objects.create(
                resume=resume,
                job=job,
                score=match_data['score'],
                matched_skills=matched_skills_str
            )
            
            # Redirect to result page
            return redirect('result', match_id=match_result.id)
            
        except Exception as e:
            messages.error(request, f'Processing error: {str(e)}')
            return render(request, 'screening/analyze.html')
    
    # GET request: show form
    return render(request, 'screening/analyze.html')


def result_view(request, match_id):
    """
    Display matching results.
    Shows resume data, JD skills, matched skills, and score.
    """
    match_result = get_object_or_404(MatchResult, id=match_id)
    
    # Prepare context
    resume = match_result.resume
    job = match_result.job
    
    # Parse matched skills from stored string
    matched_skills = [s.strip() for s in match_result.matched_skills.split(',') if s.strip()]
    
    # Re-extract skills for display
    from .services.extractor import extract_skills
    resume_skills = extract_skills(resume.extracted_text)
    jd_skills = extract_skills(job.description)
    
    context = {
        'match_result': match_result,
        'resume': resume,
        'job': job,
        'resume_skills': resume_skills,
        'jd_skills': jd_skills,
        'matched_skills': matched_skills,
        'score': match_result.score,
        # Show first 500 chars of extracted text
        'extracted_text_preview': resume.extracted_text[:1500] + '...' if len(resume.extracted_text) > 500 else resume.extracted_text
    }
    
    return render(request, 'screening/result.html', context)