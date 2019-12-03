from datetime import date


class Config(object):
    def __init__(self):
        self.start_day = 0
        self.start_date = date.today()

    def _set_configs(self, start_day, start_date):
        """Method to set start day."""
        self.start_day = start_day
        self.start_date = start_date
        days_list = [
            "mon",
            "tue",
            "wed",
            "thu",
            "fri",
            "sat",
            "sun",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        if isinstance(self.start_day, str):
            if self.start_day.lower() in days_list:
                self.start_day = (
                    days_list.index(self.start_day.lower())
                    if days_list.index(self.start_day.lower()) < 7
                    else days_list.index(self.start_day.lower()) - 7
                )
        # self.start_day = self.start_day
        print("Start day set to: " + str(self.start_day) + "/" + days_list[7 + self.start_day].capitalize())
        print("Start date set to: " + str(self.start_date))
        return self.start_day

    def get_configs(self):
        return self.start_day, self.start_date
