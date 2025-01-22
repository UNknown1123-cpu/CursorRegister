import os
import re
import csv
import copy
import queue
import random
import argparse
import threading
import concurrent.futures
from sys import platform
from datetime import datetime

from faker import Faker
from DrissionPage import ChromiumOptions, Chromium
from temp_mails import Dropmail_me , Inboxes_com

CURSOR_URL = "https://www.cursor.com/"
CURSOR_LOGIN_URL = "https://authenticator.cursor.sh"
CURSOR_SIGN_UP_URL =  "https://authenticator.cursor.sh/sign-up"
CURSOR_SETTINGS_URL = "https://www.cursor.com/settings"

# Parameters for debugging purpose
hide_account_info = os.getenv('HIDE_ACCOUNT_INFO', 'false').lower() == 'true'
enable_register_log = True
enable_headless = os.getenv('ENABLE_HEADLESS', 'false').lower() == 'true'
enable_browser_log = os.getenv('ENABLE_BROWSER_LOG', 'true').lower() == 'true' or not enable_headless

PROXY_LIST = [
    "http://183.60.141.41:443",
    "socks4://72.195.34.58:4145",
    "socks4://184.178.172.26:4145",
    "http://87.248.129.26:80",
    "socks4://174.75.211.222:4145",
    "http://72.10.160.91:29417",
    "socks4://184.181.217.194:4145",
    "http://27.109.215.216:80",
    "http://101.108.195.54:8080",
    "socks4://198.8.94.170:4145",
    "socks4://117.74.65.207:80",
    "http://185.44.65.171:9595",
    "http://67.43.228.253:15629",
    "socks4://98.170.57.249:4145",
    "socks4://192.111.139.163:19404",
    "http://50.114.33.185:8080",
    "https://198.16.70.29:425",
    "socks4://72.214.108.67:4145",
    "http://67.43.236.21:13211",
    "http://61.158.175.38:9002",
    "http://47.94.7.13:8081",
    "socks5://8.218.39.40:10800",
    "http://103.41.33.169:58080",
    "socks4://186.190.228.83:4153",
    "http://39.101.161.223:8090",
    "http://47.97.94.40:20009",
    "socks4://162.253.68.97:4145",
    "http://83.168.72.172:8081",
    "socks5://184.168.121.153:49562",
    "socks5://50.63.12.101:59998",
    "http://103.216.50.11:8080",
    "http://67.43.228.250:22837",
    "http://147.75.34.92:10000",
    "http://130.61.111.246:6379",
    "http://188.253.112.218:80",
    "http://203.89.8.107:80",
    "http://103.143.8.126:8089",
    "socks4://174.77.111.196:4145",
    "http://223.95.58.59:8080",
    "http://91.241.217.58:9090",
    "socks4://199.229.254.129:4145",
    "socks4://192.111.137.34:18765",
    "http://117.74.65.207:443",
    "http://47.243.92.199:3128",
    "http://103.152.112.120:80",
    "socks4://192.252.216.81:4145",
    "socks4://184.178.172.18:15280",
    "http://39.102.210.12:443",
    "socks4://199.187.210.54:4145",
    "http://96.0.147.177:443",
    "socks4://98.181.137.80:4145",
    "socks4://142.54.236.97:4145",
    "http://41.59.90.171:80",
    "http://220.248.70.237:9002",
    "http://67.43.227.230:27481",
    "socks4://142.54.237.34:4145",
    "http://111.1.61.47:3128",
    "http://112.124.67.149:4780",
    "http://122.51.39.108:20131",
    "http://50.62.183.223:80",
    "http://58.147.186.214:3125",
    "socks5://88.202.230.103:9497",
    "http://123.154.19.95:8085",
    "http://211.78.63.115:80",
    "http://72.10.160.91:7769",
    "socks4://142.54.235.9:4145",
    "http://178.128.113.118:23128",
    "http://72.10.160.170:4021",
    "socks5://184.168.121.153:52630",
    "socks4://192.252.208.70:14282",
    "https://104.129.194.44:11715",
    "socks5://101.132.245.14:443",
    "http://91.241.241.60:9090",
    "http://72.10.160.171:18151",
    "socks4://199.58.184.97:4145",
    "https://23.106.56.22:425",
    "socks4://72.195.34.60:27391",
    "socks5://124.221.56.11:22",
    "http://129.153.164.142:8080",
    "socks5://194.44.208.62:80",
    "http://217.15.166.95:80",
    "http://120.26.0.11:8880",
    "http://47.56.110.204:8989",
    "socks4://192.252.208.67:14287",
    "http://72.10.164.178:9615",
    "http://102.132.33.27:8080",
    "http://45.8.21.156:80",
    "socks4://192.252.209.155:14455",
    "http://113.108.13.120:4433",
    "http://67.43.227.226:28745",
    "https://147.75.34.92:9401",
    "http://102.132.33.55:8080",
    "http://185.159.153.234:80",
    "http://67.43.236.18:15455",
    "socks5://50.63.12.101:46403",
    "http://221.231.13.198:1080",
    "http://178.48.68.61:18080",
    "http://154.6.189.35:3128",
    "http://121.227.146.72:8089",
    "http://103.152.112.157:80",
    "http://120.25.1.15:7890",
    "http://219.65.73.81:80",
    "http://82.115.19.142:80",
    "socks4://124.221.56.11:22",
    "http://185.101.16.52:80",
    "http://101.201.76.157:443",
    "socks4://142.54.239.1:4145",
    "socks5://192.111.129.145:16894",
    "http://4.175.200.138:8080",
    "https://84.239.14.153:9002",
    "http://157.230.89.122:18109",
    "socks4://174.64.199.82:4145",
    "http://203.77.215.45:10000",
    "http://101.66.198.193:8085",
    "socks4://98.178.72.21:10919",
    "http://181.41.194.186:80",
    "socks5://198.8.94.170:4145",
    "http://47.83.192.255:8888",
    "http://8.138.42.216:8090",
    "socks4://198.12.248.208:47291",
    "socks5://184.168.121.153:20974",
    "http://109.61.42.223:80",
    "http://62.234.223.172:8081",
    "socks4://104.200.152.30:4145",
    "http://196.251.131.82:8080",
    "socks4://182.53.216.4:4153",
    "http://79.110.202.131:8081",
    "http://72.10.160.171:4975",
    "http://123.57.204.128:8000",
    "socks4://43.231.192.105:4145",
    "socks5://72.195.34.42:4145",
    "http://154.16.146.45:80",
    "https://198.16.70.29:443",
    "http://102.132.42.13:8080",
    "http://178.177.54.157:8080",
    "http://47.243.114.192:8180",
    "http://123.30.154.171:7777",
    "socks4://70.166.167.38:57728",
    "socks4://192.111.135.18:18301",
    "http://38.242.199.124:8089",
    "http://206.189.146.185:8888",
    "http://158.255.77.166:80",
    "socks4://174.77.111.198:49547",
    "socks4://198.8.84.3:4145",
    "http://47.100.254.82:80",
    "https://206.188.212.176:8443",
    "socks5://184.168.121.153:47137",
    "socks4://68.71.254.6:4145",
    "http://23.247.137.142:80",
    "http://118.31.43.236:443",
    "socks4://142.54.228.193:4145",
    "socks5://50.63.12.101:1376",
    "socks5://130.255.160.60:39123",
    "http://101.35.160.182:80",
    "http://45.143.223.11:8080",
    "http://84.39.112.144:3128",
    "http://160.248.7.177:80",
    "http://82.102.10.253:80",
    "socks4://142.54.226.214:4145",
    "socks4://192.111.137.35:4145",
    "http://45.87.68.4:15321",
    "socks4://85.89.184.87:5678",
    "http://67.43.227.226:13949",
    "http://143.42.191.48:80",
    "socks4://67.201.59.70:4145",
    "http://39.105.27.30:3128",
    "http://46.47.197.210:3128",
    "http://102.223.186.246:8888",
    "http://114.35.140.157:8080",
    "socks4://98.175.31.195:4145",
    "http://200.174.198.86:8888",
    "socks4://107.181.168.145:4145",
    "https://207.244.71.80:431",
    "socks4://192.111.138.29:4145",
    "socks4://24.249.199.4:4145",
    "http://185.105.102.179:80",
    "socks4://192.111.139.162:4145",
    "http://47.103.133.180:7890",
    "socks4://107.152.98.5:4145",
    "socks5://172.232.236.34:1080",
    "http://111.3.102.207:30001",
    "socks4://199.102.105.242:4145",
    "socks4://199.116.114.11:4145",
    "socks4://174.64.199.79:4145",
    "socks4://45.249.79.190:3629",
    "https://205.178.186.37:8443",
    "http://72.10.164.178:3843",
    "http://72.10.164.178:12939",
    "http://63.143.57.117:80",
    "http://47.251.43.115:33333",
    "http://162.223.90.130:80",
    "socks4://184.170.248.5:4145",
    "http://67.43.227.226:21689",
    "socks5://123.131.128.235:1080",
    "http://83.168.74.163:8080",
    "socks4://74.119.144.60:4145",
    "socks4://174.77.111.197:4145",
    "http://1.15.144.231:8989",
    "http://185.105.102.189:80",
    "http://103.27.111.156:1080",
    "socks4://72.37.216.68:4145",
    "socks4://24.249.199.12:4145",
    "http://72.10.164.178:6007",
    "http://39.175.75.144:30001",
    "socks4://72.195.34.35:27360",
    "http://103.216.50.224:8080",
    "socks5://172.104.164.41:1080",
    "socks4://184.178.172.11:4145",
    "http://47.100.67.65:7890",
    "http://8.146.207.243:8888",
    "http://47.104.160.169:443",
    "socks4://68.71.249.153:48606",
    "socks5://192.252.209.155:14455",
    "socks4://142.54.231.38:4145",
    "https://65.49.68.84:16135",
    "socks4://142.54.232.6:4145",
    "http://185.49.31.205:8080",
    "socks4://192.111.130.2:4145",
    "socks5://51.210.111.216:43311",
    "http://47.56.110.204:8990",
    "http://212.127.95.235:8081",
    "http://64.227.172.34:8080",
    "socks4://70.166.167.55:57745",
    "http://96.0.147.177:80",
    "http://23.247.136.245:80",
    "http://45.92.177.60:8080",
    "http://203.95.196.139:8080",
    "socks4://184.181.217.206:4145",
    "http://103.49.202.252:80",
    "socks4://192.252.215.5:16137",
    "socks4://184.170.249.65:4145",
    "socks5://49.232.59.192:1080",
    "http://102.132.41.49:8080",
    "http://60.188.102.225:18080",
    "socks4://72.37.217.3:4145",
    "http://152.136.41.178:8081",
    "http://47.102.185.210:8091",
    "http://95.66.244.250:8080",
    "http://58.240.211.251:7890",
    "socks5://184.168.121.153:4997",
    "http://103.105.224.181:8083",
    "http://124.227.219.106:8082",
    "http://157.245.97.60:80",
    "http://46.12.60.51:8080",
    "http://194.147.33.5:8080",
    "socks4://192.111.139.165:4145",
    "http://5.160.235.243:3128",
    "socks4://117.74.65.207:443",
    "http://80.249.112.162:80",
    "socks4://199.58.185.9:4145",
    "socks4://192.252.214.20:15864",
    "http://87.106.66.232:3128",
    "socks4://184.178.172.25:15291",
    "http://167.86.106.97:3128",
    "http://154.16.146.43:80",
    "socks5://184.168.121.153:62648",
    "http://154.16.146.41:80",
    "http://212.108.155.170:9090",
    "http://198.49.68.80:80",
    "http://186.48.8.176:3128",
    "http://23.247.136.248:80",
    "http://23.247.136.254:80",
    "socks5://98.152.200.61:8081",
    "http://59.39.226.243:2324",
    "http://154.16.146.48:80",
    "socks4://184.181.217.213:4145",
    "socks4://98.188.47.150:4145",
    "https://205.178.137.66:8447",
    "http://116.68.162.18:1111",
    "http://8.215.110.63:7777",
    "socks4://184.181.217.201:4145",
    "http://51.254.78.223:80",
    "http://98.8.195.160:443",
    "http://185.172.214.112:80",
    "http://67.43.227.227:17607",
    "socks4://72.195.114.169:4145",
    "socks4://192.252.220.89:4145",
    "http://12.176.231.147:80",
    "socks5://51.210.111.216:43520",
    "socks5://184.168.121.153:17249",
    "socks4://192.111.130.5:17002",
    "socks5://184.168.121.153:12475",
    "http://121.37.195.205:80",
    "socks4://192.111.129.145:16894",
    "http://158.255.77.169:80",
    "http://203.95.198.35:8080",
    "socks4://202.51.124.166:1080",
    "http://183.215.23.242:9091",
    "http://154.16.146.46:80",
    "socks4://43.230.196.98:48200",
    "socks4://206.220.175.2:4145",
    "https://84.239.49.37:9002",
    "http://47.98.240.170:9999",
    "https://138.199.35.213:9002",
    "http://43.251.133.179:8080",
    "socks4://184.178.172.5:15303",
    "http://67.43.236.19:13375",
    "http://159.65.230.46:8888",
    "socks4://142.54.229.249:4145",
    "http://39.98.107.108:32604",
    "http://111.1.61.49:3128",
    "socks4://107.181.161.81:4145",
    "http://91.107.196.104:8585",
    "socks5://184.168.121.153:14013",
    "http://34.87.84.105:80",
    "http://219.79.87.158:8080",
    "http://47.91.104.88:3128",
    "http://159.224.232.194:8888",
    "http://79.110.200.148:8081",
    "socks4://199.102.106.94:4145",
    "http://119.62.108.179:8085",
    "http://103.118.44.222:8080",
    "socks4://74.119.147.209:4145",
    "socks5://110.41.142.196:443",
    "http://97.74.87.226:80",
    "socks4://68.71.247.130:4145",
    "http://143.107.199.248:8080",
    "http://134.209.23.180:8888",
    "http://115.159.121.181:80",
    "socks5://184.168.121.153:1052",
    "http://109.197.197.170:3128",
    "http://183.234.215.11:8443",
    "socks4://184.181.217.220:4145",
    "http://47.97.121.189:1000",
    "http://185.212.60.62:80",
    "http://188.133.203.154:8081",
    "http://172.191.74.198:8080",
    "socks4://68.1.210.189:4145",
    "http://113.191.184.163:10000",
    "http://68.208.221.179:80",
    "http://67.43.227.229:27481",
    "http://144.126.216.57:80",
    "http://67.43.236.18:11213",
    "socks5://184.168.121.153:64744",
    "http://139.129.202.244:80",
    "http://122.185.198.242:7999",
    "socks4://98.170.57.231:4145",
    "http://8.213.151.128:3128",
    "http://14.204.97.72:8085",
    "http://72.10.164.178:24249",
    "http://73.117.183.115:80",
    "socks5://192.111.137.35:4145",
    "http://185.49.31.207:8081",
    "http://183.60.141.17:443",
    "socks4://104.37.135.145:4145",
    "socks4://72.195.101.99:4145",
    "socks5://47.110.90.254:1080",
    "http://102.132.46.134:8080",
    "socks4://198.8.94.174:39078",
    "socks4://184.181.217.210:4145",
    "http://45.22.209.157:8888",
    "socks5://51.75.126.150:36055",
    "http://154.0.14.116:3128",
    "socks4://192.111.135.17:18302",
    "socks4://103.88.169.106:33149",
    "http://1.202.174.38:49080",
    "http://203.95.199.159:8080",
    "http://212.127.93.185:8081",
    "socks4://72.195.34.42:4145",
    "socks4://184.178.172.14:4145",
    "http://147.75.34.92:9443",
    "http://106.42.30.243:82",
    "socks4://184.178.172.3:4145",
    "socks4://72.195.114.184:4145",
    "http://89.117.22.218:8080",
    "http://72.10.160.90:21301",
    "http://36.103.167.209:7890",
    "http://103.63.190.72:8080",
    "http://8.219.97.248:80",
    "socks5://212.237.125.216:6969",
    "socks4://192.111.137.37:18762",
    "http://161.97.136.251:3128",
    "http://158.255.77.168:80",
    "socks4://184.178.172.17:4145",
    "http://223.166.234.190:7890",
    "socks4://184.178.172.28:15294",
    "http://88.198.121.95:3128",
    "http://188.32.100.60:8080",
    "http://39.106.192.29:8443"
]

