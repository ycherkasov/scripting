# execute "git pull" in every dir
for dir in ~/projects/git/*
do
  (cd $dir && git pull)
done
