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

class RolSelectView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=180) # 3 dəqiqə sonra sönür
        self.user_id = user_id
        
        # Rol seçimi üçün dropdown
        select = discord.ui.Select(
            placeholder="Rolünü seç / Select your role...",
            custom_id="ephemeral_role_select",
            options=[discord.SelectOption(label=n, value=str(i)) for n, i in ROLLER.items()]
        )
        select.callback = self.role_callback
        self.add_item(select)

    async def role_callback(self, interaction: discord.Interaction):
        # Yalnız menyunu çağıran istifadəçi bu düymələrə/menyulara toxuna bilsin
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Bu menyu sənə aid deyil!", ephemeral=True)
            return

        user_id_str = str(interaction.user.id)
        state = USER_DATA["rol_data"].setdefault(user_id_str, {"first_made": False, "last_time": None})

        if state["first_made"] and state["last_time"]:
            last_time = datetime.fromisoformat(state["last_time"])
            if datetime.now() - last_time < timedelta(days=3):
                await interaction.response.send_message(
                    "❌ Rol değiştirmek için 3 gün beklemen gerekiyor.", ephemeral=True)
                return

        yeni_rol = interaction.guild.get_role(int(interaction.data["values"][0]))
        await interaction.user.add_roles(yeni_rol)

        state["first_made"] = True
        state["last_time"] = datetime.now().isoformat()
        save_data()

        await interaction.response.send_message(f"✅ {yeni_rol.name} rolü verildi!", ephemeral=True)

class RolMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # İstifadəçinin əvvəlki menyu mesajını yadda saxlamaq üçün lüğət (silmək üçün)
        self.active_menus = {}

    @commands.command()
    async def rolmenu(self, ctx):
        # İstifadəçinin yazdığı !rolmenu əmrini dərhal silirik ki, kanal təmiz qalsın
        try:
            await ctx.message.delete()
        except:
            pass

        user_id = ctx.author.id
        user_lang = get_user_lang(user_id)
        
        # Seçilmiş dilə uyğun başlıq/açıqlama (locales.py-dən və ya buradakı lüğətdən ala bilərsən)
        embed = discord.Embed(
            title="Rol Seçim Paneli / Role Selection",
            description="Aşağıdakı menüden rolünüzü seçebilirsiniz. Bu mesaj sadece size özeldir ve 3 dakika sonra geçerliliğini yitirir.",
            color=0x87CEEB
        )

        view = RolSelectView(user_id)

        # Əgər həmin istifadəçinin daha əvvəl açıq bir menyusu qalıbsa, onu silməyə çalışırıq
        if user_id in self.active_menus:
            try:
                old_msg = self.active_menus[user_id]
                await old_msg.delete()
            except:
                pass

        # Yeni menyunu yalnız həmin istifadəçiyə özəl (ephemeral) olaraq göndəririk
        message = await ctx.send(embed=embed, view=view, ephemeral=True)
        self.active_menus[user_id] = message

async def setup(bot):
    await bot.add_cog(RolMenu(bot))
