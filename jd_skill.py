from preprocessing import ResumePreprocessor


class JdParser:
    def parse_jd(self, jd_text):
        """Parses the job description text."""
        # Extract skills using the preprocessor
        preprocessor = ResumePreprocessor()
        
        # Load skill patterns
        patterns = preprocessor.load_skills_from_json("./skill.json")
        
        # Extract skills from the JD text
        extracted_skills = preprocessor.extract_skills(jd_text, patterns)
        
        if extracted_skills:
            print("Skills from Job Description:", extracted_skills)
        else:
            print("No skills found in Job Description")
        
        return extracted_skills
