import os, sys
from subprocess import Popen, PIPE
import shutil
from subprocess import call
import pystache

# TODO: a way to print new posts to the basic bitch software twitter account. :)

METADATA_DELIM = '---\n'

DRAFTS = "drafts"
POSTS = "site/posts"
PAGES = "site/pages"
TMP_OUTPUT = "tmp"
PAGE_SIZE = 8

if not os.path.exists(TMP_OUTPUT):
  os.makedirs(TMP_OUTPUT)

drafts = [ f for f in os.listdir(DRAFTS) if f.endswith(".md")]

entry_set = [] # list of draft dicts

# read in template for entry 
with open ('templates/entry.mustache', 'r') as mofile:
  entry_template = mofile.read()

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
    print( split_tags)
    tags_list = []
    for tag in split_tags:
      tags_list.append({ 'tag': tag}) 
    meta_dict['tags'] = tags_list

  if 'timestamp'not in meta_dict:
    print( "missing timestamp, skipping draft " + draft)
    continue

  meta_dict['filename'] = draft
  timestamp = meta_dict['timestamp']
  content = data[split_at+len(METADATA_DELIM):len(data)]

  with open(TMP_OUTPUT+"/"+timestamp, 'w+') as tmp:
    print(content, file=tmp)

  proc = Popen(['perl', 'Markdown/Markdown.pl', '--html4tags', TMP_OUTPUT + '/'+timestamp], stdout=PIPE)
  marked_down_content = proc.stdout.read().decode(sys.stdout.encoding)

  meta_dict['entry_body'] = marked_down_content

  # add processed entry to the entry set
  entry_set.append(meta_dict)

# sort the entries by timestamp
sorted_entries = sorted(entry_set, key=lambda k: k['timestamp'], reverse=True)

page_number = 0
page = '' # concatenated string of pages
for index, entry in enumerate(sorted_entries):
  if (index + 1 % PAGE_SIZE) is 0: #start a new page
    page_number++
    page = ''
  
  rendered_entry = pystache.render(entry_template, entry)
  page += rendered_entry

  # TODO: embed each post in a template with next & previous links
  with open(POSTS + '/' + entry['filename'].replace('.md', '.html'), 'w+') as out:
    print(rendered_entry, file=out)

  # todo: make a list of pages that can be printed out in a different loop
  # TODO: more link (for front page)
  # really gross. re-prints out for every entry. oh well.
  with open(PAGES+ '/page_' page_number + '.html', 'w+') as out:
    print(page, file=out)

try:
  shutil.rmtree(TMP_OUTPUT)
except OSError:
  pass
