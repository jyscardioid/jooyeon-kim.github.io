import os
from collections import defaultdict
from typing import List
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


def build_about(sheet: Spreadsheet, sheetname_list: List[str],
                out_dir="../_pages/about.md"):

    def _education(df: pd.DataFrame):
        for i, r in df.iterrows():
            lines.append(f"- {r.degree}, *{r.institution}*, {r.date}\n")

    def _academic_services(df: pd.DataFrame):
        position_to_rs = defaultdict(list)
        for i, r in df.iterrows():
            position_to_rs[r.position].append(r)
        for p, rs in position_to_rs.items():
            _l = []
            for r in rs:
                if r.url == "":
                    _l.append(f"{r.organization} ({r.year})")
                else:
                    _l.append(f"{r.organization} ([{r.year}]({r.url}))")
            lines.append(f"- {p}: {', '.join(_l)}\n")

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

    lines = [sheet.worksheet("about").acell("A1").value, "\n"]

    for name in sheetname_list:
        worksheet = sheet.worksheet(name)
        tab = pd.DataFrame(worksheet.get_all_records())

        if len(tab.values) > 0:
            lines.append(f"## {name.title()}\n\n")

        if name == "education":
            _education(tab)
        elif name == "academic services":
            _academic_services(tab)
        elif name == "teaching experiences":
            _teaching_experiences(tab)
        elif name == "honors":
            _honors(tab)
        elif name == "open source contributions":
            _open_source_contributions(tab)
        else:
            raise ValueError(f"Wrong name: {name}")

        if len(tab.values) > 0:
            lines.append("\n")

    open(out_dir, "w").writelines(lines)
    print("".join(lines))
    print(f"Saved at {out_dir}")


if __name__ == '__main__':

    __target__ = "all"
    __gsheet__ = "https://docs.google.com/spreadsheets/d/1QeeQhPYIeTiCTJNczKSfenHCYGMLf3a2vvzCor1Gd2A/edit#gid=0"

    gc = gspread.oauth()
    sh = gc.open_by_url(__gsheet__)

    if __target__ == "about" or __target__ == "all":
        build_about(
            sheet=sh,
            sheetname_list=["education", "academic services",
                            "teaching experiences", "honors",
                            "open source contributions"]
        )

    if __target__ == "publications" or __target__ == "all":
        build_publications(sheet=sh)

    if __target__ == "talks" or __target__ == "all":
        build_talks(sheet=sh)
