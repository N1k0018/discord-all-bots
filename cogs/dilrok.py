import discord
from discord.ext import commands
from locales import LANGUAGES, set_user_lang

class DilRokSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        for code, data in LANGUAGES.items():
            button = discord.ui.Button(
                label=data["name"].split(" ")[1],
                emoji=data["name"].split(" ")[0],
                style=discord.ButtonStyle.secondary,
                custom_id=f"dilrok_btn_{code}"
            )
            button.callback = self.create_callback(code)
            self.add_item(button)

    def create_callback(self, lang_code):
        async def button_callback(interaction: discord.Interaction):
            # Seçilən dili botun yaddaşında qeyd edirik
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # Menyunu heç vaxt bağlamırıq (view=self), sadəcə təsdiq mesajı veririk
            await interaction.response.edit_message(
                content=f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                view=self
            )
        return button_callback

class DilRok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Bot yenidən işə düşəndə daimi menyunun aktiv qalması üçün
        self.bot.add_view(DilRokSelectView())

    @commands.command(name="dilrok")
    async def dilrok_command(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        view = DilRokSelectView()
        # Daimi olaraq qalacaq dil menyusunu göndəririk
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(DilRok(bot))
