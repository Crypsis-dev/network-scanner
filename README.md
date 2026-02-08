# Network Scanner and Analyzer

This repository contains a Python-based tool designed to scan and analyze nearby Bluetooth and Wi-Fi network packets. It helps in understanding network activity in a given area, which can be useful for bug reporting, security analysis, and general network monitoring. The tool captures Wi-Fi probe requests and Bluetooth device advertisements, then processes this data to generate insightful charts.

## Features

*   **Wi-Fi Packet Sniffing**: Captures Wi-Fi probe requests to identify nearby SSIDs and MAC addresses.
*   **Bluetooth Device Scanning**: Discovers Bluetooth devices and their signal strengths.
*   **Data Storage**: Saves captured data into CSV files for further analysis.
*   **Data Visualization**: Generates charts (e.g., top SSIDs, Bluetooth RSSI distribution) to visualize network activity.

## Prerequisites

To run this tool, you will need:

*   **Python 3.x**: The scripts are written in Python.
*   **Network Interface in Monitor Mode**: For Wi-Fi sniffing, your wireless adapter must support monitor mode. Tools like `airmon-ng` (part of Aircrack-ng suite) can be used to set this up.
*   **Bluetooth Adapter**: A functional Bluetooth adapter for scanning Bluetooth devices.
*   **Root Privileges**: Packet sniffing often requires root privileges.

### Required Python Libraries

Install the necessary Python libraries using pip:

```bash
pip install -r requirements.txt
```

## Setup and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Crypsis-dev/network-scanner.git
cd network-scanner
```

### 2. Install Dependencies

```bash
sudo pip install -r requirements.txt
```

### 3. Prepare Wi-Fi Interface (Monitor Mode)

Before running the Wi-Fi scanner, you need to put your wireless interface into monitor mode. Replace `wlan0` with your actual wireless interface name.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

This will typically create a new monitor interface, often named `wlan0mon`. You will use this interface name when running the scanner.

### 4. Run the Network Scanner

Execute the `scanner.py` script. You can specify your monitor interface as an argument. If not specified, it defaults to `wlan0mon`.

```bash
sudo python3 scanner.py wlan0mon
```

The script will start sniffing Wi-Fi probe requests and scanning for Bluetooth devices. It will run until you stop it manually by pressing `Ctrl+C`.

### 5. Analyze the Data

After stopping the scanner, the captured data will be saved into `wifi_scan_results.csv` and `bt_scan_results.csv`. You can then run the `analyzer.py` script to generate visualizations:

```bash
python3 analyzer.py
```

This will generate a `scan_analysis_report.png` file containing charts of the scanned data.

## Understanding the Output

*   **`wifi_scan_results.csv`**: Contains timestamps, MAC addresses of devices sending probe requests, and the SSIDs they are looking for.
*   **`bt_scan_results.csv`**: Contains timestamps, MAC addresses, names, and RSSI (Received Signal Strength Indicator) of discovered Bluetooth devices.
*   **`scan_analysis_report.png`**: A visual report showing insights like the most frequently requested SSIDs and the distribution of Bluetooth signal strengths.

## Limitations and Considerations

*   **Range**: The effective scanning range for both Wi-Fi and Bluetooth is highly dependent on your hardware, environmental factors, and local regulations. While the request mentioned 300-500m, typical consumer-grade hardware will have a significantly shorter practical range.
*   **Passive Sniffing**: The Wi-Fi component primarily captures probe requests, which are broadcast by devices looking for known networks. It does not actively connect to networks or capture all traffic.
*   **Hardware Requirements**: Specialized hardware (e.g., external Wi-Fi adapters capable of monitor mode, powerful Bluetooth dongles) may be required for optimal performance and range.
*   **Legal and Ethical Use**: Always ensure you have the necessary permissions and adhere to local laws and regulations when performing network scanning. Unauthorized scanning can be illegal and unethical.

## Contribution

Feel free to fork the repository, submit pull requests, or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

**Author**: Siddharth Sid
**Date**: February 8, 2026

## Running on Termux (Android)

Running this tool on Termux on an Android device has specific considerations and limitations, especially regarding Wi-Fi monitor mode. Bluetooth scanning should generally work.

### Termux Prerequisites

1.  **Install Termux**: Download and install Termux from F-Droid or Google Play Store.
2.  **Install Python and Git**: Inside Termux, install Python and Git:
    ```bash
    pkg update && pkg upgrade
    pkg install python git
    ```
3.  **Install `scapy` dependencies**: `scapy` might require `libcap` and `libpcap` development headers. Install them using:
    ```bash
    pkg install libpcap libpcap-dev
    ```
4.  **Grant Storage Permission**: Allow Termux to access storage:
    ```bash
    termux-setup-storage
    ```

### Termux Setup and Usage

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Crypsis-dev/network-scanner.git
    cd network-scanner
    ```
2.  **Install Python Libraries**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: `bleak` might require `python-dev` and `build-essential` packages, which can be installed via `pkg install python-dev build-essential` if you encounter issues.*

3.  **Wi-Fi Scanning on Termux (Limitations)**:
    *   **Monitor Mode**: Most Android devices do **not** support Wi-Fi monitor mode without rooting the device and using specialized kernels or external hardware. Therefore, the Wi-Fi sniffing (`scanner.py`) functionality for capturing probe requests is unlikely to work out-of-the-box on a standard Termux installation.
    *   If you have a rooted device and a custom ROM that enables monitor mode, you might be able to use tools like `airmon-ng` (if available for Termux) or directly interact with the wireless interface. This is an advanced setup and beyond the scope of this basic guide.

4.  **Bluetooth Scanning on Termux**:
    *   Bluetooth scanning using `bleak` should work on Termux, provided your device's Bluetooth is enabled and Termux has the necessary permissions.
    *   Run the scanner (only Bluetooth part will be effective without monitor mode for Wi-Fi):
        ```bash
        python3 scanner.py
        ```
    *   Press `Ctrl+C` to stop the scan and save data.

5.  **Analyze the Data**:
    ```bash
    python3 analyzer.py
    ```
    This will generate `scan_analysis_report.png` in your current directory.

### Termux Specific Notes

*   **Rooting**: Achieving full Wi-Fi packet capture capabilities (like monitor mode) on Android typically requires rooting your device and potentially flashing a custom kernel that supports packet injection/monitor mode. This carries risks and is not recommended for novice users.
*   **External Adapters**: Some external USB Wi-Fi adapters that support monitor mode might work with Termux if your device supports USB OTG and you have the correct drivers/kernel modules installed. This is also an advanced setup.
*   **Permissions**: Ensure Termux has all necessary permissions (especially location and Bluetooth) for the Bluetooth scanner to function correctly.
