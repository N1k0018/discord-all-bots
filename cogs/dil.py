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
            # 1. Köhnə dil rollarını təmizləyirik (əgər varsa)
            # DİQQƏT: locales.py və ya rolmenu.py-dəki dil rollarının ID-ləridir
            LANG_ROLE_IDS = [
                1526232723029758073, 1526233376678481920, 1526233442616868974,
                1526233508610310256, 1526233568043602062, 1526275300738990133,
                1526275400194592778, 1526233733752033411, 1526233677053562890,
                1526233633650901132
            ]
            eski_diller = [r for r in interaction.user.roles if r.id in LANG_ROLE_IDS]
            if eski_diller:
                await interaction.user.remove_roles(*eski_diller)

            # 2. Yeni dili yadda saxlayırıq
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # 3. İstifadəçiyə bildiriş göndəririk
            await interaction.response.send_message(
                f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                ephemeral=True
            )
            
            # 4. Rol menyusunu çağırırıq (rolmenu.py özü artıq köhnə menyunu avtomatik silir)
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
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(DilCog(bot))
