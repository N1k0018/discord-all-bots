import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
import json
from locales import get_user_lang

DATA_FILE = "rok_cooldowns.json"

def load_cooldowns():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_cooldowns(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

ROK_METNLERI = {
    "az": {
        "modal_title": "RoK Qeydiyyat",
        "modal_label": "Oyun isminiz?",
        "modal_response": "İsim güncellendi! Birlikleri seçin:",
        "select_placeholder": "Birlikləri seçin...",
        "success": "✅ Güncellendi: {roles}",
        "no_roles": "Hiçbir birlik seçilmedi.",
        "not_yours": "❌ Bu menyu sənə aid deyil!",
        "cooldown": "❌ Yenidən qeydiyyatdan keçmək üçün 3 dəqiqə gözləməlisən."
    },
    "tr": {
        "modal_title": "RoK Kayıt",
        "modal_label": "Oyun isminiz?",
        "modal_response": "İsim güncellendi! Birlikleri seçin:",
        "select_placeholder": "Birlikleri seçin...",
        "success": "✅ Güncellendi: {roles}",
        "no_roles": "Hiçbir birlik seçilmedi.",
        "not_yours": "❌ Bu menü sana ait değil!",
        "cooldown": "❌ Tekrar kayıt olmak için 3 dakika beklemelisin."
    },
    "en": {
        "modal_title": "RoK Registration",
        "modal_label": "Your game name?",
        "modal_response": "Name updated! Select your units:",
        "select_placeholder": "Select units...",
        "success": "✅ Updated: {roles}",
        "no_roles": "No units selected.",
        "not_yours": "❌ This menu is not for you!",
        "cooldown": "❌ You must wait 3 minutes to register again."
    },
    "es": {
        "modal_title": "Registro RoK",
        "modal_label": "¿Tu nombre de usuario?",
        "modal_response": "¡Nombre actualizado! Selecciona tus unidades:",
        "select_placeholder": "Seleccionar unidades...",
        "success": "✅ Actualizado: {roles}",
        "no_roles": "Ninguna unidad seleccionada.",
        "not_yours": "❌ ¡Este menú no es para ti!",
        "cooldown": "❌ Debes esperar 3 minutos para registrarte de nuevo."
    },
    "fr": {
        "modal_title": "Inscription RoK",
        "modal_label": "Votre nom de jeu ?",
        "modal_response": "Nom mis à jour ! Sélectionnez vos unités :",
        "select_placeholder": "Sélectionner des unités...",
        "success": "✅ Mis à jour : {roles}",
        "no_roles": "Aucune unité sélectionnée.",
        "not_yours": "❌ Ce menu n'est pas pour vous !",
        "cooldown": "❌ Vous devez attendre 3 minutes pour vous réinscrire."
    },
    "ru": {
        "modal_title": "Регистрация RoK",
        "modal_label": "Ваше игровое имя?",
        "modal_response": "Имя обновлено! Выберите юниты:",
        "select_placeholder": "Выберите юниты...",
        "success": "✅ Обновлено: {roles}",
        "no_roles": "Юниты не выбраны.",
        "not_yours": "❌ Это меню не для вас!",
        "cooldown": "❌ Подождите 3 минуты перед повторной регистрацией."
    },
    "de": {
        "modal_title": "RoK-Registrierung",
        "modal_label": "Dein Spielname?",
        "modal_response": "Name aktualisiert! Wähle Einheiten aus:",
        "select_placeholder": "Einheiten auswählen...",
        "success": "✅ Aktualisiert: {roles}",
        "no_roles": "Keine Einheiten ausgewählt.",
        "not_yours": "❌ Dieses Menü ist nicht für dich!",
        "cooldown": "❌ Du musst 3 Minuten warten, um dich erneut zu registrieren."
    },
    "ar": {
        "modal_title": "تسجيل RoK",
        "modal_label": "اسم اللعبة الخاص بك؟",
        "modal_response": "تم تحديث الاسم! حدد الوحدات:",
        "select_placeholder": "حدد الوحدات...",
        "success": "✅ تم التحديث: {roles}",
        "no_roles": "لم يتم اختيار أي وحدة.",
        "not_yours": "❌ هذه القائمة ليست لك!",
        "cooldown": "❌ يجب عليك الانتظار 3 دقائق للتسجيل مرة أخرى."
    }
}

class RoleToggleSelect(discord.ui.Select):
    def __init__(self, role_dict, lang_texts, user_id):
        self.role_dict = role_dict
        self.lang_texts = lang_texts
        self.user_id = user_id
        options = [discord.SelectOption(label=name, value=str(rid)) for name, rid in role_dict.items()]
        super().__init__(placeholder=lang_texts["select_placeholder"], min_values=0, max_values=len(role_dict), options=options)
    
    async def callback(self, i: discord.Interaction):
        if i.user.id != self.user_id:
            await i.response.send_message(self.lang_texts["not_yours"], ephemeral=True)
            return

        selected_ids = [int(v) for v in self.values]
        all_role_ids = list(self.role_dict.values())
        
        remove_roles = [r for r in i.user.roles if r.id in all_role_ids]
        if remove_roles:
            await i.user.remove_roles(*remove_roles)
        
        add_roles = [i.guild.get_role(rid) for rid in selected_ids if i.guild.get_role(rid)]
        if add_roles:
            await i.user.add_roles(*add_roles)
        
        roles_str = ', '.join([r.name for r in add_roles]) if add_roles else self.lang_texts["no_roles"]
        msg = self.lang_texts["success"].format(roles=roles_str)
        await i.response.send_message(msg, ephemeral=True)

class NicknameModal(discord.ui.Modal):
    def __init__(self, role_dict, lang_texts, user_id):
        super().__init__(title=lang_texts["modal_title"])
        self.role_dict = role_dict
        self.lang_texts = lang_texts
        self.user_id = user_id
        
        self.isim = discord.ui.TextInput(label=lang_texts["modal_label"], required=True)
        self.add_item(self.isim)
    
    async def on_submit(self, i: discord.Interaction):
        await i.user.edit(nick=str(self.isim))
        view = discord.ui.View().add_item(RoleToggleSelect(self.role_dict, self.lang_texts, self.user_id))
        await i.response.send_message(self.lang_texts["modal_response"], view=view, ephemeral=True)

class RoKBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ROLE_IDS = {
            "Infantry": 1526342009596547142,
            "Cavalry": 1526341870899298426,
            "Archery": 1526342056430141440,
            "Siege": 1526342109983014942
        }

    @commands.command()
    async def kayit(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass
        
        user_id = str(ctx.author.id)
        user_lang = get_user_lang(ctx.author.id)
        texts = ROK_METNLERI.get(user_lang, ROK_METNLERI["en"])

        # 3 dəqiqəlik cooldown yoxlaması
        cooldowns = load_cooldowns()
        now = datetime.now()

        if user_id in cooldowns:
            last_time = datetime.fromisoformat(cooldowns[user_id])
            if now - last_time < timedelta(minutes=3):
                await ctx.send(texts["cooldown"], delete_after=5)
                return

        # Cooldown vaxtını yeniləyirik
        cooldowns[user_id] = now.isoformat()
        save_cooldowns(cooldowns)

        # İstifadəçinin qarşısına birbaşa düymə çıxır, basan kimi seçdiyi dildə modal açılır
        class DirectButtonView(discord.ui.View):
            def __init__(self, role_dict, lang_texts, author_id):
                super().__init__(timeout=60)
                self.role_dict = role_dict
                self.lang_texts = lang_texts
                self.author_id = author_id

            @discord.ui.button(label="📝 RoK Register", style=discord.ButtonStyle.primary)
            async def open_modal(self, interaction: discord.Interaction, button: discord.ui.Button):
                if interaction.user.id != self.author_id:
                    await interaction.response.send_message(self.lang_texts["not_yours"], ephemeral=True)
                    return
                await interaction.response.send_modal(NicknameModal(self.role_dict, self.lang_texts, interaction.user.id))

        view = DirectButtonView(self.ROLE_IDS, texts, ctx.author.id)
        btn_msg = "Registering..." if user_lang == "en" else "Qeydiyyat üçün tıkla..."
        await ctx.send(btn_msg, view=view, delete_after=60)

async def setup(bot):
    await bot.add_cog(RoKBot(bot))
