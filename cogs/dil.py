import discord
from discord.ext import commands
from locales import LANGUAGES, get_user_lang, set_user_lang

# Dillerin Discord-dakı rol ID-ləri (Sənin kodundakı ID-lər)
DILLER_ROLE_IDS = {
    "az": 1526232723029758073,
    "tr": 1526233376678481920,
    "en": 1526233442616868974,
    "es": 1526233508610310256,
    "fr": 1526233568043602062,
    "ru": 1526275300738990133,
    "de": 1526275400194592778,
    "ar": 1526233633650901132,
}

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
            # 1. İstifadəçinin üzərindəki köhnə dil rollarını tapıb silirik
            eski_dil_rol_idleri = list(DILLER_ROLE_IDS.values())
            eski_roller = [r for r in interaction.user.roles if r.id in eski_dil_rol_idleri]
            if eski_roller:
                await interaction.user.remove_roles(*eski_roller)

            # 2. Seçdiyi yeni dilin rolunu serverdən tapıb istifadəçiyə veririk
            yeni_rol_id = DILLER_ROLE_IDS.get(lang_code)
            if yeni_rol_id:
                yeni_rol = interaction.guild.get_role(yeni_rol_id)
                if yeni_rol:
                    await interaction.user.add_roles(yeni_rol)

            # 3. Botun daxili yaddaşındakı dili yeniləyirik
            set_user_lang(interaction.user.id, lang_code)
            lang_data = LANGUAGES[lang_code]
            
            # 4. Menyunu bağlamadan mətnini yeniləyirik
            await interaction.response.edit_message(
                content=f"✅ **{lang_data['name']}**{lang_data['lang_selected']}", 
                view=self
            )
            
            # 5. Rol menyusunu dərhal seçilən dildə çağırırıq
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
