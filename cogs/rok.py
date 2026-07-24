import discord
from discord.ext import commands
from locales import get_user_lang

ROK_METNLERI = {
    "az": {
        "modal_title": "RoK Qeydiyyat",
        "modal_label": "Oyun isminiz?",
        "modal_response": "İsim güncellendi! Birlikleri seçin:",
        "select_placeholder": "Birlikləri seçin...",
        "success": "✅ Güncellendi: {roles}",
        "no_roles": "Hiçbir birlik seçilmedi.",
        "not_yours": "❌ Bu menyu sənə aid deyil!"
    },
    "tr": {
        "modal_title": "RoK Kayıt",
        "modal_label": "Oyun isminiz?",
        "modal_response": "İsim güncellendi! Birlikleri seçin:",
        "select_placeholder": "Birlikleri seçin...",
        "success": "✅ Güncellendi: {roles}",
        "no_roles": "Hiçbir birlik seçilmedi.",
        "not_yours": "❌ Bu menü sana ait değil!"
    },
    "en": {
        "modal_title": "RoK Registration",
        "modal_label": "Your game name?",
        "modal_response": "Name updated! Select your units:",
        "select_placeholder": "Select units...",
        "success": "✅ Updated: {roles}",
        "no_roles": "No units selected.",
        "not_yours": "❌ This menu is not for you!"
    },
    "es": {
        "modal_title": "Registro RoK",
        "modal_label": "¿Tu nombre de usuario?",
        "modal_response": "¡Nombre actualizado! Selecciona tus unidades:",
        "select_placeholder": "Seleccionar unidades...",
        "success": "✅ Actualizado: {roles}",
        "no_roles": "Ninguna unidad seleccionada.",
        "not_yours": "❌ ¡Este menú no es für ti!"
    },
    "fr": {
        "modal_title": "Inscription RoK",
        "modal_label": "Votre nom de jeu ?",
        "modal_response": "Nom mis à jour ! Sélectionnez vos unités :",
        "select_placeholder": "Sélectionner des unités...",
        "success": "✅ Mis à jour : {roles}",
        "no_roles": "Aucune unité sélectionnée.",
        "not_yours": "❌ Ce menu n'est pas pour vous !"
    },
    "ru": {
        "modal_title": "Регистрация RoK",
        "modal_label": "Ваше игровое имя?",
        "modal_response": "Имя обновлено! Выберите юниты:",
        "select_placeholder": "Выберите юниты...",
        "success": "✅ Обновлено: {roles}",
        "no_roles": "Юниты не выбраны.",
        "not_yours": "❌ Это меню не для вас!"
    },
    "de": {
        "modal_title": "RoK-Registrierung",
        "modal_label": "Dein Spielname?",
        "modal_response": "Name aktualisiert! Wähle Einheiten aus:",
        "select_placeholder": "Einheiten auswählen...",
        "success": "✅ Aktualisiert: {roles}",
        "no_roles": "Keine Einheiten ausgewählt.",
        "not_yours": "❌ Dieses Menü ist nicht für dich!"
    },
    "ar": {
        "modal_title": "تسجيل RoK",
        "modal_label": "اسم اللعبة الخاص بك؟",
        "modal_response": "تم تحديث الاسم! حدد الوحدات:",
        "select_placeholder": "حدد الوحدات...",
        "success": "✅ تم التحديث: {roles}",
        "no_roles": "لم يتم اختيار أي وحدة.",
        "not_yours": "❌ هذه القائمة ليست لك!"
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

    async def trigger_registration(self, interaction: discord.Interaction, lang_code: str):
        texts = ROK_METNLERI.get(lang_code, ROK_METNLERI["en"])
        await interaction.response.send_modal(NicknameModal(self.ROLE_IDS, texts, interaction.user.id))

async def setup(bot):
    await bot.add_cog(RoKBot(bot))
