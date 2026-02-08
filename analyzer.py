import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_charts():
    # Load data
    wifi_file = "wifi_scan_results.csv"
    bt_file = "bt_scan_results.csv"

    if not os.path.exists(wifi_file) and not os.path.exists(bt_file):
        print("No scan data found. Please run scanner.py first.")
        return

    plt.figure(figsize=(12, 6))

    # Analyze WiFi Probes
    if os.path.exists(wifi_file):
        df_wifi = pd.read_csv(wifi_file)
        if not df_wifi.empty:
            # Chart 1: Top SSIDs requested
            plt.subplot(1, 2, 1)
            df_wifi['ssid'].value_counts().head(10).plot(kind='bar', color='skyblue')
            plt.title('Top 10 Requested SSIDs (WiFi Probes)')
            plt.xlabel('SSID')
            plt.ylabel('Frequency')

    # Analyze Bluetooth
    if os.path.exists(bt_file):
        df_bt = pd.read_csv(bt_file)
        if not df_bt.empty:
            # Chart 2: Bluetooth Signal Strength Distribution
            plt.subplot(1, 2, 2)
            sns.histplot(df_bt['rssi'], kde=True, color='salmon')
            plt.title('Bluetooth RSSI Distribution')
            plt.xlabel('RSSI (Signal Strength)')
            plt.ylabel('Count')

    plt.tight_layout()
    plt.savefig('scan_analysis_report.png')
    print("Analysis complete. Chart saved as 'scan_analysis_report.png'.")

if __name__ == "__main__":
    generate_charts()
