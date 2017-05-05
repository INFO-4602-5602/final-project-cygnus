import json
import csv

top = 49.3457868 # north lat
left = -124.7844079 # west long
right = -66.9513812 # east long
bottom =  24.7433195 # south lat

maxDayCheckin = 19896


f_business = open('data/yelp_academic_dataset_business.json', 'r')
business_dic = {}
for line in f_business:
    data = json.loads(line)
    business_dic[data['business_id']] = data

fileObj = open('data/yelp_academic_dataset_checkin.json')

checkin_list = []

# Exclude Airport Checkins

includeList = []
with open('processedData/restaurants.csv', 'rb') as csvfile:
    spamreader = csv.DictReader(csvfile)
    #next(spamreader, None)  # skip the headers
    for row in spamreader:
        includeList.append( row['business_id'] )

print len(includeList)
for line in fileObj:
    data = json.loads(line)
    business_id = data['business_id']
    if business_id in includeList:
        business_obj = business_dic[business_id]
        lat = business_obj['latitude']
        lng = business_obj['longitude']
        dict_obj = { "Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0, "All": 0 }
        dict_obj['latitude'] = business_obj['latitude']
        dict_obj['longitude'] = business_obj['longitude']
        dict_obj['business_id'] = business_id
        countTotal = 0
        for time in data['time']:
            temp = time.split("-")
            day = temp[0]
            count = int(temp[-1].split(":")[-1])
            dict_obj[day] += count
            countTotal += count
        dict_obj['All'] = countTotal
        #if bottom <= lat <= top and left <= lng <= right:
        #        c.append((lat, lng))
        checkin_list.append(dict_obj)

print len(checkin_list)

keys = checkin_list[0].keys()
with open('processedData/checkin.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(checkin_list)

    

