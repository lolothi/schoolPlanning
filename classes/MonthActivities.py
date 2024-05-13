from services.services_month_activities import (
    set_new_month,
    check_existing_month,
    get_activities_by_month_group_by_day,
    set_month_activity,
    get_real_activities_price_and_real_counted_activities_by_month,
)
from services.services_usual_activity import get_dict_of_usual_activities_group_by_day
from functions_help import month_days


class MonthActivities(object):
    def __init__(self, year: int, month: int):
        self.year = int(year)
        self.month = int(month)
        self.month_days_with_type_of_days = month_days(self.year, self.month)
        self.month_activities = get_activities_by_month_group_by_day(
            self.year, self.month
        )
        self.usual_activities = get_dict_of_usual_activities_group_by_day()

    @property
    def month_calendar(self):
        activitie_dict = self.month_days_with_type_of_days
        for day, activities in self.month_activities.items():
            if day in activitie_dict:
                activitie_dict[day]["activities"] = activities
        return activitie_dict

    @property
    def month_totals(self):
        (
            total_price,
            total_activities,
            total_school_canceled,
            total_family_canceled,
            total_strike_canceled,
        ) = get_real_activities_price_and_real_counted_activities_by_month(
            self.year, self.month
        )
        return {
            "price": total_price,
            "activities": total_activities,
            "school_canceled": total_school_canceled,
            "family_canceled": total_family_canceled,
            "strike_canceled": total_strike_canceled,
        }

    def set_month(self):
        month_days_filtered = {
            month_day: month_day_info
            for month_day, month_day_info in self.month_days_with_type_of_days.items()
            if month_day_info["type"] == "school_day"
        }
        if not check_existing_month(self.year, self.month):
            set_new_month(self.year, self.month, len(month_days_filtered))
        else:
            check_existing_month(self.year, self.month)

    def set_activities_from_usual_activities(self):
        for activities_day, activities in self.usual_activities.items():
            school_days_in_month_filtered = {
                month_day: month_day_info
                for month_day, month_day_info in self.month_days_with_type_of_days.items()
                if month_day_info["week_day"] == int(activities_day)
                and month_day_info["type"] == "school_day"
            }
            for month_day, activities_filtered in school_days_in_month_filtered.items():
                for activity_by_child in activities:
                    set_month_activity(
                        month_day,
                        activity_by_child["activity_id"],
                        activity_by_child["child_id"],
                    )

    def check_month_school_date(self, month_date):
        if month_date in self.month_days_with_type_of_days:
            return True
        else:
            return False
