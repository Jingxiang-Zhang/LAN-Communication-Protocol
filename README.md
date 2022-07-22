### Introduction

After learning ad hoc networks, OSPF and RIP protocol running in router, MQTT and HTTP protocol in application layer, I was very interested in network protocols, while at that time, I was working on my graduation project. Therefore, I decided to design my own protocol, as an additional part of the graduation project. This protocol I named it LAN Communication protocol, and it use to make function call between devise, and I realize this protocol by Python. (To be honest, I should realize it by C or C++ because of the efficiency, but I was quite busy at that time. So I had to use Python)

### Background Information

In my graduation project, I need to transfer data and command between on a local area network (LAN), in order to control other devise. If the central server is a high-performance computer, while user's computer is a low-performance computer, as a user, I want to execute a heavy computational command, I will need to copy my python code into server and run it on the server side. Therefore, I wish to put the function in the server in advance, and anyone any device on LAN can call that function conveniently.

![sketch](:UN_4_GP_NP/sketch.png){:data-align="center"}

For example, in the image above, device A have a heavy computational function A, device B or C can call function A by a single line of code.

Before moving on, I have to admit that this is not a general problems. Even if many device on LAN need to transfer data each other, they could have many other solutions. But here, I just want to put forward my solution. I have already upload this in pipy, and it can be install by `pip -install LANCommunicate`

The execution sequence diagram of the protocol is shown below. When the protocol is enabled on both devices A and B, device A registers function F first. At this time, device B can receive the address of device A in the LAN and execute the function F and store it in the function table. When device B uses the call function to call F, it only needs to pass in a function name "F" and the corresponding parameters to complete the function call. 

![sequence diagram](:UN_4_GP_NP/sequence.png){:data-align="center"}

The function is non-blocking function, that is, the program can continue execution after the function is called, but the result of execution is not obtained, because it need to be execute in the other device. The 'call' function returns an exe_id as the function's execution ID number, which is used to read the results of the execution. Device B can use the 'join' method to pass in an exe_id number and block the thread until the execution of function F is complete, to ensure that device B, which calls function F, can obtain the execution result. 

Finally, the 'get' function is used to obtain the execution result, passing in the exe_id number to obtain the execution result. Note that if you use 'get' function before device A returns the result, you will get a error message indicating that the result has not been obtained.

### Details of the Protocol

There are 9 fields in this protocol:

| number | field name | meaning | values |
| :------: | :------: | :------: | :------: |
| 1 | type | protocol type | LANC |
| 2 | method | protocol method | hello, func, call, callback |
| 3 | version | current version | 0.1 |
| 4 | data | the data transfer |  |
| 5 | exe_id | function call id |  |
| 6 | args | parameter of function |  |
| 7 | kwargs | parameter of function |  |
| 8 | encrypted |  | no |
| 9 | compress |  | no |
{:data-align="center"}

- The default transport port used by the protocol is port 5127, but you can change the port number in the configuration file. 
- The protocol methods include a Hello method to notify other device its address, func method use to notify other device the function it can execute, a call method use to call a function on the other device (or can call a function in itself), and a callback method to return the result of the function's execution. 
- Data represents the specific data to be transferred, and is used only when the protocol methods are func and callback, where the func method represents the list of executable function names, and the callback method represents the result of the function execution. 
- Exe_id is used to represent the execution ID of this function. For example, when device A calls function F of device B, device A will generate an exe_id to record this process. This ID will be sent to device B when calling the call method, and an ID number will be attached when the result is returned to device A after the function is executed. Used to uniquely determine the execution process. 
- Args and kwargs represent the parameter passing of a function, which is only included in the call method to pass the parameters of the function to the called device. 
- Encrypted and compress represent data encryption type and data compression type respectively. As extensible content, this module has not been implemented in this study.
- Data is sent in JSON format to facilitate data processing.

#### Hello Method

(1) Hello method send.

After the device goes online, it broadcasts to port 5127 of all devices on the network segment every few seconds. An independent thread is used to send the packet.

(2) Hello method receive.

After receiving a Hello method packet from another device, a device compares it with the device table it maintains. If it has received the IP address of the device, it updates the time when the device sent the latest Hello packet to the IP address. If it receives the address of the device for the first time or finds that the time since the last Hello packet from the device has expired, it immediately sends a Hello packet to that device to indicate its existence and then sends a Func packet. A list of function names used to inform the device that it can execute.

