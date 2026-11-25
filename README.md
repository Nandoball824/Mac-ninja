# MAC Ninja v2.0

Interactive Python CLI tool for changing Wi-Fi MAC addresses, modifying the system hostname, and renewing DHCP leases on Linux. Built for networking labs, connectivity testing, system administration practice, and controlled lab environments.

Created by **Nandoball824**.

## Features

* **Interactive terminal menu** (no command-line flags to memorize).
* **Bilingual UI** (English and Spanish), switchable anytime from the main menu.
* **MAC address management:**
  * Set a custom MAC address (`XX:XX:XX:XX:XX:XX`).
  * Assign a random MAC address.
  * Restore the original hardware (permanent) MAC address.
* **Hostname management:**
  * Generate a random hostname (using prefixes such as `android`, `iPhone`, `Galaxy`, `Redmi`, `PC`, `LAPTOP`, `DESKTOP`, `user`, `home`, `office` plus a 4-character hex suffix).
  * Set a custom hostname.
  * Restore the original hostname from before the script started.
* **IP renewal:** Releases and renews the IP lease via `dhclient` so a new MAC is less easily tied to a previous IP during lab tests.
* **Automatic restoration on exit:** Exiting with `0` or pressing `Ctrl + C` triggers `restore_all()` to restore the original MAC and hostname.

## Requirements & Dependencies

* **OS:** Linux.
* **Python:** Python 3.x.
* **Privileges:** Root / `sudo` access (required to bring interfaces up/down and change MAC, IP, and hostname).
* **System utilities invoked by the script:**
  * `macchanger` (if missing, the script offers to install it via `apt`).
  * `iwconfig` (used to detect `IEEE 802.11` wireless interfaces).
  * `ifconfig` (used to toggle interface state and read IP info).
  * `dhclient` (used for the IP renewal option).

> **Compatibility notes:** This script relies on classic utilities (`iwconfig`, `ifconfig`, `dhclient`, and `apt` for auto-install). On non-Debian/Ubuntu distros or systems managed strictly by `NetworkManager` / `iproute2`, install the required packages manually and verify your network manager does not overwrite manual changes.

## Installation

Clone the repository and enter the project folder:

```bash
git clone https://github.com/Nandoball824/Mac-ninja.git
cd Mac-ninja
```

Make the script executable (optional):

```bash
chmod +x "Mac_Ninja 2.0.py"
```

## Usage

Run the script with `sudo`:

```bash
sudo python3 "Mac_Ninja 2.0.py"
```

*(Tip: If you rename the file to `mac_ninja.py`, you won't need quotes or spaces when running it).*

### Interactive Flow

1. **Select language:** Choose `1` for English or `2` for Spanish.
2. **Select Wi-Fi interface:** Only wireless interfaces reported by `iwconfig` (`IEEE 802.11`) are listed. Pressing `Enter` selects the first interface by default. *(Wired Ethernet interfaces are not detected).*
3. **Navigate the main menu (`0`–`8`):**
   * `1` – **Custom MAC:** Enter a MAC in `XX:XX:XX:XX:XX:XX` format.
   * `2` – **Random MAC:** Switch to a randomly generated MAC.
   * `3` – **Restore original MAC:** Revert to the permanent hardware MAC.
   * `4` – **Random hostname:** Change the machine's hostname to a random one.
   * `5` – **Custom hostname:** Set a custom hostname.
   * `6` – **Restore original hostname:** Revert to the initial hostname.
   * `7` – **Renew IP:** Release and request a new IP using `dhclient`.
   * `8` – **Change language:** Switch between English and Spanish.
   * `0` – **Exit:** Attempt to restore original MAC and hostname, then exit.

## Lab Use Cases

* **DHCP & lease testing:** Observe how a lab DHCP server or test router behaves when a client changes MAC addresses and requests a new IP.
* **MAC filtering validation:** Test allow/deny MAC access rules on lab routers or access points you control.
* **Host fingerprinting & network visibility:** Inspect how different MACs and hostnames show up in ARP tables, local logs, or lab scans.
* **Network privacy testing:** Reduce persistent link-layer tracking when testing across external networks.

## Disclaimer

This tool is intended strictly for educational purposes, networking labs, self-administration, and authorized testing environments. You are solely responsible for how you use this software and must comply with all applicable laws and network policies.

## Contact / Bug Reports

Questions, suggestions, or bug reports: `luisferdeasistellez@gmail.com`
