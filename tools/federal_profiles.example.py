"""Example of the PRIVATE profiles file that tools/build_resume.py --federal reads.

Copy this to applications/profiles.py (that folder is git-ignored) and replace every value. The file is
exec'd inside build_resume.py, so it can use CITY, REGION, FED_BULLETS and the other names defined there.
Keep real dates, hours, announcement numbers and employer details ONLY in the private copy.

Each application needs: dir, date_style ("day" for MM/DD/YYYY, "month" for MM/YYYY), an optional
location, a `fed` dict (stem, title, target, tagline, keywords, summary, highlights, skills,
publications), and `bullets` (one list per job key in ORDER). Build with:

    python tools/build_resume.py --application=NAME --final
"""
FED_ANNOUNCEMENT = "ANNOUNCEMENT-NUMBER"
FED_DIR = "applications/example"
FED_HOURS_CONFIRMED = False   # set True only after you have checked every hours figure
FED_DAYS = {"vizius": (None, None)}   # (start_day, end_day); None renders as DD until you fill it
FED_HOURS = {"vizius": 40}            # hours per week per job key or employer name

FED = {
    "stem": "resume-example",
    "title": "Role title (grade)",
    "target": "Agency · Announcement number",
    "tagline": "One sentence for PDF metadata.",
    "keywords": ["keyword"],
    "summary": "Two or three sentences in your own words.",
    "highlights": ["**Handle.** One sentence of evidence per highlight, using only numbers already in EXPERIENCE."],
    "skills": [("Group", "Comma, separated, skills")],
    "publications": "Optional line.",
}
FED_BULLETS = {key: ["**Handle.** Condensed bullet."] for key in ("vibey", "vizius", "apologist", "llc", "limaone")}
FED_NOTES = {}

APPLICATIONS = {}   # name -> {"dir", "date_style", "location", "fed", "bullets"}
