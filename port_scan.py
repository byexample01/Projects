#Performs a half-open port scan of a target IP address or URL.
#Uses the scapy packet manipulation tool available at https://github.com/secdev/scapy
#This tool was used on my own LAN and on scanme.nmap.org for educational purposes.
#You alone are responsible for how you use this code.

#Tested with Python v2.7.12 and scapy v2.3.3 running on a 
#Ubuntu v16.04.1 LTS virtual machine.

#For more info on port scans, see:
#https://nmap.org/book/man-port-scanning-techniques.html

#NOTE: SUPERUSER PRIVILEGES REQUIRED TO GENERATE SYN PACKETS.



from scapy.all import *

#Target IP or URL (string):
TGT_IP = "scanme.nmap.org" 

#List of common ports to scan:
TGT_PORTLIST = [21, 22, 23, 25, 53, 80, 110, 143, 443, 1433, 3306]
   
    


#-------------------------------------------------------------------------------#
#  FUNCTIONS                                                                    #
#-------------------------------------------------------------------------------#



# Gets the flag type of the first response packet in a three-way handshake.
# INPUT:  response packet (scapy packet object)
# RETURN: flag type (string); if no response, return "Nothing" (string)
def getFlag(resp):
    try:
        flag = resp.sprintf("%TCP.flags%")
    except AttributeError:
        return "Nothing"
    return flag

    
    
# Performs a half-open port scan and prints whether the target port
# is open, closed, or filtered.
# USES:   getFlag()
# INPUT:  IP address or URL of target (string), port to scan (integer)
# RETURN: None
def SYN_scan(tgt_ip, tgt_port):

    #Construct the SYN packet for half-open scanning:
    IP_layer = IP(dst=tgt_ip)
    TCP_SYN_layer = TCP(dport=tgt_port, flags="S")
    SYN_packet = IP_layer/TCP_SYN_layer
    
    #Send packet and return the first response:
    resp = sr1(SYN_packet, retry=1, timeout=1, verbose=0)

    #Print appropriate info depending on packet response type:
    output_str = "{} received back; port {} is {}."
    flag = getFlag(resp)

    if flag == "SA" or flag == "S":
        print( output_str.format(flag, tgt_port, "open") )

    elif flag == "R":
        print( output_str.format(flag, tgt_port, "closed") )

    else:
        print( output_str.format(flag, tgt_port, "filtered") )
		
        
        
        
#----------------------------------------------------------------------------------#
#  MAIN PROGRAM                                                                    #
#----------------------------------------------------------------------------------#



def main():
    print "Performing SYN scan of:", TGT_IP 
    print "\n"
    for port in TGT_PORTLIST:
        SYN_scan(TGT_IP, port)
    

if __name__ == '__main__':
    main()

    











