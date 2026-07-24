import discord
from discord.ext import commands
from locales import LANGUAGES, get_user_lang, set_user_lang

class LanguageSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        for code, data in LANGUAGES.items():
            button = discord.ui.Button(
                label=data["name"].split(" ")[1],
                emoji=data["name"].split(" ")[0],
                style=discord.ButtonStyle.secondary,
                custom_id=f"lang_btn_{code}"
            )
            button.callback = self.create_callback(code)
            self.add_item(button)

    def create_callback(self, lang_code):
        async def button_callback(interaction: discord.Interaction):
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # Dil seçilən kimi istifadəçiyə bildiririk
            await interaction.response.send_message(
                f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                ephemeral=True
            )
            
            # VƏ AVTOMATİK OLARAK HƏMİN ÇATƏ ROL MENYUNU GÖNDƏRİRİK (seçdiyi dildə)
            # Burada birbaşa rolmenu funksiyasını çağırırıq
            cog = interaction.client.get_cog("RolMenu")
            if cog:
                await cog.send_rolmenu_to_user(interaction)

        return button_callback

class DilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(LanguageSelectView())

    @commands.command(name="dil")
    async def dil_command(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        view = LanguageSelectView()
        # Yuxarıda heç bir yazı yazmırıq, sadəcə view (düymələr) göndəririk
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(DilCog(bot))