After any device on the LAN goes online, it broadcasts hello packets. All devices that use LANCommunicate protocol will record the packets in their device lists and send the same hello packets and the list of functions that can be executed by themselves to the device. The device receives information from other devices as well as a list of functions that can be executed. Any two devices on the LAN can now know each other's addresses.
 
#### Func Method

(1) Func method send.

When use the register function on device A, it will broadcast the function name to the LAN. For example, when register 'add' function, it will first store 'add' function in it local service dictionary, and then broadcast 'add' function name over LAN. 

Func method is non-blocking, it will first promise the user to broadcast the function, and put it in the waiting list. It will wait 1 seconds. In this one second, if you register another function, it will store in the waiting list, and then, there will be 2 function in the waiting list. It will keep storing function name in the waiting list, until no addition function enter the list for 1 second. At this point, all function names will be sent as a list. (Here, I was inspired by TCP protocol)

(2) Func method receive.

When the protocol receives an list of function name, it adds it to the peripheral service dictionary, where the key is the function name and the value is the function execution address. When a function with the same function name is received from different devices, the execution address will be overwritten. When a function is called, the device only executes the address corresponding to the last received function name.

#### Call Method

(1) Call method send.

The Call type is used to send information about functions that need to be execute on other devices. When a user passes call a function, the protocol compares the function name with the local service list. If the function called by the user is found to be a local service function, the function is directly invoked without sending a Call packet. If executed on another device, the function parameters sent by the user are packaged into the args and kwargs entries for sending. The exe_id id is returned to the user to obtain the execution result. The exe_id is also sent to the function execution device along with the protocol packet.

(2) Call method receive.

When the protocol receives a call message, it starts a separate thread of execution, and searches the list of local services, invoke related functions, and returns the execution result of the function. The execution result is sent as callback.

#### Callback Method

(1) Callback method send.

After the function is executed by the invoked device, the execution result is packaged and sent as  type 'callback' with the value of exe_id.

(2) Callback method receive.

After receiving the data of type callback, the recipient stores it in the function call result dictionary, where the key is exe_id and the value is the return value of the function. The thread calling the function is then unblocked to ensure that the user can get the result of the function execution.

### Realize the Protocol by Python

#### Project Structure

Class inheritance diagram is shown below. NatConnector in the core part inherits the base class of data Transmit and data Receiver. The remaining class are the static module for storing static variables, the net_tools module for providing additional network functionality, and the LANException module for error handling

![class diagram](:UN_4_GP_NP/class.png){:data-align="center"}

This is the main structure of the project

![main structure](:UN_4_GP_NP/structure.png){:data-align="center"}

#### Data Packet

Here is the packet captured by wireshark:

![data packet](:UN_4_GP_NP/datagram.png){:data-align="center"}

### Extensible Function

This protocol is currently version 0.1, and there are still many imperfections part. However, due to the limitation of time, this project has not been completed, and it is summarized as follows:

- Data encryption: add a data encryption process before the final data transmission, can use the current mainstream symmetric encryption algorithm AES, or asymmetric encryption algorithm RSA
- Data compression: data is compressed and then transmitted
- Stable TCP protocol is used for data transmission. The function caller opens the idle TCP port in advance and sends the content and function call information to the function called. The function executor transmits the data of function execution through the TCP port, and then closes the TCP port
- Join the task queue after receiving the data, and then execute the data from the queue to solve the problem of high concurrency
- Add a callback function mechanism to call the call function, which can automatically call a callback function after the call is executed, so as to solve the problem that the result of function execution can only be obtained through join block
- The join function sets the maximum waiting time to prevent the process from getting stuck. When the waiting time reaches, an error is raised
- The error protocol generated after the error happened. It can be similar to ICMP
- Add loop_forever function to block forever, which is suitable for server to execute user's function exclusively
- Use multi-process, because python GIL lock mechanism, multi-threading can only use a CPU core, can only use multi-process to improve performance
- Messages can be sent to other network segments to realize function calls across network segments
- Support a function can be executed by multiple servers at the same time, only to obtain the fastest result
