"""
Resume Ranker - command line tool.

Example:
    python main.py --jd data/job_descriptions/python_backend_intern.txt --resumes data/resumes
    python main.py --jd data/job_descriptions/data_analyst_intern.txt --resumes data/resumes --top 3 --save
"""
import argparse
import sys
from pathlib import Path

from matcher.ranker import rank_resumes, read_text_files


def main():
    parser = argparse.ArgumentParser(description="Rank resumes against a job description.")
    parser.add_argument("--jd", required=True, help="path to the job description .txt file")
    parser.add_argument("--resumes", required=True, help="folder with resume .txt files")
    parser.add_argument("--top", type=int, default=None, help="only show the top N resumes")
    parser.add_argument("--save", action="store_true", help="save the ranking to output/ranking.csv")
    args = parser.parse_args()

    jd_path = Path(args.jd)
    if not jd_path.exists():
        print(f"Job description not found: {jd_path}")
        sys.exit(1)

    resumes = read_text_files(args.resumes)
    if not resumes:
        print(f"No .txt resumes found in {args.resumes}")
        sys.exit(1)

    df = rank_resumes(jd_path.read_text(encoding="utf-8"), resumes)
    shown = df.head(args.top) if args.top else df

    print(f"\nJob description : {jd_path.name}")
    print(f"Resumes checked : {len(resumes)}\n")
    for rank, row in shown.iterrows():
        print(f"#{rank}  {row['resume']}  ->  {row['final_score']}%")
        print(f"     skill match {row['skill_match_%']}% | text similarity {row['text_similarity_%']}%")
        print(f"     matched : {row['matched_skills'] or '-'}")
        print(f"     missing : {row['missing_skills'] or '-'}")
        print(f"     key terms: {row['top_terms'] or '-'}\n")

    if args.save:
        out = Path("output")
        out.mkdir(exist_ok=True)
        path = out / "ranking.csv"
        df.to_csv(path)
        print(f"Saved ranking -> {path}")


if __name__ == "__main__":
    main()
