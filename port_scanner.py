import socket
from concurrent.futures import ThreadPoolExecutor

TARGET = input("Enter IP address or hostname: ").strip()
START_PORT = int(input("Start port: "))
END_PORT = int(input("End port: "))

open_ports = []

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        result = sock.connect_ex((TARGET, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Unknown"

            print(f"[OPEN] {port}/tcp ({service})")
            open_ports.append((port, service))

        sock.close()

    except Exception as e:
        print(f"Error on port {port}: {e}")

print(f"\nScanning {TARGET}...\n")

with ThreadPoolExecutor(max_workers=100) as executor:
    list(executor.map(scan_port, range(START_PORT, END_PORT + 1)))

print("\n===== Scan Complete =====")

if open_ports:
    for port, service in sorted(open_ports):
        print(f"{port}/tcp - {service}")
else:
    print("No open ports found.")