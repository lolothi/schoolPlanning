from datetime import date
import calendar
from services.services_month_activities import set_new_month, set_month_activity, check_existing_month, get_activities_by_month
from services.services_usual_activity import getListOfUsualActivitiesByActivitiesIdGroupByDay
from functions_help import month_school_days

class MonthActivities(object):
    def __init__(self, year:int, month:int):
        self.year = int(year)
        self.month = int(month)
        self.school_days_in_month = month_school_days(self.year, self.month)

    @property
    def month_calendar(self):
        return calendar.monthcalendar(self.year, self.month)
    
    @property
    def activities(self):
        return get_activities_by_month(self.year, self.month)

    def set_month(self):
        if not check_existing_month(self.year, self.month):
            set_new_month(self.year, self.month, len(self.school_days_in_month))
        else:
            check_existing_month(self.year, self.month)

    def set_usual_activities(self):
        for day in getListOfUsualActivitiesByActivitiesIdGroupByDay():
            for date_of_day in self.find_dates_of_day(int(day[0])):
                if date_of_day in self.school_days_in_month:
                    for activity_by_child in day[1]:
                        set_month_activity(date_of_day, activity_by_child['activity_id'], activity_by_child['child_id'], self.month_id, 1)

    def find_dates_of_day(self, week_day:int):
        """Find all the dates in month for one day (monday, tuesday ...)"""
        day_list_of_dates = []
        for week in self.month_calendar:
            if week[week_day-1] != 0:
                day_list_of_dates.append(date(self.year, self.month, week[week_day-1]))
        return day_list_of_dates
    
    def check_month_school_date(self, month_date):
        if month_date in self.school_days_in_month:
            return True
        else:
            return False

    



    