PROXY_LIST = [proxy for proxy in PROXY_LIST if proxy.startswith("http")]

def cursor_turnstile(tab, retry_times = 5):
    thread_id = threading.current_thread().ident

    for retry in range(retry_times): # Retry times
        try:
            if enable_register_log: print(f"[Register][{thread_id}][{retry}] Passing Turnstile")
            challenge_shadow_root = tab.ele('@id=cf-turnstile').child().shadow_root
            challenge_shadow_button = challenge_shadow_root.ele("tag:iframe", timeout=30).ele("tag:body").sr("xpath=//input[@type='checkbox']")
            if challenge_shadow_button:
                challenge_shadow_button.click()
                tab.wait.load_start()
                break
        except:
            pass
        if retry == retry_times - 1:
            print("[Register] Timeout when passing turnstile")

def sign_up(options):

    def wait_for_new_email_thread(mail, queue, timeout=300):
        try:
            data = mail.wait_for_new_email(delay=1, timeout=timeout)
            queue.put(copy.deepcopy(data))
        except Exception as e:
            queue.put(None)


    # Maybe fail to open the browser
    try:
        proxy = random.choice(PROXY_LIST)
        print(proxy)
        options.set_proxy(proxy)
        browser = Chromium(options)
    except Exception as e:
        print(e)
        return None

    retry_times = 5
    thread_id = threading.current_thread().ident
    
    # Get temp email address
    # type(mailnot).__name__ in [Tempmail_io, Guerillamail_com]
    mail = Dropmail_me()
    #mail = Guerillamail_com()
    email = mail.email

    # Get password and name by faker
    fake = Faker()
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    first_name, last_name = fake.name().split(' ')[0:2]

    email_queue = queue.Queue()
    email_thread = threading.Thread(target=wait_for_new_email_thread, args=(mail, email_queue, ))
    email_thread.daemon = True
    email_thread.start()

    tab = browser.new_tab(CURSOR_SIGN_UP_URL)
    #if tab.code
    # Input first name, last name, email
    for retry in range(retry_times):
        try:
            if enable_register_log: print(f"[Register][{thread_id}][{retry}] Input first name, last name, email")
            tab.refresh()
            tab.ele("xpath=//input[@name='first_name']").input(first_name, clear=True)
            tab.ele("xpath=//input[@name='last_name']").input(last_name, clear=True)
            tab.ele("xpath=//input[@name='email']").input(email, clear=True)
            tab.ele("@type=submit").click()
            tab.wait.load_start()

            #if tab.ele("xpath=//input[@name='email']").attr("data-invalid") == "true":
            #    print(f"[Register][{thread_id}] Email is invalid")
            #    return None
            
            # In password page or data is validated, continue to next page
            if tab.wait.eles_loaded("xpath=//input[@name='password']", timeout=5):
                print(f"[Register][{thread_id}] Continue to password page")
                break
            # If not in password page, try pass turnstile page
            elif tab.ele("xpath=//input[@name='email']", timeout=3).attr("data-valid") is not None:
                if enable_register_log: print(f"[Register][{thread_id}][{retry}] Try pass Turnstile for email page")
                cursor_turnstile(tab)

        except Exception as e:
            print(f"[Register][{thread_id}] Exception when handlding email page.")
            print(e)
        
        # In password page or data is validated, continue to next page
        if tab.wait.eles_loaded("xpath=//input[@name='password']"):
            print(f"[Register][{thread_id}] Continue to password page")
            break

        # Kill the function since time out 
        if retry == retry_times - 1:
            print(f"[Register][{thread_id}] Timeout when inputing email address")
            if not enable_browser_log: browser.quit(force=True, del_data=True)
            return None
    
    # Input password
    for retry in range(retry_times):
        try:
            if enable_register_log: print(f"[Register][{thread_id}][{retry}] Input password")
            tab.ele("xpath=//input[@name='password']").input(password, clear=True)
            tab.ele('@type=submit').click()
            tab.wait.load_start()

            # In code verification page or data is validated, continue to next page
            if tab.wait.eles_loaded("xpath=//input[@data-index=0]", timeout=5):
                print(f"[Register][{thread_id}] Continue to email code page")
                break
            # If not in verification code page, try pass turnstile page
            elif tab.ele("xpath=//input[@name='password']", timeout=3).attr("data-valid") is not None:
                if enable_register_log: print(f"[Register][{thread_id}][{retry}] Try pass Turnstile for password page")
                cursor_turnstile(tab)

        except Exception as e:
            print(f"[Register][{thread_id}] Exception when handling password page.")
            print(e)

        # In code verification page or data is validated, continue to next page
        if tab.wait.eles_loaded("xpath=//input[@data-index=0]"):
            print(f"[Register][{thread_id}] Continue to email code page")
            break

        # Kill the function since time out 
        if retry == retry_times - 1:
            if enable_register_log: print(f"[Register][{thread_id}] Timeout when inputing password")
            if not enable_browser_log: browser.quit(force=True, del_data=True)
            return None

    # Get email verification code
    try:
        data = email_queue.get(timeout=60)
        assert data is not None, "Fail to get code from email."

        verify_code = None
        if "body_text" in data:
            message_text = data["body_text"]
            message_text = message_text.strip().replace('\n', '').replace('\r', '').replace('=', '')
            verify_code = re.search(r'open browser window\.(\d{6})This code expires', message_text).group(1)
        elif "preview" in data:
            message_text = data["preview"]
            message_text = message_text.strip().replace('\n', '').replace('\r', '').replace(' ', '')
            verify_code = re.search(r'(\d{6})Thiscodeexpires', message_text).group(1)
        # Handle HTML format
        elif "content" in data:
            message_text = data["content"]
            message_text = re.sub(r"<[^>]*>", "", message_text)
            message_text = re.sub(r"&#8202;", "", message_text)
            message_text = re.sub(r"&nbsp;", "", message_text)
            message_text = re.sub(r'[\n\r\s]', "", message_text)
            verify_code = re.search(r'openbrowserwindow\.(\d{6})Thiscodeexpires', message_text).group(1)
        assert verify_code is not None, "Fail to get code from email."

    except Exception as e:
        print(f"[Register][{thread_id}] Fail to get code from email.")
        if not enable_browser_log: browser.quit(force=True, del_data=True)
        return None

    # Input email verification code
    for retry in range(retry_times):
        try:
            if enable_register_log: print(f"[Register][{thread_id}][{retry}] Input email verification code")

            for idx, digit in enumerate(verify_code, start = 0):
                tab.ele(f"xpath=//input[@data-index={idx}]").input(digit, clear=True)
                tab.wait(0.1, 0.3)
            tab.wait(0.5, 1.5)
        except Exception as e:
            print(f"[Register][{thread_id}] Exception when handling email code page.")
            print(e)

        if tab.url != CURSOR_URL:
            if enable_register_log: print(f"[Register][{thread_id}][{retry}] Try pass Turnstile for email code page.")
            cursor_turnstile(tab)

        if tab.wait.url_change(CURSOR_URL, timeout=15):
            break

        # Kill the function since time out 
        if retry == retry_times - 1:
            if enable_register_log: print(f"[Register][{thread_id}] Timeout when inputing email verification code")
            if not enable_browser_log: browser.quit(force=True, del_data=True)
            return None

    # Get cookie
    try:
        cookies = tab.cookies().as_dict()
    except e:
        print(f"[Register][{thread_id}] Fail to get cookie.")
        if not enable_browser_log: browser.quit(force=True, del_data=True)
        return None

    token = cookies.get('WorkosCursorSessionToken', None)
    if enable_register_log:
        if token is not None:
            print(f"[Register][{thread_id}] Register Account Successfully.")
        else:
            print(f"[Register][{thread_id}] Register Account Failed.")

    if not hide_account_info:
        print(f"[Register] Cursor Email: {email}")
        print(f"[Register] Cursor Password: {password}")
        print(f"[Register] Cursor Token: {token}")

    browser.quit(force=True, del_data=True)

    return {
        'username': email,
        'password': password,
        'token': token
    }

