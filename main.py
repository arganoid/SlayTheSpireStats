import os
import time

STS_PATH = 'D:/SteamLibrary/steamapps/common/SlayTheSpire/'
ONLY_A20 = True

def scan(path):
    # key = (year,month), value = [games,wins]
    month_stats = {}

    for item in os.scandir(path):
        if item.is_file() and item.name[-4:] == '.run':
            stats = os.stat(item)
            raw_time = stats.st_mtime
            time_struct = time.localtime(raw_time)
            #display_date = time.ctime(raw_time)
            #print(display_date)
            #print(time_struct.tm_year, time_struct.tm_mon)

            with open(item.path) as f:
                text = f.read()

                if ONLY_A20 and '"ascension_level":20' not in text:
                    continue

                won = 'killed_by' not in text

                # Find entry for this month in stats or create new entry
                key = (time_struct.tm_year, time_struct.tm_mon)
                if key in month_stats:
                    entry = month_stats[key]
                    entry[0] += 1
                    if won:
                        entry[1] += 1
                else:
                    month_stats[key] = [1, 1 if won else 0]

    character = path.split("/")[-1]
    print(f"{character:10}\tWon/Runs")
    for key, value in month_stats.items():
        date_text = f"{key[0]}/{key[1]}"
        games_text = f"{value[1]}/{value[0]}"
        print(f"{date_text:10}\t{games_text:10}", end='')
        if value[0] != 0:
            percent = 100 * value[1] / value[0]
            print(f"\t{percent:.1f}%")

    if len(month_stats) == 0:
        print("No runs matching criteria")

    print()


if STS_PATH[:-1] != '/':
    STS_PATH += '/'

scan(STS_PATH + r'runs/IRONCLAD')
scan(STS_PATH + r'runs/THE_SILENT')
scan(STS_PATH + r'runs/DEFECT')
scan(STS_PATH + r'runs/WATCHER')
scan(STS_PATH + r'runs/DAILY')