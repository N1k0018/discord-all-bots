import discord
from discord.ext import commands
from discord.ui import Select, View, Button

# Buraya kendi kullanıcı ID'ni yazmalısın
MY_ID = 980764213683314739 

class SteamBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GAMES = [
            "Call of Duty: Modern Warfare", "Cyberpunk 2077", "Detroit: Become Human",
            "Dying Light", "EA SPORTS FC 25", "Elden Ring", "Frostpunk", "God of War",
            "God of War Ragnarök", "Marvel’s Spider-Man: Miles Morales", "Resident Evil Village",
            "Resident Evil 4", "Red Dead Redemption 2", "Rise of the Tomb Raider",
            "Shadow of the Tomb Raider", "Sons of the Forest", "The Last of Us part 1",
            "The Last of Us part 2", "The Witcher 3: Wild Hunt", "Tomb Raider"
        ]

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def oyunlar(self, ctx):
        await ctx.message.delete()
        
        class GameSelect(Select):
            def __init__(self, games):
                options = [discord.SelectOption(label=g) for g in games]
                super().__init__(placeholder="Oyun seç...", options=options)

            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_message("✅ Seçiminiz iletildi.", ephemeral=True)
                owner = await interaction.client.fetch_user(MY_ID)
                if owner:
                    embed = discord.Embed(title="🛒 Yeni Satış", color=discord.Color.gold())
                    embed.add_field(name="Kullanıcı", value=interaction.user.mention, inline=False)
                    embed.add_field(name="Oyun", value=self.values[0], inline=False)
                    view = View()
                    view.add_item(Button(label="Profil", url=f"https://discord.com/users/{interaction.user.id}"))
                    await owner.send(embed=embed, view=view)

        view = View(timeout=None)
        view.add_item(GameSelect(self.GAMES))
        await ctx.send("Lütfen bir oyun seçin:", view=view)

async def setup(bot):
    await bot.add_cog(SteamBot(bot))