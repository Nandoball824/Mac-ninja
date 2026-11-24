#!/usr/bin/env python3

import os
import sys
import random
import subprocess
import re
import signal

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"

LANG = "es"
ORIGINAL_HOSTNAME = None
ORIGINAL_MAC = None
SELECTED_INTERFACE = None

def t(text_en, text_es):
    if LANG == "en":
        return text_en
    return text_es

def clear_screen():
    os.system('clear')

def print_banner():
    banner = f"""
{Colors.RED}{Colors.BOLD}
                    ███╗   ███╗ █████╗  ██████╗     ███╗   ██╗██╗███╗   ██╗     ██╗ █████╗
                    ████╗ ████║██╔══██╗██╔════╝     ████╗  ██║██║████╗  ██║     ██║██╔══██╗
                    ██╔████╔██║███████║██║          ██╔██╗ ██║██║██╔██╗ ██║     ██║███████║
                    ██║╚██╔╝██║██╔══██║██║          ██║╚██╗██║██║██║╚██╗██║██   ██║██╔══██║
                    ██║ ╚═╝ ██║██║  ██║╚██████╗     ██║ ╚████║██║██║ ╚████║╚█████╔╝██║  ██║
                    ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝     ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚════╝ ╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}
                                ===================================================== 
                                             M A C   N I N J A   v2.0
                                 Creed by Nandoball824 - Use it on your own networks
                                =====================================================
{Colors.RESET}
    """
    print(banner)

def print_status(interface, current_mac, current_hostname):
    print(f"{Colors.CYAN}┌──────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}Interfaz:{Colors.RESET} {interface:<40} {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}MAC actual:{Colors.RESET} {current_mac:<38} {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET} {Colors.YELLOW}Hostname:{Colors.RESET} {current_hostname:<40} {Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}└──────────────────────────────────────────────────┘{Colors.RESET}")

def print_explanation(option):
    explanations = {
        "1": t("""
   EXPLANATION: Custom MAC - Allows you to enter a specific MAC address
   of your choice, for example 00:11:22:33:44:55. Useful to impersonate
   a specific device (Apple, Intel, Samsung, etc).""",
            """
   EXPLICACION: MAC personalizada - Te permite ingresar una MAC especifica
   que tu quieras, por ejemplo 00:11:22:33:44:55. Sirve para parecer un
   dispositivo especifico (Apple, Intel, Samsung, etc)."""),
        "2": t("""
   EXPLANATION: Random MAC - Generates a completely random MAC address.
   It's the fastest way to change your identity on the network.""",
            """
   EXPLICACION: MAC random - Genera una direccion MAC completamente aleatoria.
   Es la opcion mas rapida para cambiar tu identidad en la red."""),
        "3": t("""
   EXPLANATION: Restore original MAC - Returns to your network card's
   factory MAC address. Undoes any previous changes.""",
            """
   EXPLICACION: Restaurar MAC original - Vuelve a la MAC de fabrica de tu
   tarjeta de red. Sirve para deshacer cualquier cambio anterior."""),
        "4": t("""
   EXPLANATION: Random hostname - Changes your computer's name to a random
   one (androidXXXX, iPhoneXXXX, GalaxyXXXX, etc).""",
            """
   EXPLICACION: Hostname random - Cambia el nombre de tu equipo a uno
   aleatorio (androidXXXX, iPhoneXXXX, GalaxyXXXX, etc)."""),
        "5": t("""
   EXPLANATION: Custom hostname - Allows you to type any name you want
   for your computer on the network.""",
            """
   EXPLICACION: Hostname personalizado - Te permite escribir el nombre
   que quieras para tu equipo en la red."""),
        "6": t("""
   EXPLANATION: Restore original hostname - Returns to your computer's
   original name from before running this script.""",
            """
   EXPLICACION: Restaurar hostname original - Vuelve al nombre original
   de tu equipo antes de ejecutar este script."""),
        "7": t("""
   EXPLANATION: Renew IP - Requests a new IP address from the router.
   Prevents the router from linking your old IP to your new MAC.""",
            """
   EXPLICACION: Renovar IP - Le pide al router una nueva direccion IP.
   Sirve para que el router no relacione tu IP vieja con tu nueva MAC.""")
    }
    if option in explanations:
        print(f"{Colors.CYAN}{explanations[option]}{Colors.RESET}")
        print()

