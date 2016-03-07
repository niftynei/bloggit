import os, sys
from subprocess import Popen, PIPE
import shutil
from subprocess import call
import pystache
import json

# TODO: a way to print new posts to the basic bitch software twitter account. :)

METADATA_DELIM = '---\n'

BASE_URL = "//0.0.0.0:8080"
DRAFTS = "drafts"
POSTS = "site/posts"
PAGES = "site/pages"
HOME  = "site/index.html"
TMP_OUTPUT = "tmp"
PAGE_SIZE = 8

def chunk(entries, chunk_size):
  out = []
  last = 0
  
  while last < len(entries):
    out.append(entries[last:(last + chunk_size)])
    last += chunk_size

  return out

if not os.path.exists(TMP_OUTPUT):
  os.makedirs(TMP_OUTPUT)

drafts = [ f for f in os.listdir(DRAFTS) if f.endswith(".md")]

entry_set = [] # list of draft dicts

# read in template for entry 
with open ('templates/entry.mustache', 'r') as mofile:
  entry_template = mofile.read()

# read in template for home page

for draft in drafts:
  with open (DRAFTS + '/' + draft, 'r') as draftfile:
    data = draftfile.read()

  split_at = data.find(METADATA_DELIM)
  meta = data[0:split_at]

  metasplit = [item.split(':', 1) for item in filter(None, meta.split('\n'))]
  meta_dict = {}
  for line in metasplit:
    if len(line) == 2:
      meta_dict[line[0]] = line[1].strip()

  if 'tags' in meta_dict:
    split_tags = meta_dict['tags'].split(',')
    split_tags = [str.strip(x) for x in split_tags]
    tags_list = []
    for tag in split_tags:
      if (len(tag) == 0):
        continue
      tags_list.append({ 'tag': tag}) 
    meta_dict['tags'] = tags_list

  if 'timestamp'not in meta_dict:
    print( "missing timestamp, skipping draft " + draft)
    continue

  if 'time' in meta_dict:
    print("The time is " + meta_dict['time'])

  meta_dict['filename'] = draft.replace('md','html')
  meta_dict['link'] = POSTS + '/' + meta_dict['filename']
  meta_dict['permalink'] = BASE_URL + '/posts/' + meta_dict['filename']
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

# read in template for posts
with open ('templates/post.mustache', 'r') as mofile:
  post_template = mofile.read()
for index, entry in enumerate(sorted_entries):
  
  if index != 0: # if not the first item, add a prev link
    entry['prev'] = sorted_entries[index - 1]['filename']

  if index + 1 < len(sorted_entries):
    entry['next'] = sorted_entries[index + 1]['filename']

  rendered_entry = pystache.render(entry_template, entry)
  entry['rendered_entry'] = rendered_entry

  entry['escaped_entry'] = json.dumps(rendered_entry)

  post = pystache.render(post_template, entry)
  with open(POSTS + '/' + entry['filename'], 'w+') as out:
    print(post, file=out)

paged_entries = chunk(sorted_entries, PAGE_SIZE)

# read in template for pages
with open ('templates/page.mustache', 'r') as mofile:
  page_template = mofile.read()
for index, page in enumerate(paged_entries):
  
  # add a 'last' marker to the last entry in a page, so that we don't print a comma
  page[len(page) - 1]['last'] = True

  page_dict = { 'entries': page }
  # add a "more" link if there's a page after this one
  if (index + 1 < len(paged_entries)):
    page_dict['more_link'] = 'pages/page_' + str(index + 1) + '.json' 

  if (index == 0):
    # read in template for home page
    with open ('templates/home.mustache', 'r') as mofile:
      home_template = mofile.read()
    rendered_home = pystache.render(home_template, page_dict)
    with open(HOME, 'w+') as out:
      print(rendered_home, file=out)

  rendered_page = pystache.render(page_template, page_dict)
  with open(PAGES + '/page_' + str(index) + '.json', 'w+') as out:
    print(rendered_page, file=out)
  

try:
  shutil.rmtree(TMP_OUTPUT)
except OSError:
  pass


