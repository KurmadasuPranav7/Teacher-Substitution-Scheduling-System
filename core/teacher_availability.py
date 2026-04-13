import json

availability = {"Mo": {}, "Tu": {}, "We": {}, "Th": {}, "Fr": {}, "Sa": {}}

with open('teacher_wordload.json', 'r') as f:
    teachers = json.load(f)

    for teacher, details in teachers.items():
        for day, schedule in details["schedule"].items():
            for period in schedule:
                if period["subject"] is None:
                    p = period["period"]

                    if p not in availability[day]:
                        availability[day][p] = []

                    availability[day][p].append(teacher)

with open('teacher_availability.json', 'w') as f:
    json.dump(availability, f, indent=4)