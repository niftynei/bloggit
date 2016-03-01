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
    meta_dict['tags'] = meta_dict['tags'].split(',')
    map(str.strip, meta_dict['tags'])
    print( meta_dict['tags'] )

  content = data[split_at+len(METADATA_DELIM):len(data)]

  with open(TMP_OUTPUT+"/tmp", 'w+') as tmp:
    print(content, file=tmp)

  proc = Popen(['perl', 'Markdown/Markdown.pl', '--html4tags', TMP_OUTPUT + '/tmp'], stdout=PIPE)
  output = proc.stdout.read().decode(sys.stdout.encoding)

  with open(POSTS + '/' + draft.replace('md','html'), 'w+') as out:
    print(output, file=out)

try:
  shutil.rmtree(TMP_OUTPUT)
except OSError:
  pass
