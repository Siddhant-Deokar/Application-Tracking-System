import streamlit as st
from resume_processing import ResumeParser  # Ensure the class name is correctly cased
from jd_skill import JdParser  # Ensure the class name is correctly cased
from preprocessing import ResumePreprocessor  # Importing the preprocessor

# Initialize preprocessor
preprocessor = ResumePreprocessor()


# Function to calculate ATS score based on skill matching and education weights
def calculate_ats_score(extracted_skills, extracted_jd_skills, education, education_weights):
    score = 0

    # Skill Matching
    matched_skills = set(extracted_skills) & set(extracted_jd_skills)  # Intersection of skills
    len_total_skills = len(extracted_jd_skills)
    if len_total_skills > 0:
        skill_match_percentage = (len(matched_skills) / len_total_skills) * 100
    else:
        skill_match_percentage = 0

    # Skill score (75% weight)
    skill_score = skill_match_percentage * 0.75  # Adjust weight as needed
    score += skill_score

    # Education score (25% weight)
    education_score = 0
    for edu in education:
        for key in education_weights:
            if key.lower() in edu.lower():  # Match education level
                education_score = education_weights[key] * 0.25 # Weight for education
                score += education_score
                break  # Once education is matched, move to next

    # Final ATS score is a combination of both
    return round(score, 2)




def main():
    st.title("ATS Score Calculator")

    # Upload Resume and JD as PDF
    resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
    jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

    if resume_file is not None and jd_file is not None:
        
        # Parse Resume using ResumeParser
        st.subheader("Parsing Resume...")
        resume_text = preprocessor.extract_text_from_pdf(resume_file)
        
        # Create an instance of ResumeParser
        resume_parser = ResumeParser()

        # Use the parser to extract details
        name, contact_number, email, education, extracted_skills = resume_parser.parse_resume(resume_text)

        # Display parsed user details
        st.subheader("User Details from Resume:")
        st.write(f"*Name:* {name}")
        st.write(f"*Contact Number*: {contact_number}")
        st.write(f"*Email:* {email}")
        st.write("*Education:*")
        for i in education :
            st.write(i)
            st.write("---")

        st.write(f"*Skills from Resume*: {', '.join(extracted_skills) if extracted_skills else 'None'}")

        # Parse JD using JdParser
        st.subheader("Parsing Job Description...")
        jd_text = preprocessor.extract_text_from_pdf(jd_file)

        # Create an instance of JdParser
        jd_parser = JdParser()

        # Extract skills from the job description
        extracted_jd_skills = jd_parser.parse_jd(jd_text)  # Pass JD text to the method
        st.write(f"*Skills from Job Description*: {', '.join(extracted_jd_skills) if extracted_jd_skills else 'None'}")

        # Define education weights
        education_weights = {
            "bsc": 20,
            "msc": 30,
            "phd": 50
        }
       

        # Calculate ATS score
        ats_score = calculate_ats_score(
            extracted_skills, extracted_jd_skills, education, education_weights)

        # Display ATS Score
        st.subheader("ATS Score:")
        st.write(f"*ATS Score*: {ats_score}")

        if st.checkbox("Show Resume Text"):
            st.subheader("Resume Text:")
            st.write(resume_text)  # Display the extracted resume text
    else:
        st.info("Please upload both the Resume and Job Description as PDF files.")

if __name__ == '__main__':
    main()
