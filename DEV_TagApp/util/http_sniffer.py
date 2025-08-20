import os
import socket
import datetime

from scapy.all import rdpcap, sniff, wrpcap, TCP, Raw

# Configuración
PACKAGES_DIR = "packages"
os.makedirs(PACKAGES_DIR, exist_ok=True)

def resolve_domain(domain):
    """Resuelve el dominio a una dirección IP."""
    try:
        ip = socket.gethostbyname(domain)
        print(f"[INFO] Dirección IP para {domain}: {ip}")
        return ip
    except socket.gaierror:
        print(f"[ERROR] No se pudo resolver el dominio {domain}.")
        return None

def packet_filter(packet, target_ip):
    """Filtro para capturar solo paquetes relacionados con la IP del objetivo."""
    if packet.haslayer("IP"):
        src = packet["IP"].src
        dst = packet["IP"].dst
        return src == target_ip or dst == target_ip
    return False

def save_packet(packet, domain):
    """Guarda los paquetes capturados en un archivo pcap."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pcap_file = os.path.join(PACKAGES_DIR, f"{domain}_{timestamp}.pcap")
    wrpcap(pcap_file, [packet])
    print(f"[INFO] Paquete guardado en {pcap_file}")

def main():
    domain = input("Ingrese el dominio de la página web que desea monitorear (por ejemplo, example.com): ")
    target_ip = resolve_domain(domain)
    
    if not target_ip:
        return
    
    print(f"[INFO] Sniffeando tráfico relacionado con {domain} ({target_ip})...")
    
    try:
        sniff(
            filter="ip",
            prn=lambda pkt: save_packet(pkt, domain) if packet_filter(pkt, target_ip) else None,
            store=False
        )
    except KeyboardInterrupt:
        print("\n[INFO] Sniffeo detenido por el usuario.")
    except Exception as e:
        print(f"[ERROR] Ocurrió un error: {e}")

if __name__ == "__main__":
    main()