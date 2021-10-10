from collections import Counter
from typing import List

from build_homepage_md import *


def save_lines(lines, output_dir, output_name):
    full_path = os.path.join(output_dir, output_name)
    with open(full_path, "w") as f:
        f.writelines(lines)
        print("".join(lines))
        print(f"Save at {full_path}")


def _build_cventry(sheet: Spreadsheet, tab_name: str, keys: List[str],
                   out_date_format):
    # education
    worksheet = sheet.worksheet(tab_name)
    tab = pd.DataFrame(worksheet.get_all_records())

    lines = [rf"\cvsection{{{tab_name.title()}}}", "\n" * 2]
    lines += [r"\begin{cventries}", "\n" * 2]

    for i, r in tab.iterrows():
        lines += [" " * 2, r"\cventry", "\n"]
        for ik, k in enumerate(keys):
            if ik < 3:
                _l = f"{{{getattr(r, k)}}} % {k}"
            if ik == 3:  # date
                _d = datetime.strptime(getattr(r, k), "%Y-%m-%d").strftime(out_date_format)
                _l = f"{{{_d}}} % {k}"
            else:  # bullets
                _l = f"{{{getattr(r, k)}}} % {k}" if getattr(r, k) != "" else r"{}\vspace{-1em}"
            lines += [" " * 4, _l, "\n"]

        lines.append("\n")

    lines += [r"\end{cventries}"]
    return lines


def _build_cvpubs(sheet: Spreadsheet, tab_name: str, me="Dongkwan Kim"):
    # publications, services, talks, teaching
    def _publications(df: pd.DataFrame, lines, subsec_key: str):
        subsec_counter = Counter(getattr(r, subsec_key) for i, r in df.iterrows())
        for subsec, counts in subsec_counter.items():
            lines += [rf"\cvsubsection{{{subsec.title()}}}", "\n" * 2]
            lines += [r"\begin{cvpubs}", "\n" * 2]
            for i, r in sorted(df.iterrows(), key=lambda _ir: _ir[1].date, reverse=True):

                if subsec != r.type:
                    continue

                _prefix = f"{r.type[0].upper()}{subsec_counter[r.type]}"
                subsec_counter[r.type] -= 1

                _authors = r.authors.replace(me, rf"\textbf{{{me}}}")
                _year = datetime.strptime(r.date, "%Y-%m-%d").strftime("%Y")
                _pub = rf'[{_prefix}] {_authors}. \href{{{r.paperurl}}}{{``{r.title}."}} \textit{{{r.venue}}}. {_year}'
                lines += [rf"  \cvpub{{{_pub}}}", "\n" * 2]
            lines += [r"\end{cvpubs}", "\n" * 2]

    def _talks(df: pd.DataFrame, lines, *args):
        lines += [r"\begin{cvpubs}", "\n" * 2]
        for i, r in sorted(df.iterrows(), key=lambda _ir: _ir[1].date, reverse=True):
            _presenters = r.presenters.replace(me, rf"\textbf{{{me}}}")
            _date = datetime.strptime(r.date, "%Y-%m-%d").strftime("%d %b %Y")
            _talk = rf'{_presenters}. \href{{{r.slideurl}}}{{``{r.title}."}} \textit{{{r.venue}}}. {_date}'
            lines += [rf"  \cvpub{{{_talk}}}", "\n" * 2]
        lines += [r"\end{cvpubs}"]

    def _academic_services(df: pd.DataFrame, lines, *args):
        position_and_org_to_rs = defaultdict(lambda: defaultdict(list))
        for i, r in df.iterrows():
            position_and_org_to_rs[r.position][r.organization].append(r)
        lines += [r"\begin{cvpubs}", "\n" * 2]
        for p, o_to_rs in position_and_org_to_rs.items():
            _o_ys = []
            for o, rs in o_to_rs.items():
                _years = [f"{r.year}" if r.url == "" else rf"\href{{{r.url}}}{{{r.year}}}" for r in rs]
                _o_ys.append(f"{o} ({', '.join(_years)})")
            one_line = rf"\textbf{{{p}:}} {', '.join(_o_ys)}"
            lines.append(rf"  \cvpub{{{one_line}}}" + "\n" * 2)
        lines += [r"\end{cvpubs}"]

    def _teaching_experiences(df: pd.DataFrame, lines, *args):
        course_to_rs = defaultdict(list)
        for i, r in df.iterrows():
            course_to_rs[r.course].append(r)
        lines += [r"\begin{cvpubs}", "\n" * 2]
        for c, rs in course_to_rs.items():
            positions = [r.position for r in rs]
            positions = set(positions) if len(set(positions)) == 1 else positions
            head = rf'\textbf{{{", ".join(positions)}:}}'
            semesters = ", ".join(f"{r.semester}" if r.url == ""
                                  else rf"\href{{{r.url}}}{{{r.semester}}}" for r in rs)
            notes = ", ".join(r.note for r in rs if r.note != "")
            if notes == "":
                lines += [rf"  \cvpub{{{head} {c} ({semesters})}}", "\n" * 2]
            else:
                lines += [rf"  \cvpub{{{head} {c} ({semesters}), \textit{{{notes}}}}}", "\n" * 2]
        lines += [r"\end{cvpubs}"]

    worksheet = sheet.worksheet(tab_name)
    tab = pd.DataFrame(worksheet.get_all_records())
    func_name = "_" + tab_name.replace(" ", "_")

    lines = [rf"\cvsection{{{tab_name.title()}}}", "\n" * 2]
    locals()[func_name](tab, lines, "type")
    return lines


