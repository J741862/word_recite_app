# app/sms.py

def send_sms(to: str, message: str):
    # 仅在控制台打印，不调用任何外部服务
    print(f"[Stub SMS] 发送短信到 {to}：{message}")
