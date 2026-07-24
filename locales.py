LANGUAGES = {
    "az": {
        "name": "🇦🇿 Azərbaycanca",
        "menu_title": "🌐 **Dil Seçimi Menyusu**\n\nZəhmət olmasa aşağıdakı düymələrdən istifadə edərək öz dilinizi seçin:",
        "lang_selected": " uğurla seçildi! Artıq bütün menyular və bot cavabları bu dildə görünəcək.",
    },
    "tr": {
        "name": "🇹🇷 Türkçe",
        "menu_title": "🌐 **Dil Seçim Menüsü**\n\nLütfen aşağıdaki düğmeleri kullanarak dilinizi seçin:",
        "lang_selected": " başarıyla seçildi! Artık tüm menüler ve bot yanıtları bu dilde görünecek.",
    },
    "en": {
        "name": "🇬🇧 English",
        "menu_title": "🌐 **Language Selection Menu**\n\nPlease select your preferred language using the buttons below:",
        "lang_selected": " successfully selected! All menus and bot responses will now appear in this language.",
    },
    "es": {
        "name": "🇪🇸 Español",
        "menu_title": "🌐 **Menú de Selección de Idioma**\n\nPor favor, seleccione su idioma preferido usando los botones de abajo:",
        "lang_selected": " seleccionado con éxito! Todos los menús y respuestas aparecerán en este idioma.",
    },
    "fr": {
        "name": "🇫🇷 Français",
        "menu_title": "🌐 **Menu de Sélection de Langue**\n\nVeuillez sélectionner votre langue préférée en utilisant les boutons ci-dessous:",
        "lang_selected": " sélectionné avec succès ! Tous les menus et réponses apparaîtront dans cette langue.",
    },
    "ru": {
        "name": "🇷🇺 Русский",
        "menu_title": "🌐 **Меню выбора языка**\n\nПожалуйста, выберите предпочитаемый язык с помощью кнопок ниже:",
        "lang_selected": " успешно выбран! Теперь все меню и ответы будут отображаться на этом языке.",
    },
    "de": {
        "name": "🇩🇪 Deutsch",
        "menu_title": "🌐 **Sprachauswahlmenü**\n\nBitte wählen Sie Ihre bevorzugte Sprache über die Schaltflächen unten:",
        "lang_selected": " erfolgreich ausgewählt! Alle Menüs und Antworten werden nun in dieser Sprache angezeigt.",
    },
    "ar": {
        "name": "🇸🇦 العربية",
        "menu_title": "🌐 **قائمة اختيار اللغة**\n\nيرجى اختيار لغتك المفضلة باستخدام الأزرار أدناه:",
        "lang_selected": " تم اختياره بنجاح! ستظهر جميع القوائم الردود بهذه اللغة.",
    }
}

USER_LANGUAGES = {}

def get_user_lang(user_id: int) -> str:
    return USER_LANGUAGES.get(user_id, "az")

def set_user_lang(user_id: int, lang_code: str):
    USER_LANGUAGES[user_id] = lang_code