def _build_cvhonor(sheet: Spreadsheet, tab_name: str, keys: List[str], out_date_format: str):
    # honors
    worksheet = sheet.worksheet(tab_name)
    tab = pd.DataFrame(worksheet.get_all_records())

    lines = [rf"\cvsection{{{tab_name.title()}}}", "\n" * 2]
    lines += [r"\begin{cvhonors}", "\n" * 2]

    for i, r in tab.iterrows():
        lines += [" " * 2, r"\cvhonor", "\n"]
        for ik, k in enumerate(keys):
            if k is None:
                _l = "{} % None"
            elif ik < 3:
                _l = f"{{{getattr(r, k)}}} % {k}"
            else:  # date
                _d = datetime.strptime(getattr(r, k), "%Y-%m-%d").strftime(out_date_format)
                _l = f"{{{_d}}} % {k}"
            lines += [" " * 4, _l, "\n"]

        lines.append("\n")

    lines += [r"\end{cvhonors}"]
    return lines


if __name__ == '__main__':

    __target__ = "all"
    __gsheet__ = "https://docs.google.com/spreadsheets/d/1QeeQhPYIeTiCTJNczKSfenHCYGMLf3a2vvzCor1Gd2A/"
    __dir__ = "./cv/"

    os.makedirs(__dir__, exist_ok=True)

    gc = gspread.oauth()
    sh = gc.open_by_url(__gsheet__)

    if __target__ == "education" or __target__ == "all":
        tex = _build_cventry(sh, "education",
                             keys=["degree", "institution", "location", "date", "bullets"],
                             out_date_format="%b %Y")
        save_lines(tex, __dir__, "education.tex")

    if __target__ == "publications" or __target__ == "all":
        tex = _build_cvpubs(sh, "publications")
        save_lines(tex, __dir__, "publications.tex")

    if __target__ == "talks" or __target__ == "all":
        tex = _build_cvpubs(sh, "talks")
        save_lines(tex, __dir__, "talks.tex")

    if __target__ == "services" or __target__ == "all":
        tex = _build_cvpubs(sh, "academic services")
        save_lines(tex, __dir__, "services.tex")

    if __target__ == "teaching" or __target__ == "all":
        tex = _build_cvpubs(sh, "teaching experiences")
        save_lines(tex, __dir__, "teaching.tex")

    if __target__ == "honors" or __target__ == "all":
        tex = _build_cvhonor(sh, "honors",
                             keys=["title", "organization", None, "date"],
                             out_date_format="%Y")
        save_lines(tex, __dir__, "honors.tex")
