from typing import List
import requests
from bs4 import BeautifulSoup

class JobDescriptionParser:
    def __init__(self):
        pass

    def parse_linkedin(self, link: str) -> str|List[str]:
        """
        Parses a LinkedIn job description page from the given URL.

        Args:
            link (str): The URL of the LinkedIn job description page.

        Returns:
            str | List[str]: The job description text. Returns a single string if 
            there's only one description section, otherwise returns a list of strings 
            for each found description section.

        Raises:
            RuntimeError: If the job description cannot be fetched or is not found.
        """

        response = requests.get(link)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch job description: {response.status_code}")
        job_description_HTML_string = response.text
        soup = BeautifulSoup(job_description_HTML_string, 'html.parser')
        description_texts = soup.find_all('div', class_='description__text description__text--rich')

        if not description_texts:
            raise RuntimeError("Job description not found")
        elif len(description_texts) == 1:
            return description_texts[0].text
        else:
            return [text.get_text() for text in description_texts]
        
    

if __name__=="__main__":
    link = 'https://www.linkedin.com/jobs/view/4213370079/'
    job_description_parser = JobDescriptionParser()
    job_description_text = job_description_parser.parse_linkedin(link)
    