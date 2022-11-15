from fitparse import FitFile
fit_file = FitFile(r"C:\Users\Ben Coremans\Downloads\xkupqkzuzfxann3u.fit")

power = []
for record in fit_file.get_messages("record"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:
        # Print the name and value of the data (and the units if it has any)
        if data.name == 'power':
            #print(data.value)
            if data.value == 0 or data.value > 250:
                #print("value low")
                power.append(190)
                dddd=0
            else:
                power.append(data.value)



print(power)            

import statistics

statistics.median(power)
statistics.mean(power)