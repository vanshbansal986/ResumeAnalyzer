# Resume Screening Automation with Generative AI

## Project Overview
This project demonstrates the power of Generative AI in automating resume screening, significantly reducing manual effort and improving the recruitment process. By parsing resumes, scoring them based on key fields, and processing multiple resumes in batches, the solution aims to streamline the shortlisting process while maintaining high accuracy and scalability.

The solution integrates GPT models (or equivalent) to complement data extraction, ensuring relevance and context in the output. It also leverages creative AI features for innovative insights and additional value.

## Key Features
- **Generative AI Integration**: The solution uses advanced language models (GPT or equivalent) to extract relevant contextual data from resumes, ensuring accurate and meaningful results.
- **Resume Parsing**: Automatic extraction of essential fields like skills, work experience, education, and contact details from PDF resumes.
- **Batch Processing**: Handles large numbers of resumes simultaneously, ensuring quick and efficient processing.
- **Excel Output**: Outputs neatly formatted Excel files containing parsed data and scores.
- **Scoring Mechanism**: Each resume is scored based on the relevance of extracted information, with custom scoring logic for role match, experience, and other factors.
- **Scalability**: Designed to efficiently process larger sets of resumes while maintaining speed and accuracy.

## Results
Results can be viewed in [Results](artifacts/resume_analyze/data.xlsx)

## How It Works

### 1. **Data Ingestion**
The `AnalyzeResume` class is at the core of the process. It handles the following functions:
- **Extract Text from PDF**: The `extract_text_from_pdf` method parses the text from PDF resumes and retrieves any embedded hyperlinks.
- **Generate JSON Data**: The `generate_json_data_from_resume` method generates structured JSON data from the extracted resume text, leveraging a GPT model for enhanced context extraction.
- **Excel File Update**: The `update_or_create_excel` method ensures that the extracted data is either appended to or saved into a new Excel file for further analysis.

### 2. **Batch Processing**
The `analyze_resumes` method processes resumes in batches, efficiently handling a large volume of files. It processes each batch, extracting data from all resumes and generating a structured dataset for each.

### 3. **Scoring and Ranking**
The extracted data is used to score the resumes based on various factors, including skills, education, and experience, against predefined criteria. This allows for logical ranking of candidates and identifies the best matches for the roles.

## Evaluation Criteria

### Generative AI Integration
The solution utilizes GPT models to enhance resume parsing, ensuring that relevant contextual data is not only extracted but also understood. This integration adds value by analyzing the meaning behind the resume content, going beyond simple text extraction.

### Accuracy
The system demonstrates high accuracy in extracting and organizing mandatory fields, even when dealing with varying resume formats and layouts. It maintains the completeness of columns such as skills, experience, and education, ensuring that all critical data is captured.

### Batch Processing Efficiency
Batch processing is handled with scalability in mind. The solution can process hundreds of resumes in parallel, significantly reducing the time it takes to generate output. The efficiency is demonstrated by processing large batches in a timely manner, without compromising the quality of data extraction.

### Scalability
The solution is designed to scale with larger datasets. By utilizing optimized batch processing and leveraging Generative AI, the system can handle increased payloads, such as processing thousands of resumes, without significant performance degradation.

### Creativity and Innovation
The use of Generative AI enables innovative features like inferred career potential and role match scores, which add further value to the output. These features are generated from the context of the resume data, providing insights beyond simple keyword matching.

### Output Quality
The solution ensures that the output is logically structured, with consistent formatting in the Excel file. The scoring mechanism ranks candidates based on relevance, ensuring that the best candidates are easily identified.

## Requirements
- Python 3.9
- Required Libraries:
  - `openai` or equivalent for GPT integration
  - `PyPDF2` for PDF extraction
  - `pandas` for Excel file manipulation
  - Any other dependencies are mentioned in the `requirements.txt` file

## Setup Instructions
1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Configure your API keys and model parameters in the `config.yaml` file.
4. Place the resume PDFs in the designated folder as per the configuration.
5. Run the batch processing script:
    ```bash
    python main.py
    ```

## Usage
- **Single Resume Processing**: To process a single resume, call the `generate_json_data_from_resume` method with the resume file path.
- **Batch Resume Processing**: Use the `analyze_resumes` method to process multiple resumes at once. The system will automatically generate and save the results in an Excel file.

## Output Example
### You can view the output results of tested resumes in `artifacts/resume_analyze/data.xlsx`<br>
The output will be an Excel file containing:
- **Extracted Fields**: Skills, Experience, Education, Contact Information.
- **Role Match Score**: A numeric score indicating how closely the resume matches the job description.
- **Career Potential Inference**: Based on the experience and skills, inferred career potential is provided.

## Future Enhancements
- **Real-time Job Description Matching**: Enhance the scoring system by integrating job descriptions to provide dynamic candidate ranking.
- **Multi-language Support**: Extend the solution to handle resumes in multiple languages.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- OpenAI (for GPT model integration)
- PyPDF2 (for PDF parsing)
- pandas (for Excel manipulation)

