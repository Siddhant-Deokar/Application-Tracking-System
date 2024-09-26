from preprocessing import ResumePreprocessor

preprocessor = ResumePreprocessor()

class ResumeParser:
    def parse_resume(self, resume_text):
        # Extract name, contact number, email, etc. from the resume_text
        name = preprocessor.extract_name(resume_text)
        contact_number = preprocessor.extract_contact_number_from_resume(resume_text)
        email = preprocessor.extract_email_from_resume(resume_text)
        education = preprocessor.extract_education_from_resume(resume_text)

        # Clean the text and extract skills
        clean_resume_text = preprocessor.remove_extracted(resume_text, education, email, contact_number)
        patterns = preprocessor.load_skills_from_json("skill.json")
        extracted_skills = preprocessor.extract_skills(clean_resume_text, patterns)

        return name, contact_number, email, education, extracted_skills



