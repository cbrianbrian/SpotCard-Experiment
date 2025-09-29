'''

Brian C
9/29/25 - Brute force code analyzing 5 thermo couple channels on a spot card mesh. Experiment to monitor temperature
at various source heater parameters. Still a work in progress. Worked on this with intern.

'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#This Code is for a log that has 5 channels with specific names 
#AI0 - Center- F5 (°C),
#AI2 - F4 (°C),
#AI3 - E5 (°C), 
#AI5 - F6 (°C), and
#AI6 - G5 (°C)


# ***USER TO GIVE PROMPT DIRECTORY AND FILENAME ***


fn = input('Paste directory path: ')
csvname = input('Paste CSV file name to analyze (exclude ".csv"): ') 
fn = fn + "\\" + csvname + '.csv'


#fn = ''    #paste file path here to analyze if easier than prompt
    
df = pd.read_csv(fn)


ax1 = df.plot(kind='line', x='Time (s)', y='AI0 - Center- F5 (°C)', color='r', figsize = (10,5), label = 'AI0 - Center- F5 (°C)')    
ax2 = df.plot(kind='line', x='Time (s)', y='AI2 - F4 (°C)', color = 'orange', ax=ax1, label = 'AI2 - F4 (°C)')
ax3 = df.plot(kind='line', x='Time (s)', y='AI3 - E5 (°C)', color = 'deeppink', ax=ax1, label = 'AI3 - E5 (°C)')
ax4 = df.plot(kind='line', x='Time (s)', y='AI5 - F6 (°C)', color = 'green', ax=ax1, label = 'AI5 - F6 (°C)')
ax5 = df.plot(kind='line', x='Time (s)', y='AI6 - G5 (°C)', color = 'blue', ax=ax1, label = 'AI6 - G5 (°C)')

#Input temperature used and pulse duration
temp_used = input('Temperature of this pulse: ')
pulse_used = input('Duration of pulse: ')

#DICTIONARY FOR CHANNELS
channel_list = {
  1: 'AI0 - Center- F5 (°C)',
  2: 'AI2 - F4 (°C)',
  3: 'AI3 - E5 (°C)',
  4: 'AI5 - F6 (°C)',
  5: 'AI6 - G5 (°C)'
}

leftcenter = channel_list[2]
abovecenter = channel_list[3]
rightcenter = channel_list[4]
belowcenter = channel_list[5]

#ASSIGNING CENTER SPOT DATA TO VARIABLE
center_column = channel_list[1]

#CONVERT FRACTIONAL SECONDS TO SECONDS
def time_to_seconds(time_str):
    """Convert a time string in 'mm:ss' or 'mm:ss.sss' format to total seconds (float)."""
    try:
        minutes, seconds = time_str.strip().split(":")
        total_seconds = int(minutes) * 60 + float(seconds)
        return total_seconds
    except ValueError:
        raise ValueError("Input must be in 'mm:ss' or 'mm:ss.sss' format")

#BOLD TEXT
def boldtxt(txt):
    BOLD = '\033[1m'
    RESET = '\033[0m'
    print(f"{BOLD}{txt}{RESET}")


#FINDING TIME AT WHICH PULSE STARTS
pulseStartIndex = 0
for i in range(len(df[center_column]) - 1):  # stop before the last index
    if df[center_column].iloc[i+1] > df[center_column].iloc[i] + 5:
        pulseStartIndex = (df['Sample'].iloc[i])
        break

#FINDING TIME AT WHICH PULSE ENDS
pulseEndIndex = 0
for i in range(len(df[center_column]) - 1):  # stop before the last index
    if df[center_column].iloc[i+1] < df[center_column].iloc[i]-5:
        pulseEndIndex = (df['Sample'].iloc[i])
        break
filtered_df = df[df['Sample'].between(pulseStartIndex, pulseEndIndex)]



#MAX TEMP IN DATA
def maxTemp(column):
    max_index = df[column].idxmax()
    max_temp = df[column].max()
    
    return max_index, max_temp


#TIMES FOR TITLE
time1 = df["Time (s)"][pulseStartIndex-5] #5 indexes before analyzing window
time2 = df["Time (s)"][pulseEndIndex+5] #5 indexes after analyzing window

        
#PRINT DELTA TIME FOR PULSE START AND END
pulseEndTime = time_to_seconds(df["Time (s)"][pulseEndIndex])
pulseStartTime = time_to_seconds(df["Time (s)"][pulseStartIndex])
deltass = pulseEndTime - pulseStartTime
print(f"DELTA TIME BETWEEN PULSE START AND END: {deltass:.2f} sec")
print()


#TEMP DIFFEFRENCE BETWEEN PULSE START AND END
def changeInTemp(column):
    temp = float(df[column][pulseEndIndex]) - float(df[column][pulseStartIndex]) 
    return temp
deltatemp = changeInTemp(center_column)
print(f"DELTA TEMP FOR CENTER SPOT BETWEEN PULSES: {deltatemp:.2f} degC")
print()


#COOL DOWN
def coolDownDeltas(column):
    for i in df.index[df['Time (s)'] > df['Time (s)'][pulseEndIndex]]:
        if df[column][i] < df[column][pulseStartIndex-1]+3: #withing 3degC of initial rest temp
            coolDownIndex = df['Sample'][i]
            break
            
    coolDownTemp = df[column][coolDownIndex]
    coolDownTimeStamp = df['Time (s)'][coolDownIndex]
    
    coolDownDeltaTime = time_to_seconds(coolDownTimeStamp) - pulseEndTime
    coolDownDeltaTime = round(coolDownDeltaTime,2)
    
    coolDownDeltaTemp = float(df[column][pulseEndIndex]) - float(df[column][coolDownIndex])
    coolDownDeltaTemp = round(coolDownDeltaTemp,2)
    
    return coolDownDeltaTime, coolDownDeltaTemp, coolDownIndex, coolDownTemp

def coolDownDeltas1(column):
    for i in df.index[df['Time (s)'] > df['Time (s)'][pulseEndIndex]]:
        if df[column][i] < df[column][pulseStartIndex-1]+1: #withing 1degC of initial rest temp
            coolDownIndex = df['Sample'][i]
            break
            
    coolDownTemp = df[column][coolDownIndex]
    coolDownTimeStamp = df['Time (s)'][coolDownIndex]
    
    coolDownDeltaTime = time_to_seconds(coolDownTimeStamp) - pulseEndTime
    coolDownDeltaTime = round(coolDownDeltaTime,2)
    
    coolDownDeltaTemp = float(df[column][pulseEndIndex]) - float(df[column][coolDownIndex])
    coolDownDeltaTemp = round(coolDownDeltaTemp,2)
    
    return coolDownDeltaTime, coolDownDeltaTemp, coolDownIndex, coolDownTemp
    
#ANALYZING ALL COLUMNS (MAX TEMP REACHED, COOL DOWN DELTAS (TIME AND TEMP))
boldtxt('Cool Down Delta Time:'), print("Time it took channel to reach within 3degC from 'Stop Pulse'")
boldtxt('Cool Down Delta Temp: '),print("Change in Temp from 'Stop Pulse' to cool down point")
print()

pulseEndTimeStampFloat = time_to_seconds(df["Time (s)"][pulseEndIndex])

for key in (channel_list):
    cdDeltaTime = coolDownDeltas(channel_list[key])[0]
    cdDeltaTemp = coolDownDeltas(channel_list[key])[1]
    maxTempValue = maxTemp(channel_list[key])[1]
    maxTempIndex = maxTemp(channel_list[key])[0]
    maxTempTimeStamp = df["Time (s)"][maxTempIndex]
    cdDeltaTime1 = coolDownDeltas1(channel_list[key])[0]
    cdDeltaTemp1 = coolDownDeltas1(channel_list[key])[1]
    
    boldtxt(channel_list[key])
    print('CoolDownDeltaTime (3sec): ',cdDeltaTime, 'sec')
    print('CoolDownDeltaTemp (3sec): ',cdDeltaTemp, 'degC')
    
    print('CoolDownDeltaTime (1sec): ',cdDeltaTime1, 'sec')
    print('CoolDownDeltaTemp (1sec): ',cdDeltaTemp1, 'degC')
    
    print('MaxTempReached: ', maxTempValue, 'degC')
    print('MaxTemp TimeStamp: ', maxTempTimeStamp, 'sec')
    
    if maxTempIndex < pulseEndIndex:
        change = pulseEndTimeStampFloat - time_to_seconds(maxTempTimeStamp)
        change_rounded = round(change, 2)
        print('Channel reached max temp ', change_rounded,'seconds BEFORE gas pulse stopped')
    elif maxTempIndex > pulseEndIndex:
        change = time_to_seconds(maxTempTimeStamp) - pulseEndTimeStampFloat
        change_rounded = round(change, 2)
        print('Channel reached max temp ', change_rounded,'seconds AFTER gas pulse stopped')
    print()

max_index = maxTemp(center_column)[0]
max_temp = maxTemp(center_column)[1]
coolDownIndex = coolDownDeltas(center_column)[2]
coolDownTemp = coolDownDeltas(center_column)[3]

#HEAT TRANSFER PERCENTAGE
def heatTransfer(temp, roomtemp, hottest):
    temp = float(temp)
    deltaroom = temp - roomtemp
    deltamesh = hottest - roomtemp
    transfer = deltamesh / deltaroom * 100
    return transfer

BOLD = '\033[1m'
RESET = '\033[0m'

heat_transferred = heatTransfer(temp_used, df[center_column][0], max_temp)
heat_trans_rounded = round(heat_transferred,2)
print()
print(f"{BOLD}HEAT TRANSFERED FROM {temp_used}degC TEMP AND {pulse_used}sec PULSE IS {heat_trans_rounded}%{RESET}")
print()
    
#PLOT AND LEGEND 
plt.minorticks_on()
plt.xlim(pulseStartIndex-5, coolDownIndex+5)
plt.ylim(-10,200)
plt.grid(which = 'both', fillstyle = 'full', alpha=0.25)
plt.legend(fontsize=10, markerscale = 1, facecolor = 'wheat')
plt.title(f"ANALYZING {temp_used}degC FOR {pulse_used}sec PULSE FROM {time1} TO {time2}")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (degC)")

#PLOTS AT MAX
#center_column(ch1), leftcenter(ch2), abovecenter(ch3), rightcenter(ch4), belowcenter(ch5)
#channel 1
plt.scatter(df["Sample"][max_index], max_temp,color = 'red')
#plt.hlines(y=df[center_column][max_index], xmin=df['Sample'][pulseStartIndex-5], xmax=df['Sample'][coolDownIndex+5], colors=['red'], linestyles=[':'])
#plt.vlines(x=df['Sample'][max_index], ymin=-10, ymax=200, colors=['red'], linestyles=[':'])
plt.text(df["Sample"][max_index], df[center_column][max_index] - 10, 'CenterMax', 
         color='red', fontsize=10, fontweight='bold', ha='center')

#channel 2
plt.scatter(df["Sample"][maxTemp(leftcenter)[0]], maxTemp(leftcenter)[1],color = 'orange')
#plt.hlines(y=df[leftcenter][maxTemp(leftcenter)[0]], xmin=df['Sample'][pulseStartIndex-5], xmax=df['Sample'][coolDownIndex+5], colors=['orange'], linestyles=[':'])
#plt.vlines(x=df['Sample'][maxTemp(leftcenter)[0]], ymin=-10, ymax=200, colors=['orange'], linestyles=[':'])
plt.text(df["Sample"][maxTemp(leftcenter)[0]]-10, df[leftcenter][maxTemp(leftcenter)[0]] + 5, 'LeftCenterMax', 
         color='orange', fontsize=10, fontweight='bold', ha='center')

#channel 3
plt.scatter(df["Sample"][maxTemp(abovecenter)[0]], maxTemp(abovecenter)[1],color = 'deeppink')
plt.text(df["Sample"][maxTemp(abovecenter)[0]], df[abovecenter][maxTemp(abovecenter)[0]] - 15, 'AboveCenterMax', 
         color='deeppink', fontsize=10, fontweight='bold', ha='center')

#channel 4
plt.scatter(df["Sample"][maxTemp(rightcenter)[0]], maxTemp(rightcenter)[1],color = 'green')
plt.text(df["Sample"][maxTemp(rightcenter)[0]]-13, df[abovecenter][maxTemp(rightcenter)[0]], 'RightCenterMax', 
         color='green', fontsize=10, fontweight='bold', ha='center')

#channel 5
plt.scatter(df["Sample"][maxTemp(belowcenter)[0]], maxTemp(belowcenter)[1],color = 'blue')
plt.text(df["Sample"][maxTemp(belowcenter)[0]]+8, df[belowcenter][maxTemp(belowcenter)[0]] + 5, 'BelowCenterMax', 
         color='blue', fontsize=10, fontweight='bold', ha='center')

#PLOTS AT PULSE START AND END
plt.plot(df["Sample"][pulseStartIndex], df[center_column][pulseStartIndex], 'o', markersize = 5, color = 'k')
plt.hlines(y=df[center_column][pulseStartIndex], xmin=df['Sample'][pulseStartIndex-5], xmax=df['Sample'][coolDownIndex+5], colors=['k'], linestyles=[':'])
plt.vlines(x=df['Sample'][pulseStartIndex], ymin=-10, ymax=200, colors=['k'], linestyles=[':'])
plt.text(df["Sample"][pulseStartIndex], df[center_column][pulseStartIndex] + 5, 'Pulse Start', 
         color='black', fontsize=10, fontweight='bold', ha='center')

plt.plot(df["Sample"][pulseEndIndex], df[center_column][pulseEndIndex], 'o', markersize = 5, color = 'k')
plt.hlines(y=df[center_column][pulseEndIndex], xmin=df['Sample'][pulseStartIndex-5], xmax=df['Sample'][coolDownIndex+5], colors=['k'], linestyles=[':'])
plt.vlines(x=df['Sample'][pulseEndIndex], ymin=-10, ymax=200, colors=['k'], linestyles=[':'])
plt.text(df["Sample"][pulseEndIndex], df[center_column][pulseEndIndex] + 5, 'Pulse End', 
         color='black', fontsize=10, fontweight='bold', ha='center')

#PLOT AT COOL DOWN
plt.plot(df["Sample"][coolDownIndex], coolDownTemp, 'o', markersize = 7, color = 'brown')
plt.text(df["Sample"][coolDownIndex], df[center_column][coolDownIndex] + 5, 'CoolDownPoint1', 
         color='brown', fontsize=10, fontweight='bold', ha='center')


#XTICKS
df['Time (s)'] = df['Time (s)'].apply(time_to_seconds)

start_tick = max(pulseStartIndex - 5, 0)
end_tick = min(coolDownIndex + 5, len(df) - 1)
tick_step = 7

xticks = np.arange(start_tick, end_tick + 1, tick_step)
xtick_labels = df['Time (s)'].iloc[xticks].round(1).astype(str)

plt.xticks(xticks, xtick_labels, rotation=45)

#SHOW PLOT
plt.show()
