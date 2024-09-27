from datetime import datetime, timedelta
import os
import time

STS_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/SlayTheSpire/'

ONLY_A20 = True
ONLY_THIS_YEAR = False
DAYS_FILTER = 365 * 999     # Set second number to number of years back to include

characters = ('IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER', 'DAILY')

class WinsRuns:
    def __init__(self, title: str):
        self.title = title
        self.wins = 0
        self.runs = 0

    def __str__(self):
        ratio = "--" if self.runs == 0 else f"{(self.wins / self.runs) * 100:.1f}%"
        title = f"{self.title} wins/losses/runs - ratio:"
        return f"{title:40} {self.wins}/{self.runs - self.wins}/{self.runs}\t{ratio}"


totals = WinsRuns("Total")
character_wins_runs = {c:WinsRuns(c) for c in characters}

def scan(path):
    # key = (year,month), value = [games,wins]
    month_stats = {}

    character = path.split("/")[-1]

    for item in os.scandir(path):
        if item.is_file() and item.name[-4:] == '.run':
            stats = os.stat(item)
            raw_time = stats.st_mtime
            time_struct = time.localtime(raw_time)

            if ONLY_THIS_YEAR and time_struct.tm_year != datetime.now().year:
                continue

            months_ago = datetime.now() - datetime(time_struct.tm_year, time_struct.tm_mon, time_struct.tm_mday)
            if months_ago > timedelta(days=DAYS_FILTER):
                continue

            with open(item.path) as f:
                text = f.read()

                if ONLY_A20 and '"ascension_level":20' not in text:
                    continue

                won = 'killed_by' not in text

                totals.runs += 1
                totals.wins += 1 if won else 0

                character_wins_runs[character].runs += 1
                character_wins_runs[character].wins += 1 if won else 0

                # Find entry for this month in stats or create new entry
                key = (time_struct.tm_year, time_struct.tm_mon)
                if key in month_stats:
                    entry = month_stats[key]
                    entry[0] += 1
                    if won:
                        entry[1] += 1
                else:
                    month_stats[key] = [1, 1 if won else 0]

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

for character in characters:
    scan(STS_PATH + r'runs/' + character)

print(totals)

print()

for character in characters:
    item = character_wins_runs[character]
    print(character_wins_runs[character])
