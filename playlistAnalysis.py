import pandas as pd
import matplotlib.pyplot as plt
import datetime as date

plt.style.use("seaborn")
plt.rcParams['figure.figsize'] = (16, 9)


def getMostCommonX(colName, data, exportData):
    resultDict = {}
    for index in data.index:
        X = data[colName][index]
        if pd.isna(X):
            continue
        else:
            if ',' in X:
                listOfX = list(X.split(','))
                for individualX in listOfX:
                    if individualX not in resultDict.keys():
                        resultDict.update({individualX: 1})
                    else:
                        resultDict[individualX] += 1
            else:
                if X not in resultDict.keys():
                    resultDict.update({X: 1})
                else:
                    resultDict[X] += 1

    sortedDescending = sorted(resultDict.items(), key=lambda x: x[1], reverse=True)

    nameData = [name for name, occurrences in sortedDescending]
    occurrencesData = [occurrences for name, occurrences in sortedDescending]
    plt.figure()
    if colName == 'Artist Name(s)':
        plt.title(f'Most common artists')
    else:
        plt.title(f'Most common {colName}')
    plt.barh(nameData[:50][::-1], occurrencesData[:50][::-1])
    if exportData == 1:
        plt.savefig(f"{exportFolder}/{colName}.svg", format="svg")


def characteristicAnalysis(characteristic, data, exportData):
    if characteristic == 'Duration (ms)':
        data[characteristic] = data[characteristic] / (1000 * 60)
        data = data.rename(columns={'Duration (ms)': 'Duration (minutes)'})
        characteristic = 'Duration (minutes)'

    plt.figure()
    plt.hist(data[characteristic], bins=30)
    plt.title(f'{characteristic} distribution')

    average = data[characteristic].mean()
    max = data[characteristic].max()
    min = data[characteristic].min()
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
                       f'Max {characteristic}: {max}\n'
                       f'Min {characteristic}: {min}\n'
                       f'Average {characteristic}: {average}\n')


df = pd.read_csv('jgs.csv')
df = df.dropna(subset=['Artist Name(s)'])
export = 1
exportFolder = 'playlistAnalysis'

getMostCommonX('Artist Name(s)', df, export)
getMostCommonX('Genres', df, export)

parseDateYear = lambda x: x[:4]
songsAddedPerYear = {}
for d in df['Added At']:
    year = parseDateYear(d)
    if year not in songsAddedPerYear.keys():
        songsAddedPerYear.update({year: 1})
    else:
        songsAddedPerYear[year] += 1

plt.figure()
plt.bar(*zip(*songsAddedPerYear.items()))
plt.title('Amount of songs added per year')
if export == 1:
    plt.savefig(f"{exportFolder}/songsAddedPerYear.svg", format="svg")

songReleaseDates = []
for d in df['Release Date']:
    if d == '0000':  # happens for nan entries
        continue
    dateToDateTimeObj = date.datetime.strptime(parseDateYear(d), '%Y')
    songReleaseDates = songReleaseDates + [dateToDateTimeObj]

plt.figure()
plt.title('Distribution of the release dates of the songs')
plt.hist(songReleaseDates, bins=20)
if export == 1:
    plt.savefig(f"{exportFolder}/songReleaseDates.svg", format="svg")

charateristicsList = ['Popularity', 'Duration (ms)', 'Danceability', 'Energy', 'Valence', 'Loudness', 'Tempo']
for char in charateristicsList:
    characteristicAnalysis(char, df, export)
