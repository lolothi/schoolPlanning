from datetime import datetime, date
import calendar
from classes.JoursFeriesClass import JoursFeries
from services_month_activities import set_new_month, set_month_activities
from services_usual_activity import getListOfUsualActivitiesByActivitiesIdGroupByDay

class MonthActivities(object):
    def __init__(self, year:int, month:int):
        self.year = int(year)
        self.month = int(month)
        self.month_id = set_new_month(self.year, self.month)
    
    def set_usual_activities(self):
        print('USUAL_activities', getListOfUsualActivitiesByActivitiesIdGroupByDay())
        for day in getListOfUsualActivitiesByActivitiesIdGroupByDay():
            activity_day = day[0]
            print('activity_day', activity_day)
            print('find_dates_of_day',self.find_dates_of_day(int(day[0])))
            for date_of_day in self.find_dates_of_day(int(day[0])):
                for activity_by_child in day[1]:
                    print('activity_by_child', activity_by_child)
                    set_month_activities(date_of_day, activity_by_child['activity_id'], activity_by_child['child_id'], self.month_id, 1)

    @property
    def month_holidays_closed(self):
        self.month_calendar()
        JoursFeriesAnneeEnCours = JoursFeries()
        return [dateJF for dateJF in JoursFeriesAnneeEnCours.to_list() if dateJF.month == self.month]

    @property
    def month_calendar(self):
        return calendar.monthcalendar(self.year, self.month)
        # print("calendar: ", month_calendar)
        # first_day_in_month = month_calendar[0].index(1)+1
        # print('first_day_in_month', Jour(first_day_in_month).name)
        # for week in month_calendar:

    def find_dates_of_day(self, week_day:int):
        day_list_of_dates = []
        for week in self.month_calendar:
            if week[week_day-1] != 0:
                day_list_of_dates.append(date(self.year, self.month, week[week_day-1]))
        return day_list_of_dates

    
    def set_activitiy(activity):
        print('CLASS_usual_activities', activity)

    



    