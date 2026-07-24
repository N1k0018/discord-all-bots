import discord
from discord.ext import commands
import os
import json
from datetime import datetime, timedelta
from locales import LANGUAGES, get_user_lang

ROLLER = {
    "UFC-live": 1525780352679809125,
    "ROK-rise of kingdoms": 1525779899745308712,
    "Steam-alıcı": 1510649566972870767,
    "Sohbet": 1486012917324185600
}

DATA_FILE = "user_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"rol_data": {}}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

USER_DATA = load_data()

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(USER_DATA, f, ensure_ascii=False, indent=2)

# Dilə uyğun mətnlər lüğəti
ROL_METNLERI = {
    "az": {
        "title": "🎭 Rol Seçim Paneli",
        "desc": "Zəhmət olmasa aşağıdakı menyudan rolunuzu seçin.",
        "placeholder": "Rolünü seç...",
        "success": "✅ {rol} rolü uğurla verildi!",
        "cooldown": "❌ Rol değiştirmek için 3 gün beklemen gerekiyor.",
        "not_yours": "❌ Bu menyu sənə aid deyil!"
    },
    "tr": {
        "title": "🎭 Rol Seçim Paneli",
        "desc": "Lütfen aşağıdaki menüden rolünüzü seçin.",
        "placeholder": "Rolünü seç...",
        "success": "✅ {rol} rolü başarıyla verildi!",
        "cooldown": "❌ Rol değiştirmek için 3 gün beklemen gerekiyor.",
        "not_yours": "❌ Bu menü sana ait değil!"
    },
    "en": {
        "title": "🎭 Role Selection Panel",
        "desc": "Please select your role from the menu below.",
        "placeholder": "Select your role...",
        "success": "✅ Successfully assigned role: {rol}!",
        "cooldown": "❌ You must wait 3 days to change your role.",
        "not_yours": "❌ This menu is not for you!"
    },
    "es": {
        "title": "🎭 Panel de Selección de Roles",
        "desc": "Por favor seleccione su rol del menú de abajo.",
        "placeholder": "Seleccione su rol...",
        "success": "✅ ¡Rol asignado exitosamente: {rol}!",
        "cooldown": "❌ Debes esperar 3 días para cambiar tu rol.",
        "not_yours": "❌ ¡Este menú no es para ti!"
    },
    "fr": {
        "title": "🎭 Panneau de Sélection des Rôles",
        "desc": "Veuillez sélectionner votre rôle dans le menu ci-dessous.",
        "placeholder": "Sélectionnez votre rôle...",
        "success": "✅ Rôle attribué avec succès : {rol} !",
        "cooldown": "❌ Vous devez attendre 3 jours pour changer de rôle.",
        "not_yours": "❌ Ce menu n'est pas pour vous !"
    },
    "ru": {
        "title": "🎭 Панель выбора ролей",
        "desc": "Пожалуйста, выберите свою роль из меню ниже.",
        "placeholder": "Выберите роль...",
        "success": "✅ Роль успешно назначена: {rol}!",
        "cooldown": "❌ Вы должны подождать 3 дня, чтобы сменить роль.",
        "not_yours": "❌ Это меню не для вас!"
    },
    "de": {
        "title": "🎭 Rollenauswahl-Panel",
        "desc": "Bitte wählen Sie Ihre Rolle aus dem Menü unten.",
        "placeholder": "Wähle deine Rolle...",
        "success": "✅ Rolle erfolgreich zugewiesen: {rol}!",
        "cooldown": "❌ Du musst 3 Tage warten, um deine Rolle zu ändern.",
        "not_yours": "❌ Dieses Menü ist nicht für dich!"
    },
    "ar": {
        "title": "🎭 لوحة اختيار الأدوار",
        "desc": "يرجى اختيار دورك من القائمة أدناه.",
        "placeholder": "اختر دورك...",
        "success": "✅ تم تعيين الدور بنجاح: {rol}!",
        "cooldown": "❌ يجب عليك الانتظار 3 أيام لتغيير دورك.",
        "not_yours": "❌ هذه القائمة ليست لك!"
    }
}

class RolSelectView(discord.ui.View):
    def __init__(self, user_id, lang_code):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.lang_code = lang_code
        texts = ROL_METNLERI.get(lang_code, ROL_METNLERI["en"])
        
        select = discord.ui.Select(
            placeholder=texts["placeholder"],
            custom_id="ephemeral_role_select",
            options=[discord.SelectOption(label=n, value=str(i)) for n, i in ROLLER.items()]
        )
        select.callback = self.role_callback
        self.add_item(select)

    async def role_callback(self, interaction: discord.Interaction):
        texts = ROL_METNLERI.get(self.lang_code, ROL_METNLERI["en"])
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(texts["not_yours"], ephemeral=True)
            return

        user_id_str = str(interaction.user.id)
        state = USER_DATA["rol_data"].setdefault(user_id_str, {"first_made": False, "last_time": None})

        if state["first_made"] and state["last_time"]:
            last_time = datetime.fromisoformat(state["last_time"])
            if datetime.now() - last_time < timedelta(days=3):
                await interaction.response.send_message(texts["cooldown"], ephemeral=True)
                return

        yeni_rol = interaction.guild.get_role(int(interaction.data["values"][0]))
        await interaction.user.add_roles(yeni_rol)

        state["first_made"] = True
        state["last_time"] = datetime.now().isoformat()
        save_data()

        await interaction.response.send_message(texts["success"].format(rol=yeni_rol.name), ephemeral=True)

class RolMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_menus = {}

    async def send_rolmenu_to_user(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_lang = get_user_lang(user_id)
        texts = ROL_METNLERI.get(user_lang, ROL_METNLERI["en"])
        
        embed = discord.Embed(
            title=texts["title"],
            description=texts["desc"],
            color=0x87CEEB
        )

        view = RolSelectView(user_id, user_lang)

        # Əgər əvvəl açıq menyu varsa silirik
        if user_id in self.active_menus:
            try:
                await self.active_menus[user_id].delete()
            except:
                pass

        # İstifadəçinin seçdiyi dildə və yalnız ona özəl (ephemeral) olaraq göndəririk
        if interaction.response.is_done():
            msg = await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            msg = await interaction.original_response()
            
        self.active_menus[user_id] = msg

    @commands.command()
    async def rolmenu(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        # !rolmenu yazanda da birbaşa istifadəçinin dilində açılır
        class DummyInteraction:
            def __init__(self, ctx):
                self.user = ctx.author
                self.client = ctx.bot
                self.response = ctx.channel # fallback
            async def followup_send(self, *args, **kwargs):
                return await ctx.send(*args, **kwargs)
        
        # Sadə simulyasiya ilə göndəririk
        user_id = ctx.author.id
        user_lang = get_user_lang(user_id)
        texts = ROL_METNLERI.get(user_lang, ROL_METNLERI["en"])
        embed = discord.Embed(title=texts["title"], description=texts["desc"], color=0x87CEEB)
        view = RolSelectView(user_id, user_lang)
        msg = await ctx.send(embed=embed, view=view)
        self.active_menus[user_id] = msg

async def setup(bot):
    await bot.add_cog(RolMenu(bot))
