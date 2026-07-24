import discord
from discord.ext import commands
import os

DATA = {
    "piyade": {
        "open-field": [("sun_tzu.png", "bai_qi.png", "piyade_alan_ekipman.png"), ("bai_qi.png", "liu_che.png", "piyade_alan_ekipman.png"), ("sun_tzu.png", "liu_che.png", "piyade_alan_ekipman.png"), ("scipio.png", "liu_che.png", "piyade_alan_ekipman.png"), ("ragnar.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "scipio.png", "piyade_alan_ekipman.png"), ("liu_che.png", "alexander.png", "piyade_alan_ekipman.png")],
        "rally": [("scipio_aemilianus.png", "ivar.png", "piyade_rally_ekipman.png"), ("scipio_aemilianus.png", "charles_martel.png", "piyade_rally_ekipman.png"), ("charles_martel.png", "harald.png", "piyade_rally_ekipman.png")],
        "garnizon": [("gorgo.png", "tokugawa.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "cheo_yeong.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "heraclius.png", "piyade_garnizon_ekipman.png"), ("gorgo.png", "hector.png", "piyade_garnizon_ekipman.png")]
    },
    "suvari": {
        "open-field": [("gang_ghamchan.png", "achilleus.png", "suvari_alan_ekipman.png"), ("arthur.png", "achilleus.png", "suvari_alan_ekipman.png"), ("achilleus.png", "gang_ghamchan.png", "suvari_alan_ekipman.png"), ("arthur.png", "huo_qubing.png", "suvari_alan_ekipman.png"), ("attila.png", "achilleus.png", "suvari_alan_ekipman.png")],
        "rally": [("attila.png", "subutai.png", "suvari_rally_ekipman.png"), ("attila.png", "achilleus.png", "suvari_rally_ekipman.png"), ("attila.png", "charles_martel.png", "suvari_rally_ekipman.png")],
        "garnizon": [("elanor.png", "heraclius.png", "suvari_garnizon_ekipman.png")]
    },
    "okcu": {
        "open-field": [("qin_shi.png", "zhuge.png", "okcu_alan_ekipman.png"), ("alparslan.png", "hermann.png", "okcu_alan_ekipman.png"), ("qin_shi.png", "ysg.png", "okcu_alan_ekipman.png"), ("zhuge.png", "hermann.png", "okcu_alan_ekipman.png")],
        "rally": [("shapur.png", "ashurbanipal.png", "okcu_rally_ekipman.png")],
        "garnizon": [("hayam.png", "heraclius.png", "okcu_garnizon_ekipman.png"), ("hayam.png", "cheo_yeong.png", "okcu_garnizon_ekipman.png"), ("cheo_yeong.png", "heraclius.png", "okcu_garnizon_ekipman.png")]
    },
    "mix": {
        "garnizon": [("lapu_lapu.png", "mathias.png", "mix_garnizon_ekipman.png"), ("mathias.png", "lapu_lapu.png", "mix_garnizon_ekipman.png"), ("mathias.png", "heraclius.png", "mix_garnizon_ekipman.png"), ("heraclius.png", "mathias.png", "mix_garnizon_ekipman.png")]
    }
}


class NextButton(discord.ui.Button):
    def __init__(self, kategori, tip, index):
        super().__init__(label="Next", style=discord.ButtonStyle.primary)
        self.kategori = kategori
        self.tip = tip
        self.index = index

    async def callback(self, interaction: discord.Interaction):
        view = StratejiView(self.kategori, self.tip, self.index)
        await view.send_page(interaction)


class StratejiView(discord.ui.View):
    def __init__(self, kategori, tip=None, index=0):
        super().__init__(timeout=None)
        self.kategori = kategori
        self.tip = tip
        self.index = index
        self.kombinasyonlar = DATA.get(kategori, {}).get(tip, []) if tip else []

    async def gonder(self, interaction, tip):
        self.tip = tip
        self.kombinasyonlar = DATA.get(self.kategori, {}).get(tip, [])
        self.index = 0
        await self.send_page(interaction)

    async def send_page(self, interaction):
        if not self.kombinasyonlar or self.index >= len(self.kombinasyonlar):
            return
        k1, k2, ekipman = self.kombinasyonlar[self.index]
        mesaj = f"**{self.kategori.upper()} - {self.tip.upper()} ({self.index + 1}/{len(self.kombinasyonlar)})**\n{k1.replace('.png','').replace('_',' ')} + {k2.replace('.png','').replace('_',' ')}"
        files = []
        for dosya in [ekipman, k1, k2]:
            if os.path.exists(f"gorseller/{dosya}"):
                files.append(discord.File(f"gorseller/{dosya}"))

        view = StratejiView(self.kategori, self.tip, self.index + 1)
        if self.index + 1 < len(self.kombinasyonlar):
            view.add_item(NextButton(self.kategori, self.tip, self.index + 1))
        else:
            view.add_item(discord.ui.Button(label="End of List", style=discord.ButtonStyle.secondary, disabled=True))

        if interaction.response.is_done():
            await interaction.followup.send(content=mesaj, files=files, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(content=mesaj, files=files, view=view, ephemeral=True)

    @discord.ui.button(label="Open-Field", style=discord.ButtonStyle.primary)
    async def open_field(self, i, b):
        await self.gonder(i, "open-field")

    @discord.ui.button(label="Rally", style=discord.ButtonStyle.danger)
    async def rally(self, i, b):
        await self.gonder(i, "rally")

    @discord.ui.button(label="Garnizon", style=discord.ButtonStyle.success)
    async def garnizon(self, i, b):
        await self.gonder(i, "garnizon")


class Strateji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def piyade(self, ctx):
        await ctx.message.delete()
        await ctx.send("Seçim yap:", view=StratejiView("piyade"))

    @commands.command()
    async def okcu(self, ctx):
        await ctx.message.delete()
        await ctx.send("Seçim yap:", view=StratejiView("okcu"))

    @commands.command()
    async def suvari(self, ctx):
        await ctx.message.delete()
        await ctx.send("Seçim yap:", view=StratejiView("suvari"))

    @commands.command()
    async def mix(self, ctx):
        await ctx.message.delete()
        await ctx.send("Seçim yap:", view=StratejiView("mix"))


async def setup(bot):
    await bot.add_cog(Strateji(bot))