from google import genai
import os 
import pypdf

class ResumeParser:
    def __init__(self):
        pass

    def parse_pdf(self, resume_path: str) -> str:
        resume = pypdf.PdfReader(resume_path)
        resume_text = ""
        for page in resume.pages:
            resume_text += page.extract_text()
        return resume_text
    

if __name__ == '__main__':
    resume_parser = ResumeParser()
    resume_text = resume_parser.parse_pdf('C:/Users/Micha/Downloads/MTResume.pdf')
    print(resume_text)

class ResumeOptimizer:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        self.client = genai.Client(api_key=self.api_key)

    @staticmethod
    def _prompt(resume_text, jd_text) -> str:
        prompt = f"""   
        Prompt Title: Resume Optimizer: Tailor Resume to Job Description

        Model Role: You are an expert resume analyst and wordsmith. Your goal is to analyze a specific job description and meticulously tailor a given resume to align with it, highlighting the most relevant skills, experiences, and qualifications by strategically rephrasing and optimizing the language of the resume's bullet points.

        Input:

        Resume Text: {resume_text}
        Job Description Text: {jd_text} 

        Instructions:
        Analyze the Job Description: Carefully read and analyze the provided job description text. Identify the key requirements, required skills (both technical and soft), preferred qualifications, essential duties, responsibilities, keywords, and the overall tone and focus of the role. Pay close attention to specific technologies, methodologies, industry terms, and desired outcomes mentioned.
        Analyze the Resume: Carefully read and analyze the provided resume text. Understand the candidate's work history, skills, education, and accomplishments as presented.
        Identify Alignment and Gaps: Compare the analyzed job description requirements with the resume content. Identify areas where the candidate's experience directly aligns with the job description, as well as any areas where the resume could be strengthened to better reflect the job's needs.

        Optimize Resume Bullet Points: This is the core task. Go through each relevant section of the resume (primarily experience, but potentially projects or skills) and rewrite the bullet points. 
        For each bullet point:
        Prioritize Relevance: Focus on experiences and achievements that are most relevant to the job description. If an original bullet point is not relevant, consider omitting it or significantly rephrasing it if a tangential aspect can be made relevant.
        Incorporate Keywords: Seamlessly integrate keywords, skills, and phrases directly from the job description into the rewritten bullet points where authentic and appropriate. Do not simply stuff keywords; weave them into coherent and impactful statements.
        Quantify Achievements: Where possible and relevant to the job description, rephrase bullet points to include quantifiable results or metrics (e.g., "Increased efficiency by 15%", "Managed a budget of $500k", "Supported a team of 10"). Look for opportunities to demonstrate impact.
        Mirror Language/Tone: Adjust the language and tone of the bullet points to align with the professionalism and style of the job description and the industry.
        Strengthen Action Verbs: Use strong, dynamic action verbs that convey responsibility and achievement, particularly those that resonate with the actions described in the job description.
        Ensure Clarity and Conciseness: Keep the rewritten bullet points clear, concise, and easy to read.
        Review and Refine: After optimizing the bullet points, review the entire modified section (or the full resume if all sections were processed) to ensure flow, consistency, and maximum impact in relation to the target job.
        Maintain Authenticity: While optimizing, ensure that the rewritten content accurately reflects the candidate's actual experiences and qualifications. Do not invent experiences.
        Discuss Changes: Provide a summary of the changes made to the resume, highlighting the specific sections or bullet points that have been optimized and how they align with the vocabulary and tone of the job description.
        Suggest improvements: Suggest additional potential improvements, such as adding new sections, skills, experiences, or bullet points, to further align with the job description and enhance the candidate's profile.
        
        Output Format: Provide the optimized resume text. Clearly indicate which sections or bullet points have been modified. Please present the full optimized resume for ease of use followed by a summary and explanation of the changes.
        Constraint: Focus primarily on optimizing the language within the existing structure and content of the resume. Do not add entirely new sections or invent experiences not present in the original resume text. Please limit the number of bullet points to a maximum of 6.
        Desired Output: The optimized resume text, with bullet points and professional summary strategically rewritten to align with the job description, followed by a summary and explanation of the optimizations, and lastly, any further suggestions for potential improvements to address the gaps between the job and candidate's profile.
        """
        return prompt
    
    def optimize_resume(self, resume_text, jd_text) -> str:
        prompt = self._prompt(resume_text, jd_text)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        return response.text
    
if __name__=="__main__":
    resume_optimizer = ResumeOptimizer()
    # TODO: Testing resume optimizer on sample resume and job description here
    print(resume_optimizer.api_key)