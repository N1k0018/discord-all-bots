import discord
from discord.ext import commands
from locales import LANGUAGES, get_user_lang, set_user_lang

class LanguageSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Düymələrin daimi işləməsi üçün
        
        for code, data in LANGUAGES.items():
            button = discord.ui.Button(
                label=data["name"].split(" ")[1], # Dilin adı (məs: Azərbaycanca)
                emoji=data["name"].split(" ")[0], # Bayraq emoji
                style=discord.ButtonStyle.secondary,
                custom_id=f"lang_btn_{code}"
            )
            button.callback = self.create_callback(code)
            self.add_item(button)

    def create_callback(self, lang_code):
        async def button_callback(interaction: discord.Interaction):
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # İstifadəçiyə yalnız onun özünün görəcəyi təsdiq mesajı (ephemeral)
            await interaction.response.send_message(
                f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                ephemeral=True
            )
        return button_callback

class DilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(LanguageSelectView())

    @commands.command(name="dil")
    async def dil_command(self, ctx):
        # İstifadəçinin yazdığı !dil mesajını silirik ki, kanal təmiz qalsın
        try:
            await ctx.message.delete()
        except:
            pass
        
        user_lang = get_user_lang(ctx.author.id)
        menu_text = LANGUAGES[user_lang]["menu_title"]
        
        view = LanguageSelectView()
        # Menyunu kanala göndəririk (bunu istədiyin vaxt yaza bilərsən)
        await ctx.send(menu_text, view=view)

async def setup(bot):
    await bot.add_cog(DilCog(bot))