def restore_all():
    global ORIGINAL_MAC, SELECTED_INTERFACE, ORIGINAL_HOSTNAME
    print(f"\n{Colors.YELLOW}[+] {t('Restoring original settings...', 'Restaurando configuracion original...')}{Colors.RESET}")
    if SELECTED_INTERFACE and ORIGINAL_MAC:
        run_command(f"sudo ifconfig {SELECTED_INTERFACE} down")
        run_command(f"sudo macchanger -m {ORIGINAL_MAC} {SELECTED_INTERFACE}")
        run_command(f"sudo ifconfig {SELECTED_INTERFACE} up")
        print(f"{Colors.GREEN}[+] {t('Original MAC restored', 'MAC original restaurada')}{Colors.RESET}")
    if ORIGINAL_HOSTNAME:
        run_command(f"sudo hostname {ORIGINAL_HOSTNAME}")
        run_command(f"echo '{ORIGINAL_HOSTNAME}' | sudo tee /etc/hostname > /dev/null")
        run_command(f"sudo sed -i 's/127.0.1.1.*/127.0.1.1\\t{ORIGINAL_HOSTNAME}/g' /etc/hosts")
        print(f"{Colors.GREEN}[+] {t('Original hostname restored', 'Hostname original restaurado')}{Colors.RESET}")

def signal_handler(sig, frame):
    print(f"\n{Colors.RED}[!] {t('Exiting forcefully... Restoring original settings.', 'Saliendo bruscamente... Restaurando configuracion original.')}{Colors.RESET}")
    restore_all()
    print(f"\n{Colors.CYAN}{'='*55}{Colors.RESET}")
    print(f"{Colors.YELLOW}{t('Questions? Tips? Report bugs:', 'Dudas? Consejos? errores? reportelos en:')}{Colors.RESET}")
    print(f"{Colors.GREEN}luisferdeasistellez@gmail.com{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*55}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] {t('All settings restored. Goodbye!', 'Todo restaurado. Adios!')}{Colors.RESET}")
    sys.exit(0)

def select_language():
    global LANG
    clear_screen()
    print_banner()
    print(f"\n{Colors.CYAN}============================================{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}  SELECT LANGUAGE / SELECCIONA IDIOMA{Colors.RESET}")
    print(f"{Colors.CYAN}============================================{Colors.RESET}")
    print(f"  {Colors.GREEN}1.{Colors.RESET} English")
    print(f"  {Colors.GREEN}2.{Colors.RESET} Espanol")
    print(f"{Colors.CYAN}============================================{Colors.RESET}")
    
    option = input(f"{Colors.YELLOW}Lang{Colors.RED}> {Colors.RESET}").strip()
    if option == "1":
        LANG = "en"
    else:
        LANG = "es"

def run_command(cmd):
    subprocess.run(cmd, shell=True, capture_output=True)

def check_macchanger():
    result = subprocess.run("which macchanger", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"{Colors.RED}[!] {t('macchanger not found', 'macchanger no encontrado')}{Colors.RESET}")
        print(f"{Colors.YELLOW}[?] {t('Do you want to install it? (y/n)', 'Quieres instalarlo? (y/n)')}{Colors.RESET}")
        opt = input(f"{Colors.CYAN}> {Colors.RESET}").strip().lower()
        if opt == 'y' or opt == 'yes':
            print(f"{Colors.YELLOW}[+] {t('Installing macchanger...', 'Instalando macchanger...')}{Colors.RESET}")
            os.system("sudo apt update && sudo apt install macchanger -y")
            print(f"{Colors.GREEN}[+] {t('macchanger installed. Run the script again.', 'macchanger instalado. Ejecuta el script nuevamente.')}{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] {t('macchanger is required to use this script', 'macchanger es necesario para usar este script')}{Colors.RESET}")
            sys.exit(1)
    return True

