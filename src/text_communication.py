import nic_interface as nic
import time
import text_to_binary as t2bin

def initialize_communication(port):
    nic.flush()
    print(f"initializing communication, sending on port {port}")
    nic.nic_port_send("0", port)
    read_value = nic.nic_recv_from_port(port) 
    print("reading nic port values, wating for verification",end = " ")
    wait_cnt = 0
    while read_value != "0":
        read_value = nic.nic_recv_from_port(port)
        if wait_cnt%5==0: print(".",end="") 
        wait_cnt+=1
    print("\nverification received")
    return True

class Packet:
    """
    msg is any stringified binary, any conversions from text string -> binary
    or int -> binary should be done outside this class
    """
    def __init__(self, msg):
        self.bit_msg = msg 
        getbinary = lambda x, n: format(x, "b").zfill(n)
        self.header = getbinary(len(self.bit_msg), 4)
        self.header = "1" + self.header
        self.bit_msg = self.bit_msg + "0"
        self.total_msg = self.header + self.bit_msg

def send_message(port: str, message: str, sleep_time: int):
    new_packet = None
    if message == None:
        bit_sequence = "10000" # null char has a size of 0
    else:
        new_packet = Packet(message)
        bit_sequence = new_packet.total_msg
    for bit in bit_sequence:
        nic.nic_port_send(bit, port)
        time.sleep(sleep_time)
    if new_packet:
        print(new_packet.header + " " + new_packet.bit_msg)

# reads in 12 bits
def read_bit_stream(port:int, sleep_time:int):
    msg = ""
    header = ""
    time.sleep(sleep_time * 1.5)     # to get in the middle of first significant bit
    for i in range(4):  # read in header bits
        header += nic.nic_recv_from_port(port)
        time.sleep(sleep_time)
    header_size = int(header,2)
    if header_size == 0: # check for escape sequence
        return None
    for i in range(header_size):
        time.sleep(sleep_time)
        msg += nic.nic_recv_from_port(port)
    print(header + " " + msg)
    return msg

def receive_message(port, sleep_time):
    while nic.nic_recv_from_port(port) == "0":  
        continue
    bits_in_msg = read_bit_stream(port, sleep_time)          
    return t2bin.bin_to_char(bits_in_msg) if bits_in_msg else None

def listen_for_read_msgs(bit_width,port):
    msg_to_print = ""
    while True:
        received_msg = receive_message(port, bit_width)
        time.sleep(0.01) # sleep for a bit so we dont start reading a msg that isnt there
        if(received_msg != None):
            msg_to_print += received_msg
        else:
            print("\n" + msg_to_print)
            msg_to_print = ""

def listen_for_write_msgs(bit_width,port):
    while True:
        msg = input("What message would you like to send \n")
        bin_reps = t2bin.str_to_binary(msg)
        bin_reps.append(None)
        for bin_rep in bin_reps:
            send_message(port, bin_rep, bit_width)
            time.sleep(0.01)