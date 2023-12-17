import pandas as pd
import matplotlib.pyplot as plt
import datetime as date

plt.style.use("seaborn")
plt.rcParams['figure.figsize'] = (16, 9)


def getMostCommonX(colName, data, exportData, yearAddedFilter='None'):
    def buildResultDict(entry, resDict):
        if ',' in entry:
            listOfEntries = list(entry.split(','))
            for individualEntry in listOfEntries:
                if individualEntry not in resDict.keys():
                    resDict.update({individualEntry: 1})
                else:
                    resDict[individualEntry] += 1
        else:
            if entry not in resDict.keys():
                resDict.update({entry: 1})
            else:
                resDict[entry] += 1

    resultDict = {}
    for index in data.index:
        X = data[colName][index]
        if pd.isna(X):
            continue
        else:
            if yearAddedFilter == 'None':
                buildResultDict(X, resultDict)
            else:
                if data['Added At'][index][:4] == yearAddedFilter:
                    buildResultDict(X, resultDict)

    sortedDescending = sorted(resultDict.items(), key=lambda x: x[1], reverse=True)

    nameData = [name for name, occurrences in sortedDescending]
    occurrencesData = [occurrences for name, occurrences in sortedDescending]
    plt.figure()
    if colName == 'Artist Name(s)':
        if yearAddedFilter == 'None':
            plt.title(f'Most common artists')
        else:
            plt.title(f'Most common artists added in {yearAddedFilter}')
    else:
        if yearAddedFilter == 'None':
            plt.title(f'Most common {colName}')
        else:
            plt.title(f'Most common {colName} added in {yearAddedFilter}')

    if yearAddedFilter == 'None':
        plt.barh(nameData[:50][::-1], occurrencesData[:50][::-1])
    else:
        plt.barh(nameData[:10][::-1], occurrencesData[:10][::-1])
    if exportData == 1:
        if yearAddedFilter == 'None':
            plt.savefig(f"{exportFolder}/{colName}.svg", format="svg")
        else:
            plt.savefig(f"{exportFolder}/{colName}_{yearAddedFilter}.svg", format="svg")


def characteristicAnalysis(characteristic, data, exportData):
    if characteristic == 'Duration (ms)':
        data[characteristic] = data[characteristic] / (1000 * 60)
        data = data.rename(columns={'Duration (ms)': 'Duration (minutes)'})
        characteristic = 'Duration (minutes)'

    plt.figure()
    plt.hist(data[characteristic], bins=30)
    plt.title(f'{characteristic} distribution')

    average = data[characteristic].mean()
    maxChar = data[characteristic].max()
    minChar = data[characteristic].min()
    top5 = data.sort_values(by=characteristic, ascending=False).head(5)
    top5Print = top5[['Artist Name(s)', 'Track Name', characteristic]].to_string(index=False)
    bottom5 = data.sort_values(by=characteristic).head(5)
    bottom5Print = bottom5[['Artist Name(s)', 'Track Name', characteristic]].to_string(index=False)

    if exportData == 1:
        plt.savefig(f"{exportFolder}/{characteristic}.svg", format="svg")
        with open(f'{exportFolder}/{characteristic}.txt', mode='w') as file:
            file.write(f'----///---- Stats for {characteristic} ----///----\n\n\n'
                       f'Top 5:\n'
                       f'{top5Print}\n\n\n'
                       f'Bottom 5:\n'
                       f'{bottom5Print}\n\n\n'
                       f'----------------------------------------------------------------\n\n'
                       f'Max {characteristic}: {maxChar}\n'
                       f'Min {characteristic}: {minChar}\n'
                       f'Average {characteristic}: {average}\n')


def songReleaseDateDistribution(data, exportData, yearAddedFilter='None'):
    parseDateYear = lambda x: x[:4]
    songReleaseDates = []
    for idx in data.index:
        releaseDate = data['Release Date'][idx]
        if releaseDate == '0000':  # happens for nan entries
            continue
        if yearAddedFilter == 'None':
            dateToDateTimeObj = date.datetime.strptime(parseDateYear(releaseDate), '%Y')
            songReleaseDates = songReleaseDates + [dateToDateTimeObj]
        if data['Added At'][idx][:4] == yearAddedFilter:
            dateToDateTimeObj = date.datetime.strptime(parseDateYear(releaseDate), '%Y')
            songReleaseDates = songReleaseDates + [dateToDateTimeObj]

    plt.figure()
    plt.hist(songReleaseDates)
    if yearAddedFilter == 'None':
        plt.title('Song release date distribution')
        if exportData == 1:
            plt.savefig(f"{exportFolder}/songReleaseDates.svg", format="svg")

    if yearAddedFilter != 'None':
        plt.title(f'Song release date distribution for songs added in {yearAddedFilter}')
        if exportData == 1:
            plt.savefig(f"{exportFolder}/songReleaseDates_{yearAddedFilter}.svg", format="svg")


def songsAddedPerYear(data, exportData):
    parseDateYear = lambda x: x[:4]
    resultDict = {}
    for d in data['Added At']:
        yearStr = parseDateYear(d)
        if yearStr not in resultDict.keys():
            resultDict.update({yearStr: 1})
        else:
            resultDict[yearStr] += 1

    plt.figure()
    plt.bar(*zip(*resultDict.items()))
    plt.title('Amount of songs added per year')
    if exportData == 1:
        plt.savefig(f"{exportFolder}/songsAddedPerYear.svg", format="svg")


def mostActiveDays(data, exportData):
    resultDict = {}
    for x in data['Added At']:
        dateAdded = x[:10]
        if dateAdded not in resultDict.keys():
            resultDict.update({dateAdded: 1})
        else:
            resultDict[dateAdded] += 1

    sortedActiveDays = sorted(resultDict.items(), key=lambda x: x[1], reverse=True)
    activeDaysList = [name for name, occurrences in sortedActiveDays]
    activeDaysCountList = [occurrences for name, occurrences in sortedActiveDays]
    plt.figure()
    plt.title('Most active days in terms of adding songs')
    plt.barh(activeDaysList[:10][::-1], activeDaysCountList[:10][::-1])
    if exportData == 1:
        plt.savefig(f"{exportFolder}/mostActiveDays.svg", format="svg")


df = pd.read_csv('jgs_17122023.csv')
df = df.dropna(subset=['Artist Name(s)'])
firstActiveYear = int(min(df['Added At'])[:4])
lastActiveYear = int(max(df['Added At'])[:4])
yearsActive = [str(i) for i in range(firstActiveYear, lastActiveYear+1)]

export = 1
exportFolder = 'playlistAnalysis'


getMostCommonX('Artist Name(s)', df, export)
getMostCommonX('Genres', df, export)
songReleaseDateDistribution(df, export)
songsAddedPerYear(df, export)
mostActiveDays(df, export)

characteristicsList = ['Popularity', 'Duration (ms)', 'Danceability', 'Energy', 'Valence', 'Loudness', 'Tempo']
for char in characteristicsList:
    characteristicAnalysis(char, df, export)

for year in yearsActive:
    songReleaseDateDistribution(df, export, year)
    getMostCommonX('Artist Name(s)', df, export, year)
    getMostCommonX('Genres', df, export, year)
