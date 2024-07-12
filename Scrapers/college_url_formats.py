special_cases = {
    "Ala-Birmingham": "alabama-birmingham",
    "Boston Col.": "boston-college",
    "Bowling Green": "bowling-green-state",
    "BYU": "brigham-young",
    "La-Monroe": "louisiana-monroe",
    "Louisiana": "louisiana-lafayette",
    "LSU": "louisiana-state",
    "Middle Tennessee": "middle-tennessee-state",
    "Mizzou": "missouri",
    "Ole Miss": "mississippi",
    "Pitt": "pittsburgh",
    "TCU": "texas-christian",
    "UAB": "alabama-birmingham",
    "UCF": "central-florida",
    "UNLV": "nevada-las-vegas",
    "USC": "southern-california",
    "USF": "south-florida",
    "UTEP": "texas-el-paso",
    "UTSA": "texas-san-antonio",
    "SMU": "southern-methodist",
    "Southern Miss": "southern-mississippi",
}


def format_college_for_url(college):
    """Function to format college for input in a url"""
    if college in special_cases:
        return special_cases[college]

    formatted_college = college.replace(" St.", "-state")
    formatted_college = formatted_college.replace(" ", "-")
    formatted_college = formatted_college.replace("(", "").replace(")", "")
    formatted_college = formatted_college.replace(".", "")
    formatted_college = formatted_college.replace("&", "")
    formatted_college = formatted_college.replace(",", "")
    formatted_college = formatted_college.replace("/", "")
    formatted_college = formatted_college.replace("'", "")

    return formatted_college.lower()
