# recursively remove all .svn dirs
find . -name .svn -print0 | xargs -0 rm -rf
