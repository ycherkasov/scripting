apt-get --assume-yes update
apt-get --assume-yes install build-essential g++ python-dev python3-dev autotools-dev libicu-dev build-essential libbz2-dev cmake
wget -O boost_1_61_0.tar.gz http://sourceforge.net/projects/boost/files/boost/1.61.0/boost_1_61_0.tar.gz/download
tar xzvf boost_1_61_0.tar.gz
cp project-config.jam boost_1_61_0/
cd boost_1_61_0/
./bootstrap.sh --prefix=/usr/local
n=`cat /proc/cpuinfo | grep "cpu cores" | uniq | awk '{print $NF}'`
./b2 --with=all -j $n install
sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/local.conf'
ldconfig


