Both proxy and web servers are written in python2.7

The proxy server runs on port 12345
Run by: python proxyserver1.py

The proxy web runs on port 20003
Run by: python server1.py

Files can be requested by using the following command on terminal:
curl -x http://localhost:12345 http://localhost:20003/1.txt

Files can be requested on browser by:
http://localhost:20003/1.txt

