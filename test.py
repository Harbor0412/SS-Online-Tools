import asyncio
from aiocoap import Context, Message, Code
from aiocoap.credentials import CredentialsMap, DTLS

# ====== 配置区 ======
COAPS_SERVER = 'coaps://192.168.66.253:5684/v1/whoami'  # 服务器URI
# COAPS_SERVER = 'coaps://192.168.66.253:5684/'  # 服务器URI
PSK = b'\x16\x87$\x82\xa3\xb31\xdd*\x94r8\xa3\xf0\xe8\xae'  # 预共享密钥（bytes）
IDENTITY = b'MC1234567890AB'  # 身份标识（bytes）
# ====================

async def main():
    # 配置凭据
    credentials = CredentialsMap({
        'coaps://192.168.66.253:5684/*': DTLS(psk=PSK, client_identity=IDENTITY)
    })
    # 创建CoAPS上下文，传入凭据
    protocol = await Context.create_client_context()
    protocol.client_credentials = credentials

    # 构造请求
    request = Message(code=Code.GET, uri=COAPS_SERVER)
    try:
        response = await protocol.request(request).response
        print(f"Response Code: {response.code}")
        print(f"Response Payload: {response.payload.decode()}")
        await protocol.shutdown()
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    asyncio.run(main())