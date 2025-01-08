import requests
import re
import json
import time
import random
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore

# 初始化颜色
init(autoreset=True)

# 全局请求头
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
}

# 保存解密结果
RESULTS = []


# 随机生成文件名
def generate_random_filename():
    return f"results_{random.randint(1000, 9999)}.txt"


# 各解密接口函数
def md5online(md5):
    url = "https://www.md5online.org/md5-decrypt.html"
    data = "hash=" + md5
    try:
        response = requests.post(url, data=data, headers=HEADERS, timeout=10)
        if "limegreen" in response.text:
            match = re.search(r"<b>(.*?)</b>", response.text)
            if match:
                return match.group(1)
    except Exception:
        pass
    return None


def bugbank(md5):
    url = "https://www.bugbank.cn/api/md5"
    data = "md5text=" + md5
    try:
        response = requests.post(url, data=data, headers=HEADERS, timeout=10)
        result = json.loads(response.text)
        if "answer" in result:
            return result["answer"]
    except Exception:
        pass
    return None


def gongjuji(md5):
    url = f"http://md5.gongjuji.net/common/md5dencrypt?UpperCase={md5}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        result = json.loads(response.text)
        if result.get("status") == 1:
            return result["data"]["PlainText"]
    except Exception:
        pass
    return None


def hashtoolkit(md5):
    url = f"https://hashtoolkit.com/reverse-hash/?hash={md5}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        match = re.search(r"<span title=\"decrypted md5 hash\">(.*?)</span>", response.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def my_addr(md5):
    url = "http://md5.my-addr.com/md5_decrypt-md5_cracker_online/md5_decoder_tool.php"
    data = f"md5={md5}&x=16&y=15"
    try:
        response = requests.post(url, data=data, headers=HEADERS, timeout=10)
        match = re.search(r"Hashed string</span>: (.*?)</div>", response.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def gromweb(md5):
    url = f"https://md5.gromweb.com/?md5={md5}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        match = re.search(r"<em class=\"long-content string\">(.*?)</em>", response.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def nitrxgen(md5):
    url = f"http://www.nitrxgen.net/md5db/{md5}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


def tellyou(md5):
    url = "http://md5.tellyou.top/MD5Service.asmx/HelloMd5"
    data = f"Ciphertext={md5}"
    try:
        response = requests.post(url, data=data, headers=HEADERS, timeout=10)
        match = re.search(r"<string xmlns=\"http://tempuri.org/\">(.*?)</string>", response.text)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


# 新增接口：md5decrypt.net
def md5decrypt(md5):
    api_key = "your_api_key"  # 替换为你的 API 密钥
    email = "your_email@example.com"  # 替换为你的邮箱
    url = f"https://md5decrypt.net/en/Api/api.php?hash={md5}&hash_type=md5&email={email}&code={api_key}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.text and "ERROR" not in response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


# 新增接口：hashkiller.co.uk
def hashkiller(md5):
    url = f"https://hashkiller.co.uk/md5/{md5}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.text:
            return response.text.strip()
    except Exception:
        pass
    return None


# 查询 MD5 的主逻辑
def query_md5(md5):
    # 所有接口函数列表
    modules = [
        md5online, bugbank, gongjuji, hashtoolkit, my_addr,
        gromweb, nitrxgen, tellyou, md5decrypt, hashkiller
    ]

    for module in modules:
        try:
            result = module(md5)
            if result:
                return f"{Fore.GREEN}[+] {module.__name__} MD5值：{md5} 已查到解密值：{result}"
        except Exception as e:
            print(f"{Fore.RED}[-] 模块 {module.__name__} 查询失败: {e}")
        # 每次查询后随机延迟 1-5 秒
        time.sleep(random.uniform(1, 5))
    return f"{Fore.YELLOW}[-] MD5值：{md5} 未查到解密值"


# 主函数
def main():
    # 读取 input.txt 文件
    input_file = "input.txt"
    if not os.path.exists(input_file):
        print(f"{Fore.RED}文件 {input_file} 不存在！")
        return

    with open(input_file, "r") as f:
        md5_list = [line.strip() for line in f.readlines() if line.strip()]

    # 生成随机输出文件名
    output_file = generate_random_filename()
    print(f"{Fore.CYAN}解密结果将保存到: {output_file}")

    # 使用进度条显示整体进度
    with open(output_file, "w") as f_out:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(query_md5, md5): md5 for md5 in md5_list}
            for future in tqdm(futures, desc="解密进度", total=len(md5_list), unit="hash"):
                result = future.result()
                RESULTS.append(result)
                f_out.write(result + "\n")
                print(result)

    print(f"{Fore.GREEN}解密完成，结果已保存到 {output_file}")


if __name__ == "__main__":
    main()
