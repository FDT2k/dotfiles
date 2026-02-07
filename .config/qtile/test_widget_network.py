from rofi import Rofi

rofi_l = Rofi(rofi_args=['-theme', '~/.config/rofi/left_toolbar.rasi'])
rofi_r = Rofi(rofi_args=['-theme', '~/.config/rofi/right_toolbar.rasi'])


def network_widget(qtile):
    get_ssid = "iwgetid -r"
    pos = subprocess.Popen(get_ssid, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ssid = pos.communicate()[0].decode('ascii').strip()
    get_status = "nmcli radio wifi"
    ps = subprocess.Popen(get_status, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    status = ps.communicate()[0].decode('ascii').strip()
    if status == 'enabled':
        connected = ' Turn Wifi Off'
        active = "off"
    else:
        connected = ' Turn Wifi On'
        active = "on"
    options = [
        connected, ' Bandwith Monitor (CLI)', ' Network Manager (CLI)', ' Network Manager (GUI)']
    index, key = rofi_r.select(wifi_icon + internet, options)
    if key == -1:
        rofi_r.close()
    else:
        if index == 0:
            subprocess.run("nmcli radio wifi " + active, shell=True)
        elif index == 1:
            qtile.cmd_spawn(term + ' -e bmon')
        elif index == 2:
            qtile.cmd_spawn(term + ' -e nmtui')
        else:
            qtile.cmd_spawn('nm-connection-editor')


def get_net_dev():
    get_dev = "ip addr show | awk '/inet.*brd/{print $NF; exit}'"
    ps = subprocess.Popen(get_dev, shell=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode('ascii').strip()
    return(output)


internet = ' Yei Internet is working!'


def get_public_ip():
    try:
        raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
        answer = raw.json()["Answer"].split()[4]
    except Exception as e:
        return "0.0.0.0"
    else:
        return answer


public_ip = get_public_ip()

if public_ip.startswith('0'):
    internet = "OMG You Have No Internet"

wifi = get_net_dev()
if wifi.startswith('w'):
    wifi_icon = ' '
else:
    wifi_icon = ' '
