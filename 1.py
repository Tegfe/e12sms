import os
import re
import glob
import shutil
import subprocess

# 定义ANSI转义序列以显示粗体文本
BOLD = "\033[1m"
END = "\033[0m"

# 提示用户脚本将执行的操作
print("将自动为您执行以下操作：")
print(f"{BOLD}1. 安装unzip组件{END}")
print(f"{BOLD}2. 创建sms文件夹{END}")
print(f"{BOLD}3. 下载SmsForward{END}")
print(f"{BOLD}4. 创建systemctl{END}")
print(f"{BOLD}5. 清理临时zip文件{END}")
print(f"{BOLD}6. 设置PushPlusToken{END}")

# 执行操作 1
print(f"{BOLD}执行中：1. 安装unzip组件{END}")
subprocess.run(["apt", "update"])
subprocess.run(["apt", "install", "wget", "unzip", "-y"])

# 执行操作 2
print(f"{BOLD}执行中：2. 创建sms文件夹{END}")
os.makedirs("/sms")
os.chdir("/sms")

# 执行操作 3
print(f"{BOLD}执行中：3. 下载SmsForward{END}")
subprocess.run(["curl", "-LOJ", "-o", "/sms/DbusSmsForward.zip",
                "https://gitdl.cn/https://raw.githubusercontent.com/lkiuyu/DbusSmsForward/master/%E5%8F%91%E5%B8%83/DbusSmsForward.zip"])
os.makedirs("/sms/forward")
subprocess.run(["unzip", "DbusSmsForward.zip", "-d", "/sms/forward"])
subprocess.run(["chmod", "+x", "/sms/forward/DbusSmsForward"])

# 执行操作 4
print(f"{BOLD}执行中：4. 创建systemctl{END}")
subprocess.run(["curl", "-LOJ", "-o", "/sms/sms.zip",
                "https://gitdl.cn/https://raw.githubusercontent.com/Clunky1546/RES/main/sms.py"])
subprocess.run(["unzip", "/sms/sms.zip"])
shutil.move("/sms/sms.service", "/etc/systemd/system/")
shutil.move("/sms/sim.service", "/etc/systemd/system/")
subprocess.run(["systemctl", "enable", "sms.service"])
subprocess.run(["systemctl", "enable", "sim.service"])

# 执行操作 5
print(f"{BOLD}执行中：5. 清理临时zip文件{END}")
for zip_file in glob.glob("/sms/*.zip"):
    os.remove(zip_file)

# 执行操作 6
print(f"{BOLD}执行中：6. 设置PushPlusToken{END}")
while True:
    push_plus_token = input("请输入您的 PushPlusToken: ")
    if push_plus_token:
        save_choice = input("要保存修改吗？(y/n): ")
        if save_choice == "y":
            config_file = "/sms/forward/DbusSmsForward.dll.config"
            if os.path.isfile(config_file):
                with open(config_file, "r") as file:
                    config_data = file.read()
                    # 使用re.sub进行正则表达式替换
                    updated_data = re.sub(
                        r"<add key=\"pushPlusToken\" value=\"[^\"]*\" />",
                        f"<add key=\"pushPlusToken\" value=\"{push_plus_token}\" />",
                        config_data
                    )
                with open(config_file, "w") as file:
                    file.write(updated_data)
                print(f"PushPlusToken 已成功设置为: {push_plus_token}")
                break
            else:
                print(f"配置文件 {config_file} 不存在，请确保文件存在。")
        elif save_choice == "n":
            print("未保存修改，重新输入 PushPlusToken。")
        else:
            print("无效的选择，请输入 'y' 或 'n'。")
    else:
        print("未提供有效的 PushPlusToken，请重新输入。")

print(f"{BOLD}恭喜您，所有操作已完成。{END}")

# 倒计时 5 秒，然后重启系统
print(f"{BOLD}将在 5 秒后重启系统...{END}")
import time
time.sleep(5)
subprocess.run(["reboot"])