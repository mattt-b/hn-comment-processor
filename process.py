import copy
import json
import sys


if len(sys.argv) != 2:
    print "Usage: python script.py <file_to_process>"
    exit(1)

try:
    comment_file = open(sys.argv[1], 'rw+')
    existing_data = json.load(comment_file)
except IOError:
    print "Error opening file %s" % sys.argv[1]
    exit(1)

updated_data = copy.deepcopy(existing_data)

prev_commands = []
while True:
    try:
        comment = updated_data['comments']['unprocessed'].pop()
    except IndexError:
        break

    print '\033[2J'
    print comment['text'].replace('<p>', '\n\n')
    print
    print "https://news.ycombinator.com/item?id={}".format(comment['id'])

    command = ""
    while command not in ['s', 'd', 'p', 'u', 'f']:
        command = raw_input("(S)ave, (D)elete, (P)ass, (U)ndo, (F)inish: ").lower().strip()

    if command == 's':
        updated_data['comments']['saved'].append(comment)
        prev_commands.append(command)
    elif command == 'd':
        updated_data['comments']['deleted'].append(comment)
        prev_commands.append(command)
    elif command == 'p':
        updated_data['comments']['unprocessed'].insert(0, comment)
        prev_commands.append(command)

    elif command == 'u':
        updated_data['comments']['unprocessed'].append(comment)

        try:
            prev_command = prev_commands.pop()
        except IndexError:
            prev_command = None
        if prev_command == 's':
            undo_comment = updated_data['comments']['saved'].pop()
        elif prev_command == 'd':
            assert(prev_command == 'd')
            undo_comment = updated_data['comments']['deleted'].pop()
        elif prev_command == 'p':
            undo_comment = updated_data['comments']['unprocessed'].pop(0)
        else:
            assert(prev_command is None)
            continue

        updated_data['comments']['unprocessed'].append(undo_comment)

    elif command == 'f':
        updated_data['comments']['unprocessed'].append(comment)
        break

comment_file.seek(0)
json.dump(updated_data, comment_file, indent=4)
comment_file.truncate()

print "Total-"
print "Remaining: {}, Saved: {}, Deleted: {}".format(
    len(updated_data['comments']['unprocessed']),
    len(updated_data['comments']['saved']),
    len(updated_data['comments']['deleted']),
)
print "Session-"
print "Processed: {} Saved: {} Deleted: {}".format(
    len(existing_data['comments']['unprocessed'])
    - len(updated_data['comments']['unprocessed']),
    len(updated_data['comments']['saved'])
    - len(existing_data['comments']['saved']),
    len(updated_data['comments']['deleted'])
    - len(existing_data['comments']['deleted']),
)
