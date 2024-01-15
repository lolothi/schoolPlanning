from classes.JoursFeriesClass import JoursFeries
import calendar
from datetime import date
from vacances_scolaires_france import SchoolHolidayDates


def stringToNumber(String_number):
    return int(String_number)


def month_school_days(year, month):
    business_days = month_business_days(year, month)
    # print('business_days', business_days)
    holidays_closed = set(month_holidays_closed(year, month))
    print('holidays_closed', holidays_closed)
    holidays_general = set(holidays(year, month))
    print('holidays_general', holidays_general)
    holidays_dict = {day: True for day in holidays_closed.union(holidays_general)}
    print('holidays_dict',holidays_dict)
    return [
        school_day
        for school_day in business_days
        if school_day.month == month
        and not holidays_dict.get(school_day, False)
    ]


def month_holidays_closed(year, month):
    JoursFeriesAnneeEnCours = JoursFeries(year)
    return [
        dateJF
        for dateJF in JoursFeriesAnneeEnCours.to_list()
        if dateJF.month == month and dateJF
    ]


# FR : jours ouvrés
def month_business_days(year, month):
    month_business_days = []
    print('calendar: ', calendar.monthcalendar(year, month))
    for week in calendar.monthcalendar(year, month):
        for day in week:
            if day != 0 and week.index(day) != 5 and week.index(day) != 6:
                month_business_days.append(date(year, month, day))
    return month_business_days


def holidays(year, month):
    # from data.gouv.fr :
    # https://github.com/AntoineAugusti/vacances-scolaires-france
    d = SchoolHolidayDates()
    return [holiday for holiday in d.holidays_for_year_and_zone(year, 'A') if holiday.month == month]
