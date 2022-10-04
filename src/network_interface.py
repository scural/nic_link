import nic_interface as nic
import text_communication as tc
import threading


# if it recieves on port it must send to other ports

# create three threads for reading, one for writing
# writing thread writes to all availible ports at once
def send_messages_on_two_ports(msg,port1,port2,bit_width):
    tc.send_message(port1,msg,bit_width)
    tc.send_message(port2,msg,bit_width)
"""
Uses one thread to send out data on all ports
"""
def broadcast(msg,user_name,bit_width):
    total_msg = user_name + ": " + msg
    # split sending of msg's into two threads
    thread1 = threading.Thread(target=send_messages_on_two_ports, args=(total_msg,1,2,bit_width))
    send_messages_on_two_ports(total_msg,3,4,bit_width)
    thread1.start()
    thread1.join()


def receive(bit_width,port1,port2):
    if port2:
        thread1 = threading.Thread(target=tc.listen_for_read_msgs,args=(bit_width,port1))
        thread1.start()
    tc.listen_for_read_msgs(bit_width,port2)

    





