
from services.services_month_activities import set_new_month, check_existing_month, get_activities_by_month_group_by_day, set_month_activity
from services.services_usual_activity import get_dict_of_usual_activities_group_by_day
from services.services_off_days import get_off_days_by_month
from functions_help import month_days
from datetime import datetime

class MonthActivities(object):
    def __init__(self, year:int, month:int):
        self.year = int(year)
        self.month = int(month)
        self.month_days_with_type_of_days = month_days(self.year, self.month)
        self.month_activities = get_activities_by_month_group_by_day(self.year, self.month)
        self.usual_activities = get_dict_of_usual_activities_group_by_day()
        self.off_days = get_off_days_by_month(self.year, self.month)
        # self.off_days_set = {datetime.strptime(off_day[0], "%Y-%m-%d").date() for off_day in self.off_days}

    @property
    def month_calendar(self):
        activitie_dict = self.month_days_with_type_of_days
        for day, activities in self.month_activities.items():
            if day in activitie_dict: 
                activitie_dict[day]['activities'] = activities
        return activitie_dict

    def set_month(self):
        month_days_filtered = {month_day: month_day_info for month_day, month_day_info in self.month_days_with_type_of_days.items() if month_day_info['type'] == 'school_day'}
        if not check_existing_month(self.year, self.month):
            set_new_month(self.year, self.month, len(month_days_filtered))
        else:
            check_existing_month(self.year, self.month)

    def set_activities_from_usual_activities(self):
        # print('self.off_days: ', self.off_days)
        # off_days_dict = {off_day['date']: off_day for off_day in self.off_days}
        off_days_set = {off_day['date'] for off_day in self.off_days}
        # print('off_days_set: ', off_days_set)
        # print('Clés du dictionnaire off_days_dict :', off_days_dict.keys())
        # print('-----off_days_dict:' , off_days_dict)
        for activities_day, activities in self.usual_activities.items():
            school_days_in_month_filtered = {month_day: month_day_info for month_day, month_day_info in self.month_days_with_type_of_days.items() if month_day_info['week_day'] == int(activities_day) and month_day_info['type'] == 'school_day'}
            # print('Valeurs de month_day :', school_days_in_month_filtered.keys())
            for month_day, activities_filtered in school_days_in_month_filtered.items() :
                for activity_by_child in activities:
                    # month_day_str = month_day.strftime("%Y-%m-%d")
                    if month_day in off_days_set:
                        set_month_activity(month_day, activity_by_child['activity_id'], activity_by_child['child_id'], self.off_days['web_validated'], self.off_days['strike_canceled'], self.off_days['family_canceled'], self.off_days['school_canceled'])
                    else:
                        set_month_activity(month_day, activity_by_child['activity_id'], activity_by_child['child_id'])

    def check_month_school_date(self, month_date):
        if month_date in self.month_days_with_type_of_days:
            return True
        else:
            return False

    



    