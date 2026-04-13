tables = page.extract_tables()
        # temp = 0

        # if i == 0:
        #     for table in tables:
        #         teacher_name = teacher_lines_cleaned[temp] if temp < len(teacher_lines_cleaned) else "Unknown Teacher"
        #         temp += 1
        #         data = {
        #             teacher_name:{
        #                 "schedule":{
        #                     "Mo":[],
        #                     "Tu":[],
        #                     "We":[],
        #                     "Th":[],
        #                     "Fr":[],
        #                     "Sa":[],
        #                 }
        #             }
        #         }

        #         for row in table:
        #             if row[0] != "Genesis School, Sangeeth Nagar, Kukatpally, Hyderabad 500072" and row[0] != "":
        #                 for i, period in enumerate(row[1:]):
        #                     period = period.strip() if period else ""
        #                     subject, class_sec = period.split("\n") if period != "" else (None, None)
        #                     data[teacher_name]["schedule"][row[0]].append({
        #                         "period": i+1,
        #                         "class": class_sec[:-1] if class_sec else None,
        #                         "section": class_sec[-1] if class_sec else None,
        #                         "subject": subject if subject else None
        #                     })

        #         with open("teacher_wordload.json", "a") as json_file:
        #             json.dump(data, json_file, indent=4)