import os
from collections import defaultdict
import re

import gspread
import pandas as pd
from gspread import Spreadsheet


def _build_md_files(sheet: Spreadsheet, name: str, output_dir):
    worksheet = sheet.worksheet(name)
    tab = pd.DataFrame(worksheet.get_all_records())
    for i, r in tab.iterrows():
        ym = re.compile(r"\d\d\d\d-\d\d").search(r.date).group()
        sv = re.compile(r"\((.*?)\)").search(r.venue).group(1)
        file_name = f"{ym}-{sv.replace(' ', '-').lower()}.md"
        file_path = os.path.join(output_dir, file_name)

        kv = [f"{k}: '{v}'\n" for k, v in r.items() if k != "contents" and not k.endswith("url")]
        urls = [f"{k}: '{v}'\n" for k, v in r.items() if k.endswith("url") and v != ""]
        lines = ["---\n", *kv, *urls, "---\n\n"]
        if hasattr(r, "contents"):
            lines.append(r.contents)
        with open(file_path, "w") as f:
            f.writelines(lines)
            print("".join(lines))
            print(f"Saved at {file_path}")


def build_publications(sheet: Spreadsheet, output_dir="../_publications/"):
    _build_md_files(sheet, "publications", output_dir)


def build_talks(sheet: Spreadsheet, output_dir="../_talks/"):
    _build_md_files(sheet, "talks", output_dir)


def build_about(sheet: Spreadsheet, out_dir="../_pages/about.md"):

    def _education(df: pd.DataFrame):
        for i, r in df.iterrows():
            lines.append(f"- {r.degree}, *{r.institution}*, {r.date}\n")

    def _academic_services(df: pd.DataFrame):
        position_and_org_to_rs = defaultdict(lambda: defaultdict(list))
        for i, r in df.iterrows():
            position_and_org_to_rs[r.position][r.organization].append(r)
        for p, o_to_rs in position_and_org_to_rs.items():
            _o_ys = []
            for o, rs in o_to_rs.items():
                _years = [f"{r.year}" if r.url == "" else f"[{r.year}]({r.url})" for r in rs]
                _o_ys.append(f"{o} ({', '.join(_years)})")
            lines.append(f"- {p}: {', '.join(_o_ys)}\n")

    def _teaching_experiences(df: pd.DataFrame):
        course_to_rs = defaultdict(list)
        for i, r in df.iterrows():
            course_to_rs[r.course].append(r)
        for c, rs in course_to_rs.items():
            head = ", ".join(f"{r.position} ({r.semester})" for r in rs)
            course = f"of {c}"
            codes = "/".join(f"{r.code}" if r.url == "" else f"[{r.code}]({r.url})" for r in rs)
            notes = ", ".join(r.note for r in rs if r.note != "")
            notes = notes if notes == "" else f"({notes})"
            lines.append(" ".join(["-", head, course, codes, notes, "\n"]))

    def _honors(df: pd.DataFrame):
        for i, r in df.iterrows():
            if r.url == "":
                lines.append(f"- {r.title}, *{r.organization}*, {r.date}\n")
            else:
                lines.append(f"- [{r.title}]({r.url}), *{r.organization}*, {r.date}\n")

    def _open_source_contributions(df: pd.DataFrame):
        for i, r in df.iterrows():
            lines.append(f"- [{r.title}]({r.url})\n")

    lines = []

    about = pd.DataFrame(sheet.worksheet("about").get_all_records())
    for idx, about_row in about.iterrows():

        if about_row.use == "FALSE":
            continue

        elif about_row.type == "text":
            lines += [about_row.content, "\n" * 2]

        elif about_row.type == "sheet":
            name: str = about_row.content
            worksheet = sheet.worksheet(name)
            tab = pd.DataFrame(worksheet.get_all_records())

            if len(tab.values) > 0:
                lines.append(f"## {name.title()}\n\n")
                func_name = "_" + name.replace(" ", "_")
                locals()[func_name](tab)
                lines.append("\n")

        else:
            raise ValueError

    open(out_dir, "w").writelines(lines)
    print("".join(lines))
    print(f"Saved at {out_dir}")


if __name__ == '__main__':

    __target__ = "all"
    __gsheet__ = "https://docs.google.com/spreadsheets/d/1QeeQhPYIeTiCTJNczKSfenHCYGMLf3a2vvzCor1Gd2A/edit#gid=0"

    gc = gspread.oauth()
    sh = gc.open_by_url(__gsheet__)

    if __target__ == "about" or __target__ == "all":
        build_about(sheet=sh)

    if __target__ == "publications" or __target__ == "all":
        build_publications(sheet=sh)

    if __target__ == "talks" or __target__ == "all":
        build_talks(sheet=sh)
