from __future__ import print_function
from django.utils.encoding import smart_str, smart_unicode
import pandas as pd
import csv
import urllib2
from bs4 import BeautifulSoup
import time
import operator
import sys

def getDownloadedFileNames(filename):
    with open(filename) as in_file:
        return [file.strip() for file in in_file]

root = "/home/baadalvm/KaggleAssignment/"
url = "https://www.kaggle.com/c/digit-recognizer/leaderboard"
data_path = root + "KaggleAssignment/public/leaderboards/"
teams_path = data_path + "teams.txt"
filename = time.strftime("%d-%b-%Y") + ".csv"
downloadedFiles = getDownloadedFileNames(data_path + "files.txt")

with open(teams_path) as in_file:
    teams = [smart_str(line.strip()) for line in in_file if line.strip() != ""]

def parse(html):
    records = [["Rank", "Team", "Score", "IITD_Students"]]
    soup = BeautifulSoup(html)
    leaderNos = soup.findAll("td", {"class": "leader-number"})
    teamNames = soup.findAll("a", {"class": "team-link"})
    scores = soup.findAll("abbr", {"class": "score"})
    total_records = len(leaderNos)
    for i in range(total_records):
        leaderNo = smart_str(leaderNos[i].text.strip())
        teamName = smart_str(teamNames[i].text.strip())
        score = smart_str(scores[i].text.strip())
        iitd_students = "No"
        if teamName in teams:
            iitd_students = "Yes"
        #print([leaderNo, teamName, score, iitd_students])
        records.append([leaderNo, teamName, score, iitd_students])
    return records

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
scores_percentile = {}
downloadedFiles = getDownloadedFileNames(data_path + "files.txt")
total_leaderboards = len(downloadedFiles)
for file in downloadedFiles:
    leaderboard = pd.read_csv(data_path + file, delimiter="\t", skipinitialspace=True)
    total_rows = len(leaderboard.index)
    ranks_below = total_rows - 1

    for row in leaderboard.iterrows():
        rank = row[1]["Rank"]
	team = row[1]["Team"]
        score = row[1]["Score"]
        if(team not in scores):
            scores[team] = score / total_leaderboards
            scores_percentile[team] = 1.0 * ranks_below / total_rows / total_leaderboards
        else:
            scores[team] += score / total_leaderboards
            scores_percentile[team] += 1.0 * ranks_below / total_rows / total_leaderboards
	ranks_below -= 1

sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
sorted_scores.reverse()
records = [["Rank", "Team", "Score", "IITD_Students"]]
for i in range(len(sorted_scores)):
    IITD_Students = "No"
    if(sorted_scores[i][0] in teams):
        IITD_Students = "Yes"
    records.append([i] + list(sorted_scores[i]) + [IITD_Students])
with open(data_path + "average.csv", "wb") as out_file:
    writer = csv.writer(out_file, delimiter='\t')
    writer.writerows(records)

sorted_scores_perc = sorted(scores_percentile.items(), key=operator.itemgetter(1))
sorted_scores_perc.reverse()
records = [["Rank", "Team", "Percentile_Score", "IITD_Students"]]
for i in range(len(sorted_scores_perc)):
    IITD_Students = "No"
    if(sorted_scores_perc[i][0] in teams):
        IITD_Students = "Yes"
    records.append([i] + list(sorted_scores_perc[i]) + [IITD_Students])
with open(data_path + "avg_percentile.csv", "wb") as out_file:
    writer = csv.writer(out_file, delimiter='\t')
    writer.writerows(records)
