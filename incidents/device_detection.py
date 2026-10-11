import re


def detect_device(user_agent):
    agent = (user_agent or "").lower()

    if "ipad" in agent or ("macintosh" in agent and "mobile" in agent):
        device_type = "iPad / tablet"
        operating_system = "iPadOS"
    elif "iphone" in agent:
        device_type = "iPhone"
        operating_system = "iOS"
    elif "android" in agent:
        device_type = "Android phone" if "mobile" in agent else "Android tablet"
        operating_system = "Android"
    elif "windows phone" in agent:
        device_type = "Windows phone"
        operating_system = "Windows Phone"
    elif "cros" in agent:
        device_type = "Laptop / desktop"
        operating_system = "ChromeOS"
    elif "windows" in agent:
        device_type = "Laptop / desktop"
        operating_system = "Windows"
    elif "macintosh" in agent or "mac os" in agent:
        device_type = "Laptop / desktop"
        operating_system = "macOS"
    elif "linux" in agent:
        device_type = "Laptop / desktop"
        operating_system = "Linux"
    else:
        device_type = "Unknown device"
        operating_system = "Unknown"

    if "edg/" in agent or "edge/" in agent:
        browser = "Microsoft Edge"
    elif "opr/" in agent or "opera" in agent:
        browser = "Opera"
    elif "firefox/" in agent:
        browser = "Firefox"
    elif "chrome/" in agent or "crios/" in agent:
        browser = "Google Chrome"
    elif "safari/" in agent:
        browser = "Safari"
    else:
        browser = "Unknown browser"

    return {
        "device_type": device_type,
        "operating_system": operating_system,
        "browser": browser,
    }
