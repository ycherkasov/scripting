# add to *.tar only hidden directories
find -regex './\..*' | tar cvf ./test.tar -T -
