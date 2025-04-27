% resume.cls
% A simple LaTeX class for creating resumes

% Requires LaTeX2e
\NeedsTeXFormat{LaTeX2e}
% Provides the class with a name and date
\ProvidesClass{resume}[2025/04/26 Generalized Resume] %Optional parameter to add description; yyyy/mm/dd of last update

% --- Options ---
% Define macros to hold the title and author, with default values
% Using \def is simple for this case. \edef ensures expansion if needed.
\def\@pdftitle{Resume}
\def\@pdfauthor{Candidate Name}

% Declare options that can be passed to the class
% #1 refers to the value passed to the option (e.g., value of pdftitle=...)
\DeclareOption{pdftitle}{\edef\@pdftitle{#1}}
\DeclareOption{pdfauthor}{\edef\@pdfauthor{#1}}

% Pass any other options (like font size) to the underlying class (article)
\DeclareOption*{%
    \PassOptionsToClass{\CurrentOption}{article}%
}

% Process all declared and passed options
\ProcessOptions* % Use * to process all options

% Load the base class (article)
\LoadClass[11pt]{article}

% --- Packages ---
% Geometry for margins
\RequirePackage{geometry}
\geometry{letterpaper, margin=0.5in} % Default margin - adjust as needed

% Hyperref for clickable links
\RequirePackage{hyperref}
\hypersetup{
    colorlinks=true,
    urlcolor=blue,
    linkcolor=blue,
    citecolor=blue,
    pdftitle={\@pdftitle}, % Document Metadata
    pdfauthor={\@pdfauthor} % Document Metadata
}

% Enumitem for list customization
\RequirePackage{enumitem}
% Configure itemize lists to be compact
\setlist[itemize]{leftmargin=*, itemsep=0.5pt, parsep=0.1pt, topsep=0pt, partopsep=0pt}

% Titlesec for section title formatting
\RequirePackage{titlesec}
% Configure section spacing
\titlespacing*{\section}{0pt}{0.4em}{0.4em} % Space before, after title

% Parskip for aligning paragraphs
\RequirePackage{parskip}

% --- Page Style ---
% Remove page numbering
\pagestyle{empty}

% --- Custom Commands and Environments ---

% Command for the main header (Name and contact info)
% Arguments:
% #1: Name
% #2: Website URL
% #3: Website Text
% #4: LinkedIn URL
% #5: LinkedIn Text
% #6: Location
% #7: Phone
% #8: Email
\newcommand{\makeheader}[8]{
    \begin{center}
        {\fontsize{24pt}{28pt}\selectfont \textbf{#1}} \\ % Name (larger font)
        \vspace{0.2em}
        \href{#2}{#3} $|$ \href{#4}{#5} \\
        #6 $|$ #7 $|$ \href{mailto:#8}{#8}
    \end{center}
}

% Command for horizontal separator line
\newcommand{\separator}{\vspace{0.4em}\hrule\vspace{0.4em}}

% Redefine \section to be unnumbered by default and uppercase the title
\let\oldsection\section % Save original \section
\renewcommand{\section}[1]{\oldsection*{\MakeUppercase{#1}}} % Use unnumbered and uppercase


% Environment for Experience entries
% Arguments:
% #1: Company Name
% #2: Location
% #3: Title
% #4: Dates
\newenvironment{experience}[4]{
    \vspace{0.1em}% Space before entry
    \textbf{#1} \hfill #2 \\ % Company | Location
    \textit{#3} \hfill #4 % Title | Dates (italicize title)
    \begin{itemize} % Start bullet points for responsibilities
}{
    \end{itemize}
    % \vspace{-0.5em} % Optional: Reduce space after bullet list if needed
}


% Environment for Education entries
% Arguments:
% #1: Institution Name
% #2: Location
% #3: Degree(s) and Honors
% #4: Date(s)
% #5 GPA (optional)
\newenvironment{educationentry}[5]{
     \vspace{0.1em}% Space before entry
    \textbf{#1} \hfill #2 \\ % Institution | Location
    #3 \hfill #4 \\ % Degree(s) | Date(s)
    #5  %GPA
}{
    \vspace{-0.5em} % Optional: Reduce space after this block
}


% --- End of resume.cls ---