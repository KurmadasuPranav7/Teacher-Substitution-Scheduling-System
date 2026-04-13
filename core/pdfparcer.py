import pdfplumber
import json
import re

pdf_path = "core\\teacher_tt.pdf"
all_teachers = {}
valid_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa"]

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        lines = text.split("\n")
        teacher_lines = [line.split("Teacher ") for line in lines if "Teacher" in line] 
        teacher_lines_cleaned = [teacher.strip(" ") for t in teacher_lines for teacher in t if teacher.strip()]

        tables = page.extract_tables()

        for idx, table in enumerate(tables):
            teacher_name = teacher_lines_cleaned[idx] if idx < len(teacher_lines_cleaned) else "Unknown Teacher"
            if "LAB" in teacher_name:
                continue

            subjects = set()
            classes = set()

            all_teachers[teacher_name.lower()] = {
                "schedule":{
                    day: [] for day in valid_days
                },
                "subjects": [],
                "classes": [],
                "sub_counter": 0
            }

            for row in table:
                if row[0] not in valid_days:
                    continue

                day = row[0]

                for i, period in enumerate(row[1:]):
                    period = period.strip() if period else ""
                    subject, class_name, section = None, None, None

                    if period:
                        parts = period.split("\n")
                        if len(parts) == 2:
                            subject, class_sec = parts

                            match = re.match(r"([A-Z0-9]+)([A-Z])$", class_sec)
                            if match:
                                class_name, section = match.groups()

                    if subject and class_name:
                        subjects.add(subject)
                        classes.add(class_name + section)


                    all_teachers[teacher_name.lower()]["subjects"] = list(subjects)
                    all_teachers[teacher_name.lower()]["classes"] = list(classes)

                    all_teachers[teacher_name.lower()]["schedule"][day].append({
                        "period": i+1,
                        "class": class_name,
                        "section": section,
                        "subject": subject,
                    })

with open(".\\teacher_workload.json", "w") as json_file:
    json.dump(all_teachers, json_file, indent=4)
