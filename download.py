import copy
import HTMLParser
import json
import sys
import urllib

if len(sys.argv) != 2:
    print "Usage: python script.py <post_id>"
    exit(1)

post_id = int(sys.argv[1])

request = urllib.urlopen("https://hacker-news.firebaseio.com/v0/item/{}.json".format(post_id))
post = json.loads(request.read())

comment_ids = sorted(post['kids'], reverse=True)

try:
    comment_file = open("%d.json" % post_id, 'rw+')
    existing_data = json.load(comment_file)
except IOError:
    comment_file = open("%d.json" % post_id, 'w')
    existing_data = {'last_id': None, 'comments': {'unprocessed': [], 'deleted': [], 'saved': []}}
except ValueError:
    print "Error reading json"
    exit(1)

try:
    highest_current_id = comment_ids[0]
except IndexError:
    print "No comments"
    exit(1)

highest_previous_id = existing_data['last_id']

if highest_current_id <= highest_previous_id:
    print "No new comments"
    exit(0)

updated_data = copy.deepcopy(existing_data)
num_new_comments = 0
html_parser = HTMLParser.HTMLParser()
invalid_comments = [] # some comments return nothing from the API for unknown reason
for comment_id in comment_ids:
    if highest_previous_id is not None:
        if comment_id < highest_previous_id:
            break

    num_new_comments += 1

    print "fetching comment %d" % comment_id
    request = urllib.urlopen(
        "https://hacker-news.firebaseio.com/v0/item/{}.json".format(comment_id)
    )
    comment = json.loads(request.read())

    if comment is None:
        invalid_comments.append(comment_id)
        continue

    if comment.get('deleted'):
        continue

    updated_data['comments']['unprocessed'].append({
        'id': comment['id'],
        'text': html_parser.unescape(comment['text']),
    })

updated_data['last_id'] = highest_current_id

comment_file.seek(0)
json.dump(updated_data, comment_file, indent=4)
comment_file.truncate()

for comment_id in invalid_comments:
    print "Error on %d must check manually" % comment_id
print "%d new comments" % num_new_comments
