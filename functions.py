import pytz
from datetime import datetime

def GetCurrentTime(timezone):
  timeInTimezone = pytz.timezone(timezone)
  datetime_timezone = datetime.now(timeInTimezone)
  return datetime_timezone.strftime('%Y:%m:%d %H:%M:%S')