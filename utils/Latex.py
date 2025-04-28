import os, pathlib, subprocess
from google import genai


class ResumeLatexWriter:
    def __init__(self, resume_string: str) -> None:
        self._resume_text = resume_string
        self._api_key = os.environ.get("GEMINI_API_KEY")
        if self._api_key is None:
            raise ValueError("GEMINI_API_KEY environment variable not found")
        self.client = genai.Client(api_key=self._api_key)
        
        current_directory = pathlib.Path(__file__).parent
        self._assets_directory = current_directory.parent / 'assets'
        template_path = self._assets_directory / 'resume.cls'
        self._template = template_path.read_text()

    def _prompt(self) -> str:
        text_input = f"""Resume Text: {self._resume_text} - The complete text content of the resume.
    Resume Class Code: (Provided below) - The LaTeX code for the resume.cls file that defines the template structure and commands.
    Resume Class LaTeX Code (resume.cls): {self._template}""" 
        
        prompt = r"""
    Prompt Title: Resume Text to LaTeX Conversion using resume.cls

    Model Role: You are an expert LaTeX typesetter and resume formatter. Your task is to convert raw resume text into a structured LaTeX document using a specific, provided .cls file as a template. You must parse the resume content, identify sections and details, and accurately map them to the custom commands and environments defined in the class file.

    Input: """ + text_input + r"""

    Instructions:

    Parse Resume Text: Carefully read the provided resume text. Identify the following key sections and their corresponding details:

    Header: Candidate's full name, portfolio website URL and text, LinkedIn URL and text, location, phone number, and email address.
    Professional Summary: The summary paragraph.
    Experience: Each job entry, including Company Name, Location, Job Title, Dates of Employment, and the list of bullet points describing responsibilities and achievements.
    Education: Each educational entry, including Institution Name, Location, Degree(s) and Honors (e.g., Summa Cum Laude), Date(s) of Graduation/Completion, and GPA if listed separately for that entry. Include certifications as separate education entries if they fit the structure.
    Additional Information / Skills: Sections listing skills, technologies, or other relevant information, typically presented as lists or categories.
    Map to resume.cls Structure: Generate the LaTeX code (.tex file content) that uses the provided resume.cls.

    Start the document with \documentclass{resume}.
    Add \begin{document} and \end{document}.
    Use the candidate's name for the pdftitle and pdfauthor options in \documentclass.
    Use the extracted header information as arguments for the \makeheader command. Ensure the arguments are in the correct order: #1: Name, #2: Website URL, #3: Website Text, #4: LinkedIn URL, #5: LinkedIn Text, #6: Location, #7: Phone, #8: Email. If any are not present, use empty curly braces in place of that argument.
    Use the \separator command to add horizontal lines between major sections as appropriate (Header, Summary, Experience, Education, Additional Information).
    Use the \section{...} command (which is redefined in the class to be unnumbered and uppercase) for each main section title (e.g., PROFESSIONAL SUMMARY, EXPERIENCE, EDUCATION, ADDITIONAL INFORMATION).
    For each experience entry, use the experience environment: \begin{experience}{Company Name}{Location}{Title}{Dates}. Place each bullet point from that experience entry inside this environment using the \item command and do not add a period. 
    For each education entry (including certifications that fit), use the educationentry environment: \begin{educationentry}{Institution}{Location}{Degree(s) & Honors}{Dates}{GPA}. Note that GPA is the 5th argument. If a GPA is not listed for an entry, provide empty curly braces for the 5th argument, otherwise provide {GPA: $gpa_value} where $gpa_value is the listed GPA.
    For any additional sections for information, skills, technologies, etc. use the \section{...}, followed by \textbf{...} with the actual subsection title if different and then a standard \begin{itemize}...\end{itemize} list for the skills, using \item for each skill or category line.
    Ensure proper LaTeX syntax, including escaping special characters if necessary and using $$ for inline math like <, > etc.
    Generate Output: Provide the complete LaTeX code for the .tex file within a single markdown code block (latex ...).

    Explanation: After the code block, provide a brief explanation detailing how the generated LaTeX code utilizes the resume.cls file and maps the resume text sections to the class's custom commands and environments.

    Constraint: Your output must be valid LaTeX code designed to be compiled with the provided resume.cls file present in the same directory. Do not include the resume.cls content in the output code block itself, only the .tex content. Do not include further explanations or clarifications in the output code block; only include valid compileable LaTeX.
    """

        return prompt
    
    def compile_latex(self, file_name: str = "resume_temp") -> None:
        """
        Compiles the LaTeX document to a PDF file and returns the path to the PDF
        file.

        Args:
            file_path (str): The path to the LaTeX document.

        Returns:
            str: The path to the PDF file.
        """
        file_path = self._assets_directory / f"{file_name}.tex"
        
        # Use subprocess to call the LaTeX compiler on your machine 
        # TODO maybe use docker to ensure that a compiler is installed?
        

        return None
    
    def write_latex(self, file_name: str = "resume_temp") -> None:
        prompt = self._prompt()

        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt   
        )

        file_path = self._assets_directory / f"{file_name}.tex"

        markdown_block = response.text
        latex_code = markdown_block.split(r"```")[1][5:]
        with open(file_path, "w+") as f:
            f.write(latex_code)
        print("LaTeX file written successfully to ", file_path)
        return 
    
    def write_resume(self, file_name: str = "resume_temp") -> None:
        """
        Writes the resume text to a LaTeX file and compiles it into a PDF
        file.

        This function uses the ``write_latex`` and ``compile_latex`` methods
        to generate a LaTeX file from the resume text and compile it into
        a PDF file. The PDF file is saved in the same directory as the LaTeX
        file.
        """
        self.write_latex(file_name)
        return

    



       

if __name__ == "__main__":
    current_directory = pathlib.Path(__file__).parent
    resume_path = current_directory.parent / 'assets' / 'test_resume.txt'
    resume_text = resume_path.read_text()

    latex_writer = ResumeLatexWriter(resume_text)
    latex_writer.write_latex()