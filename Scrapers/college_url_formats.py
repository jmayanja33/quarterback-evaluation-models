special_cases = {
    "LSU": "louisiana-state",
    "BYU": "brigham-young",
    "TCU": "texas-christian",
    "USC": "southern-california",
    "Ala-Birmingham": "alabama-birmingham",
    "La-Monroe": "louisiana-monroe"
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

    return formatted_college.lower()
