def define_years(start_year, end_year):
    """Function to define years for being independent"""
    return set([i for i in range(start_year, end_year+1)])


# Dictionary which lists all independents from 1996-present
independent_schools = {
    "Ala-Birmingham": define_years(1996, 1998),
    "Arkansas St.": define_years(1996, 1998),
    "Army": define_years(1997, 1997).union(define_years(2005, 2023)),
    "Brigham Young": define_years(2011, 2022),
    "BYU": define_years(2011, 2022),
    "Central Florida": define_years(1996, 2001),
    "Connecticut": define_years(2000, 2003).union(define_years(2020, 2025)),
    "East Carolina": {1996},
    "Idaho": {2013},
    "Louisiana": define_years(1996, 2000),
    "Louisiana Tech": define_years(1996, 2000),
    "La-Monroe": define_years(1996, 2000),
    "Liberty": define_years(2018, 2022),
    "Massachusetts": define_years(2016, 2024),
    "Middle Tennessee": define_years(1999, 2000),
    "Navy": define_years(1978, 2014),
    "New Mexico St.": {2013}.union(define_years(2018, 2022)),
    "Northern Illinois": {1996},
    "Notre Dame": define_years(1996, 2019).union(define_years(2021, 2030)),
    "South Florida": define_years(2001, 2002),
    "Temple": define_years(2005, 2006),
    "Troy": define_years(2002, 2003),
    "UAB": define_years(1996, 1998),
    "UCF": define_years(1996, 2001),
    "USF": define_years(2001, 2002),
    "Utah State": define_years(2001, 2002),
    "Western Kentucky": {2008}
}