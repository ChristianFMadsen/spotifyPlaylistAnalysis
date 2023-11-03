import csv


listOfSongs = []
with open('jgs.csv', encoding="utf8") as csvfile:
    playlist = csv.reader(csvfile)
    next(playlist) #skips header
    for row in playlist:
        song_and_artist = row[2] + ' - ' + row[4]
        if song_and_artist not in listOfSongs:
            listOfSongs.append(song_and_artist)
        elif song_and_artist in listOfSongs:
            print(f'Duplicate: {song_and_artist}')