def register_cursor(number, max_workers):

    options = ChromiumOptions()
    options.auto_port()
    # Use turnstilePatch from https://github.com/TheFalloutOf76/CDP-bug-MouseEvent-.screenX-.screenY-patcher
    options.add_extension("turnstilePatch")

    if platform == "linux" or platform == "linux2":
        platformIdentifier = "X11; Linux x86_64"
    elif platform == "darwin":
        platformIdentifier = "Macintosh; Intel Mac OS X 10_15_7"
    elif platform == "win32":
        platformIdentifier = "Windows NT 10.0; Win64; x64"
    options.set_user_agent(f"Mozilla/5.0 ({platformIdentifier}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
    if enable_headless: 
        options.headless()

    # Run the code using multithreading
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(sign_up, copy.deepcopy(options)) for _ in range(number)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                results.append(result)

    results = [result for result in results if result["token"] is not None]

    if len(results) > 0:
        formatted_date = datetime.now().strftime("%Y-%m-%d")

        csv_file = f"./output_{formatted_date}.csv"
        token_file = f"./token_{formatted_date}.csv"

        fieldnames = results[0].keys()

        # Write username, password, token into a csv file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerows(results)

        # Only write token to csv file, without header
        tokens = [{'token': row['token']} for row in results]
        with open(token_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['token'])
            writer.writerows(tokens)

    return results

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Cursor Registor')
    parser.add_argument('--number', type=int, default=2, help="How many account you want")
    parser.add_argument('--max_workers', type=int, default=1, help="How many workers in multithreading")
    
    # The parameters with name starts with oneapi are used to uploead the cookie token to one-api, new-api, chat-api server.
    parser.add_argument('--oneapi', action='store_true', help='Enable One-API or not')
    parser.add_argument('--oneapi_url', type=str, required=False, help='URL link for One-API website')
    parser.add_argument('--oneapi_token', type=str, required=False, help='Token for One-API website')
    parser.add_argument('--oneapi_channel_url', type=str, required=False, help='Base url for One-API channel')

    args = parser.parse_args()
    number = args.number
    max_workers = args.max_workers
    use_oneapi = args.oneapi
    oneapi_url = args.oneapi_url
    oneapi_token = args.oneapi_token
    oneapi_channel_url = args.oneapi_channel_url

    print(f"[Register] Start to register {number} accounts in {max_workers} threads")
    account_infos = register_cursor(number, max_workers)
    tokens = list(set([row['token'] for row in account_infos]))
    print(f"[Register] Register {len(tokens)} accounts successfully")
    
    if use_oneapi and len(account_infos) > 0:
        from tokenManager.oneapi_manager import OneAPIManager
        from tokenManager.cursor import Cursor
        oneapi = OneAPIManager(oneapi_url, oneapi_token)

        # Send request by batch to avoid "Too many SQL variables" error in SQLite.
        # If you use MySQL, better to set the batch_size as len(tokens)
        batch_size = 10
        for idx, i in enumerate(range(0, len(tokens), batch_size), start=1):
            batch = tokens[i:i + batch_size]
            response = oneapi.add_channel("Cursor",
                                          oneapi_channel_url,
                                          '\n'.join(batch),
                                          Cursor.models)
            print(f'[OneAPI] Add Channel Request For Batch {idx}. Status Code: {response.status_code}, Response Body: {response.json()}')
