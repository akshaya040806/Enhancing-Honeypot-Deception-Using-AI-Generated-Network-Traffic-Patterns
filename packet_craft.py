import pandas as pd
from scapy.all import IP, TCP, wrpcap, RandShort
import random
import os

def session(row, target_ip="192.168.1.100", target_port=80):
    if str(row['proto']).lower() != 'tcp':
        return []  
    packets = []

    # Fake source IP in subnet (realism)
    source_ip = f"192.168.1.{random.randint(1, 254)}"
    source_port = RandShort()
    ip_lay = IP(src=source_ip, dst=target_ip)
    tcp_seq = random.randint(1000, 4000)

    # Simulate TCP flow
    syn = ip_lay / TCP(sport=source_port, dport=target_port, flags='S', seq=tcp_seq)
    syn_ack = ip_lay / TCP(sport=source_port, dport=target_port, flags='SA', seq=tcp_seq + 1, ack=tcp_seq + 1)
    ack = ip_lay / TCP(sport=source_port, dport=target_port, flags='A', seq=tcp_seq + 1, ack=syn_ack.seq + 1)

    fake_page = random.randint(100, 999)
    payload = f"GET /page{fake_page}.html HTTP/1.1\r\nHost: honeypot\r\n\r\n"
    data_packets = ip_layer / TCP(sport=source_port, dport=target_port, flags='PA',seq=ack.seq, ack=ack.ack) / payload
    fin = ip_lay / TCP(sport=source_port, dport=target_port, flags='FA',seq=data_packets.seq + len(payload), ack=data_packets.ack)
    packets.extend([syn, syn_ack, ack, data_packet, fin])
    return packets

def main():
    csv_path = "data/synthetic.csv"         
    pcap_path = "output/traffic_for_pot.pcap"
    pot_ip = "192.168.1.100"                       

    flow_data = pd.read_csv(csv_input_path)
    tot_packets = []
    for _, row in flow_data.iterrows():
        packets = session(row, pot_ip)
        tot_packets.extend(packets)
    wrpcap(pcap_path, tot_packets)
    print(f"Saved {len(tot_packets)} packets to: {pcap_path}")

if __name__ == "__main__":
    main()
