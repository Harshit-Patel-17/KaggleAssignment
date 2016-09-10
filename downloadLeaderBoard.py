from __future__ import print_function
from django.utils.encoding import smart_str, smart_unicode
import pandas as pd
import csv
import urllib2
from bs4 import BeautifulSoup
import time
import operator

def parse(html):
    records = [["Rank", "Team", "Score"]]
    soup = BeautifulSoup(html)
    leaderNos = soup.findAll("td", {"class": "leader-number"})
    teamNames = soup.findAll("a", {"class": "team-link"})
    scores = soup.findAll("abbr", {"class": "score"})
    total_records = len(leaderNos)
    for i in range(total_records):
        leaderNo = smart_str(leaderNos[i].text).strip()
        teamName = smart_str(teamNames[i].text).strip()
        score = smart_str(scores[i].text).strip()
        records.append([leaderNo, teamName, score])
    return records

def getDownloadedFileNames(filename):
    with open(filename) as in_file:
        return [file.strip() for file in in_file]

url = "https://www.kaggle.com/c/digit-recognizer/leaderboard"
data_path = "KaggleAssignment/public/leaderboards/"
filename = time.strftime("%d-%b-%Y") + ".csv"
downloadedFiles = getDownloadedFileNames(data_path + "files.txt")

if(filename not in downloadedFiles):
    response = urllib2.urlopen(url)
    try:
        html = response.read()
    except Exception:
        raise
    else:
        records = parse(html)
        with open(data_path + "files.txt", "ab") as out_file:
            out_file.write(filename + "\n")
        with open(data_path + filename, "wb") as out_file:
            writer = csv.writer(out_file, delimiter='\t')
            writer.writerows(records)
    finally:
        try:
            response.close()
        except (UnboundLocalError, NameError):
            raise UnboundLocalError

scores = {}
downloadedFiles = getDownloadedFileNames(data_path + "files.txt")
total_leaderboards = len(downloadedFiles)
for file in downloadedFiles:
    leaderboard = pd.read_csv(data_path + file, delimiter="\t", skipinitialspace=True)
    for row in leaderboard.iterrows():
        team = row[1]["Team"]
        score = row[1]["Score"]
        if(team not in scores):
            scores[team] = score / total_leaderboards
        else:
            scores[team] += score / total_leaderboards

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
sorted_scores.reverse()
records = [["Rank", "Team", "Score"]]
for i in range(len(sorted_scores)):
    records.append([i] + list(sorted_scores[i]))
with open(data_path + "average.csv", "wb") as out_file:
    writer = csv.writer(out_file, delimiter='\t')
    writer.writerows(records)