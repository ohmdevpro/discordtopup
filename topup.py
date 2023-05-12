import discord
import requests
import json

# Discord bot token
TOKEN = 'your-discord-bot-token'

# Create a Discord client
client = discord.Client()

class Topup:
    @staticmethod
    def giftcode(hash, phone):
        if hash is None or phone is None:
            return False

        hash = hash.replace("https://gift.truemoney.com/campaign/?v=", "")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        postData = {
            'mobile': phone,
            'voucher_hash': hash
        }
        response = requests.post(f"https://gift.truemoney.com/campaign/vouchers/{hash}/redeem", json=postData, headers=headers)
        result = response.json()
        return result

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$topup'):
        # Extract the mobile number and voucher server from the message content
        content = message.content.split(' ')
        mobile = content[1]
        voucher_server = content[2]

        # Perform the giftcode redemption
        tc = Topup()
        vc = tc.giftcode(voucher_server, mobile)

        if vc['status']['code'] == 'SUCCESS':
            amount = vc['data']['voucher']['amount_baht']
            info = f"ทำรายการจำนวน {amount} บาท"
            await message.channel.send(info)
        elif vc['status']['code'] == 'VOUCHER_NOT_FOUND':
            info = "ไม่พบซองของขวัญอั่งเปา"
            await message.channel.send(info)
        elif vc['status']['code'] == 'CANNOT_GET_OWN_VOUCHER':
            info = "คุณไม่สามารถใช้ของขวัญของคุณเองได้"
            await message.channel.send(info)
        elif vc['status']['code'] == 'TARGET_USER_NOT_FOUND':
            info = "หมายเลขโทรศัพท์ของผู้รับไม่ถูกต้อง"
            await message.channel.send(info)
        elif vc['status']['code'] == 'VOUCHER_OUT_OF_STOCK':
            info = "เสียใจด้วยของขวัญแจกหมดแล้ว"
            await message.channel.send(info)
        elif vc['status']['code'] == 'VOUCHER_EXPIRED':
            info = "ของขวัญหมดอายุ"
            await message.channel.send(info)
        elif vc['status']['code'] == 'INTERNAL_ERROR':
            info = "503 Internal error"
            await message.channel.send(info)
        else:
            info = "เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ"
            await message.channel.send(info)

# Run the Discord bot
client.run(TOKEN)
