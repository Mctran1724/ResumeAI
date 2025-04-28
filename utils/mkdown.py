import os, pathlib
from google import genai
from markdown_pdf import MarkdownPdf, Section

class ResumeMarkdownWriter:
    def __init__(self, resume_string: str):        
        self._resume_text = resume_string
        self._api_key = os.environ.get("GEMINI_API_KEY")
        if self._api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        self.client = genai.Client(api_key=self._api_key)
        
        current_directory = pathlib.Path(__file__).parent
        self._assets_directory = current_directory.parent / 'assets'
        
    def _prompt(self):
        resume_text = self._resume_text
        prompt = f"""
        Prompt Title: Resume Text to Compact Markdown Conversion

Model Role: You are an expert resume formatter and Markdown generator. Your task is to convert raw resume text into a well-structured, aesthetically pleasing, and easily readable Markdown document. The Markdown should be formatted efficiently to maximize content density, aiming to fit onto a single page when rendered with narrow margins (like 0.5 inches), while maintaining clarity.

Input:

Resume Text: {resume_text} - The complete text content of the resume.
Instructions:

Parse Resume Text: Carefully read the provided {resume_text}. Identify and extract the following key pieces of information and sections:

Candidate's full name.
Contact information: Portfolio Website URL and text, LinkedIn URL and text, Location (City, State), Phone number, and Email address.
Professional Summary: The introductory paragraph.
Experience: Each job entry, including Company Name, Location, Job Title, Dates of Employment, and the list of bullet points describing responsibilities and achievements.
Education: Each educational entry, including Institution Name, Location, Degree(s) and Honors (e.g., Summa Cum Laude), Date(s) of Graduation/Completion, and GPA if listed. Include certifications as separate education entries if they follow a similar structure (Name, Institution/Source, Date).
Additional Information / Skills: Any sections listing technical skills, technologies, languages, awards, or other relevant details. Identify skill categories and the items within them.
Map to Markdown Structure & Format: Generate the Markdown code using standard Markdown syntax.

Use a top-level heading (#) for the candidate's full name.
Format the contact information on one or two lines immediately following the name, using separators like | or ⋄ between items. Use Markdown link syntax [text](URL) for website and LinkedIn.
Use a horizontal rule (---) below the contact information.
Use second-level headings (##) for major sections (e.g., "PROFESSIONAL SUMMARY", "EXPERIENCE", "EDUCATION", "ADDITIONAL INFORMATION"). Ensure section titles are clear and consistently formatted (e.g., all uppercase).
For the Professional Summary, place the paragraph text directly under its heading.
For each Experience entry, use bold text (**) for the Company Name, followed by Location and Dates. The Job Title can be on the same line or the next line, possibly in bold or italics. Create an unordered list (* or -) for the bullet points under each entry.
For each Education entry, use bold text (**) for the Institution Name, followed by Location and Dates. The Degree(s) and Honors can be on the next line, possibly in bold. Include the GPA if listed, potentially on its own line or with the degree information.
For the Additional Information / Skills section, use the main heading (##). Within this section, use bold text (**) for skill categories (e.g., Skills and Technologies). List the skills under each category using an unordered list (* or -). You can combine related skills on a single list item if it enhances compactness and readability (e.g., * Computation: Python, Excel, Jupyter).
Use horizontal rules (---) to separate major sections (Summary, Experience, Education, Additional Info).
Focus on Compactness: Minimize the use of excessive blank lines between elements. Combine related pieces of information onto single lines where logical and readable (e.g., contact info, company/location/dates). Ensure lists are formatted efficiently. The goal is a dense, but still highly readable, Markdown output.
Address Rendering Goal: While you cannot control the final PDF/HTML rendering engine's margin and pagination settings directly, format the Markdown to be as concise as possible to facilitate fitting on one page with narrow margins. Acknowledge that the final output size depends on the rendering tool used.

Generate Output: Provide the complete formatted Markdown code within a single markdown code block (markdown ...).

Explanation: After the code block, provide a brief explanation detailing:

How the Markdown structure maps to the resume sections.
The specific Markdown syntax used (headings, bold, lists, links, rules).
Mention that the formatting was optimized for compactness to help meet the one-page/narrow-margin rendering goal, while noting that the final result depends on the rendering tool.
Constraint: Your output must be valid Markdown syntax. The formatting should prioritize readability and compactness.
        """
        return prompt
    
    def write_markdown(self, file_name: str = "resume_temp") -> None:
        prompt = self._prompt()

        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt   
        )

        file_path = self._assets_directory / f"{file_name}.md"

        response_text = response.text.split(r"```") #extract the explanation
        
        markdown_block = response_text[1][8:] #strips out only the markdown portion
        self.markdown_text = markdown_block

        with open(file_path, "w+") as f:
            f.write(markdown_block)
        print("MD file written successfully to ", file_path)
        return 

    def markdown_to_pdf(self, file_name: str = "resume_temp") -> str:
        pdf = MarkdownPdf(toc_level=2, optimize=True)
        pdf.meta['title'] = 'Resume'
        pdf.meta['author'] = 'Michael Tran'
        section = Section(self.markdown_text)
        pdf.add_section(section)
        pdf.save(self._assets_directory / f"{file_name}.pdf")
        return self._assets_directory / f"{file_name}.pdf"
    

    

if __name__=='__main__':
    file_path = pathlib.Path(__file__).parent.parent / 'assets' / 'test_resume.txt'

    with open(file_path, 'r') as f:
        resume_string = f.read()

    md = ResumeMarkdownWriter(resume_string)
    md.write_markdown()
    md.markdown_to_pdf()