
from services.services_month_activities import set_new_month, check_existing_month, get_activities_by_month_group_by_day, set_month_activity
from services.services_usual_activity import get_dict_of_usual_activities_group_by_day
from functions_help import month_days

class MonthActivities(object):
    def __init__(self, year:int, month:int):
        self.year = int(year)
        self.month = int(month)
        self.school_days_in_month = month_days(self.year, self.month)
        self.month_activities = get_activities_by_month_group_by_day(self.year, self.month)
        self.usual_activities = get_dict_of_usual_activities_group_by_day()

    @property
    def month_calendar(self):
        activitie_dict = self.school_days_in_month
        for day, activities in self.month_activities.items():
            if day in activitie_dict: 
                activitie_dict[day]['activities'] = activities
        return activitie_dict

    def set_month(self):
        month_days_filtered = {month_day: month_day_info for month_day, month_day_info in self.school_days_in_month.items() if month_day_info['type'] == 'school_day'}
        if not check_existing_month(self.year, self.month):
            set_new_month(self.year, self.month, len(month_days_filtered))
        else:
            check_existing_month(self.year, self.month)

    def set_activities_from_usual_activities(self):
        for activities_day, activities in self.usual_activities.items():
            school_days_in_month_filtered = {month_day: month_day_info for month_day, month_day_info in self.school_days_in_month.items() if month_day_info['week_day'] == int(activities_day)}
            for month_day, activities_filtered in school_days_in_month_filtered.items() :
                for activity_by_child in activities:
                    set_month_activity(month_day, activity_by_child['activity_id'], activity_by_child['child_id'])
    
    def check_month_school_date(self, month_date):
        if month_date in self.school_days_in_month:
            return True
        else:
            return False

    



    