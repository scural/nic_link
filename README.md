# nic_link
A simple multi-user chat program.

## Authors
- [scural](https://github.com/scural)
- [JamesSettles](https://github.com/JamesSettles)
- [RobertMusser](https://github.com/RobertMusser)

### Languages used
- Python

### SRC Directory
#### Packages Used
- pigpio 

#### multiuser_chat.py
This file provides threading information between the raspberry pi's, sets the bitwidth, goes through the ports, sets usernames for ports and sets reading/writing wires.

#### network_interface.py
File that creates three threads for writing and one for reading. Contains the broadcast() method which queues a message to be sent out all of the ports. Also contains a receive() method which returns queued message from any of the ports.

#### nic_interface.py
Library that provides setting up all of the receiver and transmitter ports on the pi's. Contains all the functions that receive and send information on the transmitters. Also has a flush function to reset all transmitters.

#### text_to_binary.py
Library that can turn string to binary representation, characters to binary representation, and vice versa. 

### Running The Code
To run the code, the user shoud run network_interface.py. Once the file successfully runs, the user should type their username as a character, then they can send any message they please. As other users send messages, their username and message should pop up in other monitors.

### Physical Wiring 
The topology of the network contains four messaging ports and one server port. All four of these messaging ports should be connected to the server with one reading wire and one writing wire.

### Bit Detection/Signaling
The bit sequences start with a header, continue with a message sequence and end with an ending sequence. The header is a 4 bit sequence that starts with a "1" to indicate the start and the last 3 bits indicate the size of the message. The message sequence is an 8 bit binary representation of a character in a string. The ending sequence is a "0" at the end of the bit to convey the end of the character representation. To signal the end of a string there is an escape sequence that imitates a null object in python. The escape sequence is represented as 12 bits of 0's.

