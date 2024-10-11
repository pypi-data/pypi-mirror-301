import random


def 生成随机ChromeUA():
    """
    动态生成一个随机的 Windows 10 或 Windows 11 的 Chrome 浏览器 User-Agent。

    返回值:
        返回一个随机生成的 Windows 10 或 Windows 11 的 Chrome 浏览器 User-Agent。
        如果生成过程中出现错误，返回一个默认的 User-Agent。
    """
    try:
        windows_versions = ["Windows NT 10.0", "Windows NT 11.0"]  # Windows 10 和 11
        chrome_versions = ["114.0.5735", "113.0.5672", "112.0.5615", "111.0.5563",
                           "110.0.5481", "109.0.5414", "108.0.5359", "107.0.5304",
                           "106.0.5249", "105.0.5195", "104.0.5112", "103.0.5060"]  # 常见 Chrome 版本
        build_numbers = range(50, 150)  # 随机生成的构建号，例如 114.0.5735.**110**

        # 随机选择 Windows 版本、Chrome 版本和构建号
        windows_version = random.choice(windows_versions)
        chrome_version = random.choice(chrome_versions)
        build_number = random.choice(build_numbers)

        # 生成 User-Agent
        ua = f"Mozilla/5.0 ({windows_version}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.{build_number} Safari/537.36"

        return ua

    except Exception:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"