import os
import socket
import datetime

from scapy.all import rdpcap, sniff, wrpcap, TCP, Raw

# Cargar el archivo PCAP
pcap_file_path = "packages\\prod-gen.rjcfactura17.com_20250107_110005.pcap"
packets = rdpcap(pcap_file_path)

# Buscar paquetes HTTP
http_requests = []
for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load
        if b"HTTP" in payload:
            http_requests.append(payload.decode(errors="ignore"))

# Guardar las solicitudes HTTP en un archivo para revisión
with open("http_requests.txt", "w", encoding="utf-8") as f:
    for request in http_requests:
        f.write(request + "\n\n")

print(f"Se extrajeron {len(http_requests)} solicitudes HTTP.")