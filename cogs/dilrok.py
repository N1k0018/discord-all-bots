import discord
from discord.ext import commands
from locales import LANGUAGES, set_user_lang
from cogs.rok import NicknameModal, ROK_METNLERI

# Hər dilə uyğun qeydiyyat düyməsi mətnləri
REGISTER_BUTTON_TEXTS = {
    "az": "📝 RoK Qeydiyyatını Başlat",
    "tr": "📝 RoK Kaydını Başlat",
    "en": "📝 Start RoK Registration",
    "es": "📝 Iniciar Registro RoK",
    "fr": "📝 Commencer l'inscription RoK",
    "ru": "📝 Начать регистрацию RoK",
    "de": "📝 RoK-Registrierung starten",
    "ar": "📝 بدء تسجيل RoK"
}

class DynamicRegisterView(discord.ui.View):
    def __init__(self, role_dict, lang_texts, lang_code, btn_label):
        super().__init__(timeout=None)
        self.role_dict = role_dict
        self.lang_texts = lang_texts
        self.lang_code = lang_code
        self.btn_label = btn_label

    @discord.ui.button(label="Placeholder", style=discord.ButtonStyle.primary, custom_id="dynamic_rok_register_btn")
    async def reg_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Düyməyə basan kimi birbaşa həmin dildə modal açılır
        await interaction.response.send_modal(NicknameModal(self.role_dict, self.lang_texts, interaction.user.id))

    def update_button_label(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button) and child.custom_id == "dynamic_rok_register_btn":
                child.label = self.btn_label

class DilRokSelectView(discord.ui.View):
    def __init__(self, bot):
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
            # 1. Dili yadda saxlayırıq
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # 2. Dil menyusu silinmir, yerində qalır
            await interaction.response.edit_message(
                content=f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                view=self
            )
            
            # 3. rok.py-dən rolları alırıq
            rok_cog = interaction.client.get_cog("RoKBot")
            role_dict = rok_cog.ROLE_IDS if rok_cog else {
                "Infantry": 1526342009596547142,
                "Cavalry": 1526341870899298426,
                "Archery": 1526342056430141440,
                "Siege": 1526342109983014942
            }
            
            texts = ROK_METNLERI.get(lang_code, ROK_METNLERI["en"])
            btn_label = REGISTER_BUTTON_TEXTS.get(lang_code, REGISTER_BUTTON_TEXTS["en"])
            
            # 4. Seçilən dildə dinamik qeydiyyat düyməsini mesaj olaraq göndəririk
            view = DynamicRegisterView(role_dict, texts, lang_code, btn_label)
            view.update_button_label()
            
            await interaction.followup.send(content=texts.get("ctx_message", "Register:"), view=view, ephemeral=True)

        return button_callback

class DilRok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(DilRokSelectView(bot))

    @commands.command(name="dilrok")
    async def dilrok_command(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        view = DilRokSelectView(self.bot)
        # Menyu həmişə açıq şəkildə göndərilir
        await ctx.send(view=view)

async def setup(bot):
    await bot.add_cog(DilRok(bot))
