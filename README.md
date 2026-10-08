# Resume Ranker

A command-line tool that ranks resumes against a job description. It combines two things: **skill matching** (which required skills appear in the resume) and **TF-IDF cosine similarity** (how similar the overall wording is). I built it to practise NLP basics with scikit-learn after working on text-processing tasks in Python.

The output explains *why* a resume got its score, showing matched skills, missing skills and the key terms that pushed the similarity up.

## Features

- Extracts skills from text using a keyword dictionary with aliases (`sklearn` → scikit-learn, `ml` → machine learning)
- Handles tricky names like `C++` and avoids false matches (`java` inside `javascript`)
- TF-IDF with unigrams + bigrams, cosine similarity against the job description
- Final score = 70% skill coverage + 30% text similarity
- Shows matched skills, missing skills and top shared terms for every resume
- Saves the full ranking to a CSV file

## Tech used

Python 3.10+, scikit-learn, pandas, pytest, argparse

## Project structure

```
resume-ranker/
├── matcher/
│   ├── skills.py        # skill dictionary + extraction
│   ├── similarity.py    # TF-IDF and cosine similarity
│   └── ranker.py        # combines everything, returns a DataFrame
├── data/
│   ├── resumes/             # 5 sample resumes (made up)
│   └── job_descriptions/    # 2 sample job descriptions
├── tests/
│   └── test_matcher.py
├── main.py              # command line entry point
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/vbalhara523/resume-ranker.git
cd resume-ranker

python -m venv venv
# Windows:  venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
```

## Usage

```bash
# rank all sample resumes for the backend internship
python main.py --jd data/job_descriptions/python_backend_intern.txt --resumes data/resumes

# data analyst role, show only the top 3, and save results to output/ranking.csv
python main.py --jd data/job_descriptions/data_analyst_intern.txt --resumes data/resumes --top 3 --save
```

### Example output

```
Job description : python_backend_intern.txt
Resumes checked : 5

#1  isha_verma.txt  ->  55.5%
     skill match 75.0% | text similarity 10.2%
     matched : agile, docker, dsa, flask, git, pytest, python, rest api, sql
     missing : fastapi, linux, oop
     key terms: python, flask, docker, requests, pull requests

#2  aarav_sharma.txt  ->  50.8%
     skill match 66.7% | text similarity 13.8%
     matched : dsa, fastapi, git, linux, oop, pytest, python, rest api
     missing : agile, docker, flask, sql
```

## Using your own files

- Put resumes as plain `.txt` files in a folder and pass it with `--resumes`
- Write the job description in a `.txt` file and pass it with `--jd`
- To track more skills, add entries to the `SKILLS` dictionary in `matcher/skills.py`

## Running the tests

```bash
pytest
```

## How the score works

1. Skills are extracted from the job description and from each resume.
2. **Skill coverage** = matched skills ÷ skills required by the job description.
3. **Text similarity** = cosine similarity between TF-IDF vectors of the job description and the resume.
4. **Final score** = 0.7 × skill coverage + 0.3 × text similarity. I gave skills more weight because TF-IDF similarity alone stays low (10–20%) even for good matches.

## Limitations

- Skill detection is keyword based, so it will miss skills that are not in the dictionary
- It treats "FastAPI or Flask" as two required skills instead of "either one"
- Only plain text input (no PDF parsing yet)
- The sample resumes are fictional and only meant for testing

## What I learned

- How TF-IDF turns text into vectors and why common words get low weight
- Using cosine similarity to compare documents
- Using regex lookarounds so `C++` and `scikit-learn` match correctly
- Splitting code into modules and testing each part separately

## Future improvements

- Read PDF resumes
- Treat "A or B" requirements as alternatives
- Simple web interface with Streamlit
- Try sentence embeddings instead of TF-IDF

## Author

**Vallabh Balhara** – B.Tech CSE student
[LinkedIn](https://linkedin.com/in/vallabhbalhara) · [GitHub](https://github.com/vbalhara523)

## License

MIT