def get_wifi_interfaces():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.split('\n'):
        if 'IEEE 802.11' in line:
            interfaces.append(line.split()[0])
    return interfaces

def get_current_mac(interface):
    result = subprocess.run(f"macchanger -s {interface}", shell=True, capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Current MAC' in line:
            match = re.search(r'([0-9a-fA-F:]{17})', line)
            if match:
                return match.group(0)
    return "Unknown"

def get_permanent_mac(interface):
    result = subprocess.run(f"macchanger -s {interface}", shell=True, capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Permanent MAC' in line:
            match = re.search(r'([0-9a-fA-F:]{17})', line)
            if match:
                return match.group(0)
    return None

def get_current_hostname():
    result = subprocess.run("hostname", shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def change_mac_random(interface):
    print(f"{Colors.YELLOW}[+] {t('Changing random MAC on', 'Cambiando MAC random en')} {interface}...{Colors.RESET}")
    run_command(f"sudo ifconfig {interface} down")
    run_command(f"sudo macchanger -r {interface}")
    run_command(f"sudo ifconfig {interface} up")
    new_mac = get_current_mac(interface)
    print(f"{Colors.GREEN}[+] {t('New MAC', 'Nueva MAC')}: {new_mac}{Colors.RESET}")
    return new_mac

def change_mac_custom(interface):
    print(f"{Colors.YELLOW}[+] {t('Custom MAC', 'MAC personalizada')}{Colors.RESET}")
    custom_mac = input(f"{Colors.CYAN}{t('Enter MAC (format XX:XX:XX:XX:XX:XX)', 'Ingresa la MAC (formato XX:XX:XX:XX:XX:XX)')}: {Colors.RESET}")
    if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', custom_mac):
        print(f"{Colors.RED}[!] {t('Invalid MAC format', 'Formato de MAC invalido')}{Colors.RESET}")
        return get_current_mac(interface)
    run_command(f"sudo ifconfig {interface} down")
    run_command(f"sudo macchanger -m {custom_mac} {interface}")
    run_command(f"sudo ifconfig {interface} up")
    print(f"{Colors.GREEN}[+] {t('MAC changed to', 'MAC cambiada a')}: {custom_mac}{Colors.RESET}")
    return custom_mac

def restore_mac(interface):
    print(f"{Colors.YELLOW}[+] {t('Restoring original MAC', 'Restaurando MAC original')}...{Colors.RESET}")
    run_command(f"sudo ifconfig {interface} down")
    run_command(f"sudo macchanger -p {interface}")
    run_command(f"sudo ifconfig {interface} up")
    original_mac = get_current_mac(interface)
    print(f"{Colors.GREEN}[+] {t('MAC restored', 'MAC restaurada')}: {original_mac}{Colors.RESET}")
    return original_mac

def change_hostname_random():
    print(f"{Colors.YELLOW}[+] {t('Changing to random hostname', 'Cambiando a hostname random')}...{Colors.RESET}")
    hostnames = ["android", "iPhone", "Galaxy", "Redmi", "PC", "LAPTOP", "DESKTOP", "user", "home", "office"]
    suffix = ''.join(random.choices('0123456789abcdef', k=4))
    new_hostname = random.choice(hostnames) + suffix
    run_command(f"sudo hostname {new_hostname}")
    run_command(f"echo '{new_hostname}' | sudo tee /etc/hostname > /dev/null")
    run_command(f"sudo sed -i 's/127.0.1.1.*/127.0.1.1\\t{new_hostname}/g' /etc/hosts")
    print(f"{Colors.GREEN}[+] {t('New hostname', 'Nuevo hostname')}: {new_hostname}{Colors.RESET}")
    return new_hostname

def change_hostname_custom():
    print(f"{Colors.YELLOW}[+] {t('Custom hostname', 'Hostname personalizado')}{Colors.RESET}")
    new_hostname = input(f"{Colors.CYAN}{t('Enter new hostname', 'Ingresa nuevo hostname')}: {Colors.RESET}").strip()
    if not new_hostname:
        print(f"{Colors.RED}[!] {t('Invalid hostname', 'Hostname invalido')}{Colors.RESET}")
        return get_current_hostname()
    run_command(f"sudo hostname {new_hostname}")
    run_command(f"echo '{new_hostname}' | sudo tee /etc/hostname > /dev/null")
    run_command(f"sudo sed -i 's/127.0.1.1.*/127.0.1.1\\t{new_hostname}/g' /etc/hosts")
    print(f"{Colors.GREEN}[+] {t('Hostname changed to', 'Hostname cambiado a')}: {new_hostname}{Colors.RESET}")
    return new_hostname

def restore_hostname():
    global ORIGINAL_HOSTNAME
    if ORIGINAL_HOSTNAME:
        print(f"{Colors.YELLOW}[+] {t('Restoring original hostname', 'Restaurando hostname original')}...{Colors.RESET}")
        run_command(f"sudo hostname {ORIGINAL_HOSTNAME}")
        run_command(f"echo '{ORIGINAL_HOSTNAME}' | sudo tee /etc/hostname > /dev/null")
        run_command(f"sudo sed -i 's/127.0.1.1.*/127.0.1.1\\t{ORIGINAL_HOSTNAME}/g' /etc/hosts")
        print(f"{Colors.GREEN}[+] {t('Hostname restored to', 'Hostname restaurado a')}: {ORIGINAL_HOSTNAME}{Colors.RESET}")
    else:
        print(f"{Colors.RED}[!] {t('No original hostname saved', 'No hay hostname original guardado')}{Colors.RESET}")

def renew_ip(interface):
    print(f"{Colors.YELLOW}[+] {t('Renewing IP', 'Renovando IP')}...{Colors.RESET}")
    run_command(f"sudo dhclient -r {interface}")
    run_command(f"sudo dhclient {interface}")
    result = subprocess.run(f"ifconfig {interface} | grep 'inet '", shell=True, capture_output=True, text=True)
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
    if match:
        print(f"{Colors.GREEN}[+] {t('New IP', 'Nueva IP')}: {match.group(1)}{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}[!] {t('IP not obtained (check connection)', 'IP no obtenida (revisa conexion)')}{Colors.RESET}")

def main():
    global ORIGINAL_HOSTNAME, ORIGINAL_MAC, SELECTED_INTERFACE, LANG
    
    signal.signal(signal.SIGINT, signal_handler)
    
    select_language()
    
    if os.geteuid() != 0:
        print(f"{Colors.RED}[!] {t('Run with sudo', 'Ejecuta con sudo')}{Colors.RESET}")
        sys.exit(1)
    
    check_macchanger()
    
    interfaces = get_wifi_interfaces()
    if not interfaces:
        print(f"{Colors.RED}[!] {t('No WiFi interfaces found', 'No se encontraron interfaces WiFi')}{Colors.RESET}")
        sys.exit(1)
    
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.CYAN}[*] {t('Available interfaces', 'Interfaces disponibles')}: {', '.join(interfaces)}{Colors.RESET}")
        
        iface = input(f"{Colors.YELLOW}[*] {t('Select interface', 'Selecciona interfaz')} [{interfaces[0]}]: {Colors.RESET}").strip()
        if not iface:
            iface = interfaces[0]
            break
        elif iface in interfaces:
            break
        else:
            print(f"{Colors.RED}[!] {t('Invalid interface. Try again.', 'Interfaz no valida. Intenta de nuevo.')}{Colors.RESET}")
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
    
    SELECTED_INTERFACE = iface
    ORIGINAL_MAC = get_permanent_mac(iface)
    ORIGINAL_HOSTNAME = get_current_hostname()
    
    while True:
        current_mac = get_current_mac(iface)
        current_hostname = get_current_hostname()
        
        clear_screen()
        print_banner()
        print_status(iface, current_mac, current_hostname)
        
        print(f"\n{Colors.PURPLE}============================================{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}  MAC NINJA - {t('Main Menu', 'Menu Principal')}{Colors.RESET}")
        print(f"{Colors.PURPLE}============================================{Colors.RESET}")
        print(f"  {Colors.GREEN}1.{Colors.RESET} {t('Custom MAC', 'MAC personalizada')}")
        print(f"  {Colors.GREEN}2.{Colors.RESET} {t('Random MAC', 'MAC random')}")
        print(f"  {Colors.GREEN}3.{Colors.RESET} {t('Restore original MAC', 'Restaurar MAC original')}")
        print(f"  {Colors.GREEN}4.{Colors.RESET} {t('Random hostname', 'Hostname random')}")
        print(f"  {Colors.GREEN}5.{Colors.RESET} {t('Custom hostname', 'Hostname personalizado')}")
        print(f"  {Colors.GREEN}6.{Colors.RESET} {t('Restore original hostname', 'Restaurar hostname original')}")
        print(f"  {Colors.GREEN}7.{Colors.RESET} {t('Renew IP', 'Renovar IP')}")
        print(f"  {Colors.GREEN}8.{Colors.RESET} {t('Change language', 'Cambiar idioma')}")
        print(f"  {Colors.RED}0.{Colors.RESET} {t('Exit', 'Salir')}")
        print(f"{Colors.PURPLE}============================================{Colors.RESET}")
        
        option = input(f"{Colors.YELLOW}Ninja{Colors.RED}> {Colors.RESET}").strip()
        
        if option == "1":
            clear_screen()
            print_banner()
            print_explanation("1")
            change_mac_custom(iface)
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "2":
            clear_screen()
            print_banner()
            print_explanation("2")
            change_mac_random(iface)
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "3":
            clear_screen()
            print_banner()
            print_explanation("3")
            restore_mac(iface)
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "4":
            clear_screen()
            print_banner()
            print_explanation("4")
            change_hostname_random()
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "5":
            clear_screen()
            print_banner()
            print_explanation("5")
            change_hostname_custom()
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "6":
            clear_screen()
            print_banner()
            print_explanation("6")
            restore_hostname()
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "7":
            clear_screen()
            print_banner()
            print_explanation("7")
            renew_ip(iface)
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        elif option == "8":
            select_language()
        elif option == "0":
            restore_all()
            print(f"\n{Colors.CYAN}{'='*55}{Colors.RESET}")
            print(f"{Colors.YELLOW}{t('Questions? Tips? Report bugs:', 'Dudas? Consejos? Reportar errores:')}{Colors.RESET}")
            print(f"{Colors.GREEN}luisferdeasistellez@gmail.com{Colors.RESET}")
            print(f"{Colors.CYAN}{'='*55}{Colors.RESET}")
            print(f"{Colors.GREEN}[+] {t('Goodbye, ninja.', 'Adios, ninja.')}{Colors.RESET}")
            break
        elif option == "":
            print(f"{Colors.RED}[!] {t('Invalid option', 'Opcion invalida')}{Colors.RESET}")
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] {t('Invalid option', 'Opcion invalida')}{Colors.RESET}")
            input(f"{Colors.CYAN}{t('Press Enter to continue', 'Presiona Enter para continuar')}{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        signal_handler(None, None)
