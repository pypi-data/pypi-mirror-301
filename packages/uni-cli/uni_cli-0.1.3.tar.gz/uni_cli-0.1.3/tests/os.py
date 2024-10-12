import platform


def get_os_type():
    os_type = platform.system()
    if os_type == "Windows":
        return "当前操作系统是 Windows"
    elif os_type == "Darwin":
        return "当前操作系统是 macOS"
    elif os_type == "Linux":
        return "当前操作系统是 Linux"
    else:
        return "无法识别的操作系统"


if __name__ == "__main__":
    print(platform.system())
