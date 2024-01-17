from datetime import date
import calendar
from services.services_month_activities import set_new_month, set_month_activities, check_existing_month, get_activities_by_month_id
from services.services_usual_activity import getListOfUsualActivitiesByActivitiesIdGroupByDay
from functions_help import month_school_days

class MonthActivities(object):
    def __init__(self, year:int, month:int):
        self.year = int(year)
        self.month = int(month)
        
    @property
    def month_holidays_closed(self):
        print('month_holidays_closed')

    @property
    def month_calendar(self):
        return calendar.monthcalendar(self.year, self.month)
    
    @property
    def activities(self):
        return get_activities_by_month_id(self.month_id)
    
    # def month_price(self):

    def set_month(self):
        school_days = month_school_days(self.year, self.month)
        if not check_existing_month(self.year, self.month):
            self.month_id = set_new_month(self.year, self.month, len(school_days))
        else:
            self.month_id = check_existing_month(self.year, self.month)

    def set_usual_activities(self):
        for day in getListOfUsualActivitiesByActivitiesIdGroupByDay():
            for date_of_day in self.find_dates_of_day(int(day[0])):
                for activity_by_child in day[1]:
                    set_month_activities(date_of_day, activity_by_child['activity_id'], activity_by_child['child_id'], self.month_id, 1)

    def find_dates_of_day(self, week_day:int):
        day_list_of_dates = []
        for week in self.month_calendar:
            if week[week_day-1] != 0:
                day_list_of_dates.append(date(self.year, self.month, week[week_day-1]))
        return day_list_of_dates
    
    



    def set_activitiy(activity):
        print('CLASS_usual_activities', activity)

    



    