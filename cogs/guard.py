import discord
import asyncio
from discord.ext import commands

class Guard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bekleme_listesi = {}

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # 2 saat (7200 saniye) boyunca bekleme listesine al
        self.bekleme_listesi[member.id] = asyncio.create_task(asyncio.sleep(7200))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id in self.bekleme_listesi:
            try:
                await member.kick(reason="2 saatlik yeniden giriş kuralı.")
            except:
                pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def affet(self, ctx, user_id: int):
        await ctx.message.delete()
        if user_id in self.bekleme_listesi:
            self.bekleme_listesi[user_id].cancel()
            del self.bekleme_listesi[user_id]
            await ctx.send(f"✅ {user_id} ID'li kullanıcı affedildi.", delete_after=5)
        else:
            await ctx.send("❌ Kullanıcı zaten bekleme listesinde değil.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Guard(bot))