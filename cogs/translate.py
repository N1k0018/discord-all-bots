import discord
from discord.ext import commands
from deep_translator import GoogleTranslator

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LANG_ROLES = {
            1526232723029758073: "az", 1526233376678481920: "tr", 1526233442616868974: "en",
            1526233508610310256: "es", 1526233568043602062: "fr", 1526275300738990133: "ru",
            1526275400194592778: "de", 1526233733752033411: "zh-CN", 1526233677053562890: "hi",
            1526233633650901132: "ar",
        }
        self.LANG_LABELS = {
            "az": {"user_msg": "İstifadəçi Mesajı", "translation": "Tərcümə"},
            "tr": {"user_msg": "Kullanıcı Mesajı", "translation": "Çeviri"},
            "en": {"user_msg": "User Message", "translation": "Translation"},
            "es": {"user_msg": "Mensaje del Usuario", "translation": "Traducción"},
            "fr": {"user_msg": "Message de l'Utilisateur", "translation": "Traduction"},
            "ru": {"user_msg": "Сообщение пользователя", "translation": "Перевод"},
            "de": {"user_msg": "Benutzernachricht", "translation": "Übersetzung"},
            "zh-CN": {"user_msg": "用户消息", "translation": "翻译"},
            "hi": {"user_msg": "उपयोगकर्ता संदेश", "translation": "अनुवाद"},
            "ar": {"user_msg": "رسالة المستخدم", "translation": "الترجمة"},
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.content and not message.content.startswith("!"):
            await message.add_reaction("🌐")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot or str(reaction.emoji) != "🌐": return
        message = reaction.message
        lang = next((self.LANG_ROLES[r.id] for r in user.roles if r.id in self.LANG_ROLES), "en")
        labels = self.LANG_LABELS.get(lang, self.LANG_LABELS["en"])
        try:
            t = GoogleTranslator(source="auto", target=lang).translate(message.content)
            embed = discord.Embed(color=discord.Color.blue())
            embed.add_field(name=f"🔵 {labels['user_msg']}", value=f"{message.author.mention}: {message.content}", inline=False)
            embed.add_field(name=f"📖 {labels['translation']}", value=f"{t}", inline=False)
            await user.send(embed=embed)
        except Exception as e:
            print(f"Çeviri hatası: {e}")

async def setup(bot):
    await bot.add_cog(Translate(bot))