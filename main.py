import os
import requests
import random
import json
from datetime import datetime, date
from colorama import init, Fore
from discord_webhook import DiscordWebhook, DiscordEmbed
from keep_alive import keep_alive
from dateutil import parser
import time
import asyncio

keep_alive()
init()

with open("usg.txt", "w") as usg_file:
    pass

with open("osg.txt", "w") as osg_file:
    pass

webhook_url = os.environ.get("webhook")

num_users = 10000000

users_info = []

verified_item_links = ["https://www.roblox.com/catalog/102611803/Verified-Hat", "https://www.roblox.com/catalog/1567446/Verified-Sign"]

async def main():
    for _ in range(num_users):
        f = random.randint(20000000, 75000000)

        try:
            req = requests.get(f"http://users.roblox.com/v1/users/{f}", timeout=5)
            if req.status_code == 200:
                data = req.json()
                doc = data.get("created", "") or ""
                name = data.get("name", "")
                description = data.get("description", "") 

                if not data.get("isBanned", False):
                    user_ids = [data["id"]]
                    presence_url = "https://presence.roblox.com/v1/presence/last-online"
                    payload = {"userIds": user_ids}
                    headers = {"Content-Type": "application/json"}
                    try:
                        presence_response = requests.post(presence_url, data=json.dumps(payload), headers=headers, timeout=5)
                        presence_data = presence_response.json()
                        last_online_timestamps = presence_data.get("lastOnlineTimestamps", [])

                        if len(last_online_timestamps) > 0:
                            last_online = last_online_timestamps[0].get("lastOnline", "")
                            created_date = parser.isoparse(doc).strftime("<t:%s:D>")
                            account_age = (date.today() - parser.isoparse(doc).date()).days

                            try:
                                last_online_date = datetime.strptime(last_online, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("<t:%s:D>")
                            except ValueError:
                                last_online_date = datetime.strptime(last_online, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("<t:%s:D>")

                            id = data["id"]
                            req2 = requests.get(
                                f"https://thumbnails.roblox.com/v1/users/avatar?userIds={id}&size=420x420&format=Png&isCircular=false",
                                timeout=5,
                            )
                            avatar_data = req2.json()
                            avatar_url = avatar_data["data"][0]["imageUrl"]

                            req3 = requests.get(
                                f"https://inventory.roblox.com/v2/users/{id}/items/asset/collectibles?sortOrder=Asc&limit=100",
                                timeout=5,
                            )
                            info = req3.json()
                            items = info.get("data", [])
                            item_links = [item.get("link", "") for item in items]

                            verified_status = "False"

                            if any(item_link in item_links for item_link in verified_item_links):
                                if all(item_link in item_links for item_link in verified_item_links):
                                    verified_status = "Hat/Sign"
                                elif "https://www.roblox.com/catalog/1567446/Verified-Sign" in item_links:
                                    verified_status = "Sign"
                                elif "https://www.roblox.com/catalog/102611803/Verified-Hat" in item_links:
                                    verified_status = "Hat"

                            req4 = requests.get(
                                f"https://inventory.roblox.com/v1/users/{id}/assets/collectibles?limit=10&sortOrder=Asc",
                                timeout=5,
                            )
                            info = req4.text
                            data2 = json.loads(info)
                            rbx = data2.get("data", [])
                            recent_average_prices = [item.get("recentAveragePrice", 0) for item in rbx]
                            total_sum = sum(recent_average_prices)

                            is_email_verified = "Hat" if data.get("isEmailVerified", False) else "False"

                            if total_sum > 0:
                                value = f"[{total_sum}](https://www.rolimons.com/player/{id})"
                                rap = f"[{total_sum}](https://www.rolimons.com/player/{id})"

                                output = f"[{name}](https://www.roblox.com/users/{id}/profile)\n\n**ID**\n{id}\n\n**Verified:** {verified_status}\n\n**Account Age**\n{account_age} days\n\n**Rap**\n{rap}\n\n**Value**\n{value}\n\n**Created**\n{created_date}\n\n**Last Online**\n{last_online_date}\n\n**Description**\n{description}"
                                print(Fore.GREEN + output)

                                with open("osg.txt", "a") as osg_file:
                                    osg_file.write(f"{output}\n")

                                users_info.append({"output": output, "id": id})

                                webhook = DiscordWebhook(url=webhook_url)
                                embed = DiscordEmbed(
                                    title=name,
                                    description=output,
                                )
                                embed.set_thumbnail(url=avatar_url)
                                webhook.add_embed(embed)
                                webhook.execute()

                            else:
                                output = f"[{name}](https://www.roblox.com/users/{id}/profile)\n\n**ID**\n{id}\n\n**Verified:** False\n\n**Account Age**\n{account_age} days\n\n**Rap**\n{rap}\n\n**Value**\n{value}\n\n**Created**\n{created_date}\n\n**Last Online**\n{last_online_date}\n\n**Description**\n{description}"  # Updated line to include user description
                                print(Fore.RED + output)

                                with open("usg.txt", "a") as usg_file:
                                    usg_file.write(f"{output}\n")

                    except Exception as e:
                        print(Fore.YELLOW + "An error occurred:", str(e))

        except Exception as e:
            print(Fore.YELLOW + "An error occurred:", str(e))

    if users_info:
        webhook = DiscordWebhook(url=webhook_url)
        for user_info in users_info:
            output = user_info["output"]
            user_id = user_info["id"]

            embed = DiscordEmbed(title="User Information", description=output, color=242424)
            embed.add_embed_field(name="User ID", value=user_id)
            avatar_url = "https://tr.rbxcdn.com/a2cee91750570bd692bc0540b60eb4fb/352/352/Avatar/Png"
            embed.set_thumbnail(url=avatar_url)
            webhook.add_embed(embed)
            webhook.execute()
    else:
        print("No accounts found.")

# Made By Just_InScripts#0001
# If you're using the code, please DM me and give me credit :)

asyncio.run(main())
