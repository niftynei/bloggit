#˜/bin/sh

# make a new blog file, using the first arg as the title for it.

TIME=`date +%s`
DATE=`date -r $TIME "+%Y-%m-%d"`
TITLE=$1
OK_TITLE=`echo "$TITLE" | tr " " -`

echo -e "timestamp: $TIME\ndate: `date -r $TIME "+%-d %h %Y"`\ntime: `date -r $TIME "+%R"`\ntitle: $TITLE\ntags: \n\n---\n" > drafts/$DATE-$OK_TITLE.md
echo "file created: $DATE-$OK_TITLE.md"

vim + drafts/$DATE-$OK_TITLE.md
