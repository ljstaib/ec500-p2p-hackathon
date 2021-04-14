# EC500 P2P Hackathon - Spring 2021
## Created by:
- Luke Staib, ljstaib@bu.edu
- Brian Xu, brianxu@bu.edu
- Rahul Rajaram, rrajaram@bu.edu

## Overview

For this hackathon, we created a peer to peer chat application which uses the command line. Our repository has two files: "clientP2P.py" and "serverP2P.py". The only difference between the two is that one user binds a socket and the second user connects to that socket ("serverP2P.py" binds the socket and "clientP2P.py" connects). We use Python sockets to connect between each user and MongoDB to store messages locally and store name/IP combinations in MongoDB Atlas.

## Design

### Discovery

#### Centralized MongoDB Atlas

#### Auto updating IPV4
Since the public IPv4 of a user updates periodically, we use http://ip.jsontest.com/ to retrieve the current IPv4 of that user. A user's IPv4 is updated and saved in our MongoDB Atlas database.

### P2P Messaging

#### Local Message Storage

#### Python Sockets for P2P Transfer
