from classes.JoursFeriesClass import JoursFeries
import calendar
from datetime import date
from vacances_scolaires_france import SchoolHolidayDates


def stringToNumber(String_number):
    return int(String_number)

def month_school_days(year, month):
    """School days by month : monday to friday"""
    business_days = month_business_days(year, month)
    public_holidays = set(month_public_holidays(year, month))
    holidays_general = set(holidays(year, month))
    holidays_dict = {day: True for day in public_holidays.union(holidays_general)}
    return [
        school_day
        for school_day in business_days
        if school_day.month == month
        and not holidays_dict.get(school_day, False)
    ]

def month_public_holidays(year, month):
    JoursFeriesAnneeEnCours = JoursFeries(year)
    return [
        dateJF
        for dateJF in JoursFeriesAnneeEnCours.to_list()
        if dateJF.month == month and dateJF
    ]


# FR : jours ouvrés
def month_business_days(year, month):
    """Business days by month : monday to friday"""
    month_business_days = []
    for week in calendar.monthcalendar(year, month):
        for day in week:
            if day != 0 and week.index(day) != 5 and week.index(day) != 6:
                month_business_days.append(date(year, month, day))
    return month_business_days

def month_days(year, month):
    public_holidays = set(month_public_holidays(year, month))
    holidays_general = set(holidays(year, month))
    # holidays_dict = {day: True for day in public_holidays.union(holidays_general)}
    month_all_days = {}
    for week in calendar.monthcalendar(year, month):
        for day in week:
            if day != 0:
                month_day = date(year, month, day)
                if month_day in public_holidays:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'public_holiday'}
                elif month_day in holidays_general:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'school_holiday'}
                elif week.index(day) != 5 and week.index(day) != 6:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'school_day'}
                else:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'off'}
    return month_all_days


def holidays(year, month, zone='A'):
    # from data.gouv.fr :
    # https://github.com/AntoineAugusti/vacances-scolaires-france
    d = SchoolHolidayDates()
    return [holiday for holiday in d.holidays_for_year_and_zone(year, zone) if holiday.month == month]
