# find text 'text-to-find-here' in all files
find / -type f -exec grep -H 'text-to-find-here' {} \;
