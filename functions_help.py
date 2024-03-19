from classes.JoursFeriesClass import JoursFeries
import calendar
from datetime import date, datetime
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
                # month_day_ts = datetime(year, month, day).timestamp()
                if month_day in public_holidays:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'public_holiday'}
                elif month_day in holidays_general:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'school_holiday'}
                elif week.index(day) != 5 and week.index(day) != 6:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'school_day'}
                else:
                    month_all_days[month_day] = {'week_day': week.index(day)+1, 'type': 'off'}
    print('--month_all_days: ', month_all_days)
    return month_all_days


def holidays(year, month, zone='A'):
    # from data.gouv.fr :
    # https://github.com/AntoineAugusti/vacances-scolaires-france
    d = SchoolHolidayDates()
    return [holiday for holiday in d.holidays_for_year_and_zone(year, zone) if holiday.month == month]


def calculate_real_activities_in_month(
    total_activities,
    activity_price,
    total_price,
    school_canceled,
    family_canceled,
    strike_canceled,
):
    if school_canceled >= 1 or family_canceled >= 1 or strike_canceled >= 1:
        real_total_price = total_price - (
            (school_canceled + family_canceled + strike_canceled) * activity_price
        )
        real_total_activities = total_activities - (
            school_canceled + family_canceled + strike_canceled
        )
    else:
        real_total_price = total_price
        real_total_activities = total_activities
    return {
        "real_total_price": real_total_price,
        "real_total_activities": real_total_activities,
    }