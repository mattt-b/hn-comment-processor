Basic processing of top level comments on a HackerNews article. Designed for processing HN Who's Hiring listings.

No requirements other than Python 2. Screen clearing untested on Windows, program should still work, just noisier.

Usage:  
Get the id of the post. Pass it to the download script `python download.py <id>`. This is repeatable and will only fetch new comments on subsequent usages.

Process the posts one at a time with `python process.py <file>` (file will be `<id>.json`). Can save/delete/skip/undo. All comments will remain nicely printed in the file.
