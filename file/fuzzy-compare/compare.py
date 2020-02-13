# I have a list of files locally and remote. I would like to delete
# the local file, if it has a closely matching remote file.
# For each local file, check the list of remote files. If there is a match
# over a certain threshold, add it to the list.

from pandas      import pandas as pd
from fuzzywuzzy  import fuzz

pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', True)
pd.set_option('max_colwidth', 100)

local = pd.read_csv("local")
remote = pd.read_csv("remote")

def fmatch(local, remotes):
  max_score = -1
  max_name = ""
  for remote in remotes.itertuples():
    score = fuzz.ratio(local, remote)
    if (score > max_score):
      max_score = score
      max_name = remote

  return {'local': file[1], 'remote': max_name[1], 'score': max_score}

matches = []

for file in local.itertuples():
  match = fmatch(file, remote)
  matches.append(match)

common = pd.DataFrame(matches)
common = common[common['score'] > 89]

for local in common.itertuples():
  print('rm -rf "/Volumes/movie/{0}"'.format(local[1]))


