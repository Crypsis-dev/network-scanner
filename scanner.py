import sys
import time
import pandas as pd
from scapy.all import sniff, Dot11, Dot11ProbeReq
from bleak import BleakScanner
import asyncio
import threading
import json
from datetime import datetime

class NetworkScanner:
    def __init__(self, interface="wlan0mon"):
        self.interface = interface
        self.wifi_data = []
        self.bt_data = []
        self.running = False

    def packet_callback(self, packet):
        """Callback for Wi-Fi packet sniffing."""
        if packet.haslayer(Dot11ProbeReq):
            mac = packet.addr2
            ssid = packet.info.decode('utf-8', errors='ignore') if packet.info else "Hidden"
            signal_strength = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else "N/A"
            
            self.wifi_data.append({
                "timestamp": datetime.now().isoformat(),
                "type": "WiFi_Probe",
                "mac": mac,
                "ssid": ssid,
                "signal": signal_strength
            })
            print(f"[WiFi] Probe Request from {mac} for SSID: {ssid}")

    async def scan_bluetooth(self):
        """Asynchronous Bluetooth scanning."""
        print("[BT] Starting Bluetooth Scan...")
        while self.running:
            devices = await BleakScanner.discover()
            for d in devices:
                self.bt_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "type": "Bluetooth",
                    "mac": d.address,
                    "name": d.name or "Unknown",
                    "rssi": d.rssi
                })
                print(f"[BT] Found: {d.name} ({d.address}) RSSI: {d.rssi}")
            await asyncio.sleep(10)

    def start_wifi_sniff(self):
        """Starts Wi-Fi sniffing in a separate thread."""
        print(f"[WiFi] Starting Sniffing on {self.interface}...")
        sniff(iface=self.interface, prn=self.packet_callback, store=0, stop_filter=lambda x: not self.running)

    def start(self):
        self.running = True
        # Start WiFi thread
        wifi_thread = threading.Thread(target=self.start_wifi_sniff)
        wifi_thread.start()

        # Start Bluetooth loop
        try:
            asyncio.run(self.scan_bluetooth())
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        print("\nStopping scan and saving data...")
        self.save_data()

    def save_data(self):
        df_wifi = pd.DataFrame(self.wifi_data)
        df_bt = pd.DataFrame(self.bt_data)
        
        df_wifi.to_csv("wifi_scan_results.csv", index=False)
        df_bt.to_csv("bt_scan_results.csv", index=False)
        print("Data saved to wifi_scan_results.csv and bt_scan_results.csv")

if __name__ == "__main__":
    # Note: Requires monitor mode interface (e.g., airmon-ng start wlan0)
    iface = "wlan0mon" if len(sys.argv) < 2 else sys.argv[1]
    scanner = NetworkScanner(interface=iface)
    try:
        scanner.start()
    except KeyboardInterrupt:
        scanner.stop()
