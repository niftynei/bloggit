import os, sys
from subprocess import Popen, PIPE
import shutil
from subprocess import call

METADATA_DELIM = '---\n'

DRAFTS = "drafts"
POSTS = "site/posts"
TMP_OUTPUT = "tmp"

if not os.path.exists(TMP_OUTPUT):
  os.makedirs(TMP_OUTPUT)

drafts = [ f for f in os.listdir(DRAFTS) if f.endswith(".md")]

for draft in drafts:
  with open (DRAFTS + '/' + draft, 'r') as draftfile:
    data = draftfile.read()

  split_at = data.find(METADATA_DELIM)
  meta = data[0:split_at]

  metasplit = [item.split(':') for item in filter(None, meta.split('\n'))]
  meta_dict = {}
  for line in metasplit:
    if len(line) == 2:
      meta_dict[line[0]] = line[1].strip()

  if 'tags' in meta_dict:
    split_tags = meta_dict['tags'].split(',')
    map(str.strip, split_tags)
    tags_list = []
    for tag in split_tags:
      tags_list.append({ 'tag': tag}) 
    meta_dict['tags'] = tags_list
    print( meta_dict['tags'])

  if 'timestamp'not in meta_dict:
    print( "missing timestamp, skipping draft " + draft)
    continue

  if 'date' in meta_dict:
    date = meta_dict['date']
    print( date )

  timestamp = meta_dict['timestamp']
  content = data[split_at+len(METADATA_DELIM):len(data)]

  with open(TMP_OUTPUT+"/"+timestamp, 'w+') as tmp:
    print(content, file=tmp)

  proc = Popen(['perl', 'Markdown/Markdown.pl', '--html4tags', TMP_OUTPUT + '/'+timestamp], stdout=PIPE)
  marked_down_content = proc.stdout.read().decode(sys.stdout.encoding)

  meta_dict['entry_body'] = marked_down_content

  with open(POSTS + '/' + draft.replace('md','html'), 'w+') as out:
    print(marked_down_content, file=out)

  # TODO: embed in template & print to posts file.

# TODO: sort files in tmp chronologically, embed in template
# print to pages directory

try:
  shutil.rmtree(TMP_OUTPUT)
except OSError:
  pass
