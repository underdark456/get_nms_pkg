from datetime import date
from datetime import datetime

today = date.today()
t = today.strftime("%d-%b-%Y %H:%M")

# print(datetime.strftime(t,"%d-%b-%Y %H:%M" ))
print(date.strptime("04/26/2017", '%m/%d/%Y').strftime('%Y-%m-%d'))