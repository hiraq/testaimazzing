import operator 
import pprint
from concurrent import futures
from processors import bank1, bank2, bank3

URL_1 = 'https://www.ocbc.com/rates/daily_price_fd.html'
URL_2 = 'https://www.dbs.com.sg/personal/rates-online/foreign-currency-fixed-deposits.page'
URL_3 = 'https://uniservices1.uobgroup.com/secure/online_rates/foreign_currency_fixed_deposits.jsp'

tasks = []
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    tasks.append(executor.submit(bank1.extract_values, URL_1))
    tasks.append(executor.submit(bank2.extract_values, URL_2))
    tasks.append(executor.submit(bank3.extract_values, URL_3))

    data = {}
    for task in futures.as_completed(tasks):
        result = task.result()
        data.update({result['host']: result['highest']})

    bank_highest_value = max(data.items(), key=operator.itemgetter(1))[0]
    print('------ Result -----')
    print('Bank with highest deposit value: {} - Value: {}'.format(bank_highest_value, data[bank_highest_value]))
    print('---------------')
    for bank, value in data.items():
        print('Bank: {} - Value: {}'.format(bank, value))
    print('---------------')