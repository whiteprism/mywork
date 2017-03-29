HOME=/Users/zhangquanming/mywork
IP=`curl ip.cip.cc`
IPZ=`sed 'q' ip.txt`
IPL=`cat ip.txt|wc -l`
if [ !$IPL ]
then
    curl ip.cip.cc > ip.txt
fi

if [ "${IP}" != "${IPZ}" ]
then
    curl ip.cip.cc > ip.txt
    python $HOME/sendemail.py $IPZ $IP
fi

cat ip.txt
