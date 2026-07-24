import discord
from discord.ext import commands
from locales import LANGUAGES, set_user_lang

# rok.py faylından modal və rol lüğətini birbaşa çağırırıq
from cogs.rok import NicknameModal, ROK_METNLERI, RoKBot

class DilRokSelectView(discord.ui.View):
    def __init__(self, bot):
        # timeout=None edirik ki, menyu heç vaxt vaxtaşırı bağlanmasın (həmişə açıq qalsın)
        super().__init__(timeout=None)
        self.bot = bot
        
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
            # 1. Seçilən dili botun yaddaşında qeyd edirik
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # 2. Menyunu BAĞLAMIRİK (view=self saxlayırıq), sadəcə təsdiq mətni göstəririk
            await interaction.response.edit_message(
                content=f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                view=self 
            )
            
            # 3. Dil seçilən kimi AVTO-OLARAQ rok.py-dəki qeydiyyat modalını açırıq
            rok_cog = interaction.client.get_cog("RoKBot")
            if rok_cog:
                role_dict = rok_cog.ROLE_IDS
            else:
                # Əgər cog tapılmazsa defolt rollar
                role_dict = {
                    "Infantry": 1526342009596547142,
                    "Cavalry": 1526341870899298426,
                    "Archery": 1526342056430141440,
                    "Siege": 1526342109983014942
                }
            
            texts = ROK_METNLERI.get(lang_code, ROK_METNLERI["en"])
            
            # İstədiyin kimi dil seçilən kimi avtomatik rok.py modalı açılır
            await interaction.response.send_modal(NicknameModal(role_dict, texts, interaction.user.id))

        return button_callback

class DilRok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Bot yenidən işə düşəndə menyunun aktiv qalması üçün qeydiyyata alırıq
        self.bot.add_view(DilRokSelectView(bot))

    @commands.command(name="dilrok")
    async def dilrok_command(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        view = DilRokSelectView(self.bot)
        # Menyu göndərilir və sən özün silənə qədər həmişə açıq/yerində qalır
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(DilRok(bot))
