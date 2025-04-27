from utils import Resume, JobDescription
def main():
    resume_parser = Resume.ResumeParser()
    resume_text = resume_parser.parse_pdf('C:/Users/Micha/Downloads/MTResume.pdf')
    resume_optimizer = Resume.ResumeOptimizer()
    job_description_parser = JobDescription.JobDescriptionParser()
    job_description_text: str = job_description_parser.parse_linkedin('https://www.linkedin.com/jobs/view/4213370079/')

    response = resume_optimizer.optimize_resume(resume_text, job_description_text)
    print(response)
    return


if __name__ == "__main__":
    main()
