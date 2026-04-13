import json

def generate_substitutions(day, teachers_on_leave):

    with open('teacher_availability.json') as f:
        availability = json.load(f)

    with open('teacher_workload.json') as f:
        teachers = json.load(f)

    assignments = []
    assigned_today = []
    leave_teachers = [
    t for t in teachers if t.lower() in [x.lower() for x in teachers_on_leave]
    ]


    avg = sum(t["sub_counter"] for t in teachers.values()) / len(teachers)

    classes_to_cover = []

    for teacher in leave_teachers:
        for period in teachers[teacher]["schedule"][day]:
            if period["subject"] is not None:
                classes_to_cover.append({
                    "period": period["period"],
                    "class": period["class"],
                    "section": period["section"],
                    "subject": period["subject"]
                })

    for cls in classes_to_cover:
        scores = []

        period = cls["period"]
        subject = cls["subject"]
        section = cls["section"]
        class_name = cls["class"]

        candidates = availability[day].get(str(period), [])

        for teacher in candidates:

            if teacher in leave_teachers:
                continue

            teacher_data = teachers[teacher]
            teacher_subjects = teacher_data["subjects"]
            teacher_classes = teacher_data["classes"]

            score = 0

            if subject in teacher_subjects:
                score += 40

            if class_name + section in teacher_classes:
                score += 50

            if any(c.startswith(class_name) for c in teacher_classes):
                score += 10

            if teacher in assigned_today:
                score -= 20

            prev_period = period - 1
            if prev_period > 0:
                prev_teachers = availability[day].get(str(prev_period), [])
                if teacher in prev_teachers:
                    score -= 10

            penalty = teacher_data["sub_counter"] - avg
            score -= penalty * 5

            scores.append((teacher, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        if scores:
            best_teacher = scores[0][0]

            teachers[best_teacher]["sub_counter"] += 1
            assigned_today.append(best_teacher)

            assignments.append({
                "class": f"{class_name}{section}",
                "subject": subject,
                "period": period,
                "assigned_teacher": best_teacher,
                "score": scores[0][1]
            })

    # save updated counts
    with open('teacher_workload.json', 'w') as f:
        json.dump(teachers, f, indent=4)

    return assignments