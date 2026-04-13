import json

target_day = "Mo"
teacher_on_leave = ["tv neelima"]
classes_to_cover = []
assigned_today = []

with open('substitution_log.json', 'r') as f:
    log = json.load(f)

with open('teacher_availability.json', 'r') as f:
    availability = json.load(f)

with open('teacher_wordload.json', 'r') as f:
    teachers = json.load(f)

avg = sum(t["sub_counter"] for t in teachers.values()) / len(teachers)

for teacher in teacher_on_leave:
    for period in teachers[teacher]["schedule"][target_day]:
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

    candidate_teachers = availability[target_day].get(str(period), [])
        
    for teacher in candidate_teachers:
        if teacher.lower() in teacher_on_leave:
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
            prev_teachers = availability[target_day].get(str(prev_period), [])
            if teacher in prev_teachers:
                score -= 10

        penalty = teacher_data["sub_counter"] - avg

        score -= penalty * 5
            
        scores.append((teacher, score, {
            "same_subject": subject in teacher_subjects,
            "same_class": class_name + section in teacher_classes
        }))

    scores.sort(key=lambda x: x[1], reverse=True)

    if scores:
        best_teacher = scores[0][0]
        teachers[best_teacher]["sub_counter"] += 1
        avg = sum(t["sub_counter"] for t in teachers.values()) / len(teachers)
        assigned_today.append(best_teacher)

        print({
            "assigned_teacher": best_teacher,
            "class": f"{class_name}{section}",
            "subject": subject,
            "period": period,
            "top_candidates": scores[:3]
        }, end="\n\n")

        log[f"{class_name}{section}_{subject}_{period}"] = {
            "assigned_teacher": best_teacher,
            "class": f"{class_name}{section}",
            "subject": subject,
            "period": period,
            "top_candidates": scores[:3]
        }
    else:
        print("No teacher available (all busy)")

with open('teacher_wordload.json', 'w') as f:
    json.dump(teachers, f, indent=4)

with open('substitution_log.json', 'w') as f:
    json.dump(log, f, indent=4)