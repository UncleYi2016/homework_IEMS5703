# Network Address Translation (NAT) Traversal Application
### Introduction
In this Mini Project, I want to implement a simple NAT traversal application. This application can help an inner-network application can be accessable. This NAT traversal application has two programs, one program needs to be set up at outer-network server, which forwards packet between client and inner-network server. The other is set up at inner-network server, which forwards packet from outer-network server to inner-network server.
### Implementation
This project will use socket to implement both server side and client side, and use log module to record all information.
### Architecture
![image](file:///Users/uncleyi/Documents/CUHK-IE/Term2/IEMS5703/homework_IEMS5703/project/Architecture.png)
As the image shows, when inner network server started, it will try to build and keep a tunnel with outer network server, and outer network server open a port to accept clients' request, once client send a request, the outer network server will send all data to inner network server, otherwise, when inner network server send a response, outer network server will send data to client too.
### Supported Connection
This project can only support TCP connection now, UDP connection is more complicated because it is connctionless protocol, it cannot keep a tunnel to send and receive data.  But if time is enough, I will still try to implement supporting UDP connection.
### Additional Function
 - Configuration File
   - This program supports configuration file to save all configuration data
 - Logging
   - The log information will be saved into a *.log file