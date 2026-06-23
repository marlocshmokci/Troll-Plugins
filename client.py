from telethon import TelegramClient, events
import asyncio
import random
import re
import time
from datetime import datetime
from telethon.tl.functions.messages import ReportRequest

# === ТВОИ ДАННЫЕ ===
API_ID = 30436414
API_HASH = "b9b2df0bf5f5e14d75109a2dd419984b"
MY_USER_ID = 8857781669

SESSION = "my_session"

# СПИСОК ГРУПП (без минусов)
TARGET_CHAT_IDS = [
    1003888778733,
    1003881875724,
    1003875221776,
    1003867014436,
    1003839239195,
    1003798780223
]

# === ВАЛИДНЫЕ КЛЮЧИ (100 штук) ===
VALID_KEYS = [
    "ABC12-DEF34-GHI56-JKL78", "MN90P-QRS12-TUV34-WXY56", "ZAB78-CDE90-FGH12-IJK34",
    "LMN56-OPQ78-RST90-UVW12", "XYZ34-ABC56-DEF78-GHI90", "JKL12-MNO34-PQR56-STU78",
    "VWX90-YZA12-BCD34-EFG56", "HIJ78-KLM90-NOP12-QRS34", "TUV56-WXY78-ZAB90-CDE12",
    "FGH34-IJK56-LMN78-OPQ90", "RST12-UVW34-XYZ56-ABC78", "DEF90-GHI12-JKL34-MNO56",
    "PQR78-STU90-VWX12-YZA34", "BCD56-EFG78-HIJ90-KLM12", "NOP34-QRS56-TUV78-WXY90",
    "ZAB12-CDE34-FGH56-IJK78", "LMN90-OPQ12-RST34-UVW56", "XYZ78-ABC90-DEF12-GHI34",
    "JKL56-MNO78-PQR90-STU12", "VWX34-YZA56-BCD78-EFG90", "HIJ12-KLM34-NOP56-QRS78",
    "TUV90-WXY12-ZAB34-CDE56", "FGH78-IJK90-LMN12-OPQ34", "RST56-UVW78-XYZ90-ABC12",
    "DEF34-GHI56-JKL78-MNO90", "PQR12-STU34-VWX56-YZA78", "BCD90-EFG12-HIJ34-KLM56",
    "NOP78-QRS90-TUV12-WXY34", "ZAB56-CDE78-FGH90-IJK12", "LMN34-OPQ56-RST78-UVW90",
    "XYZ12-ABC34-DEF56-GHI78", "JKL90-MNO12-PQR34-STU56", "VWX78-YZA90-BCD12-EFG34",
    "HIJ56-KLM78-NOP90-QRS12", "TUV34-WXY56-ZAB78-CDE90", "FGH12-IJK34-LMN56-OPQ78",
    "RST90-UVW12-XYZ34-ABC56", "DEF78-GHI90-JKL12-MNO34", "PQR56-STU78-VWX90-YZA12",
    "BCD34-EFG56-HIJ78-KLM90", "NOP12-QRS34-TUV56-WXY78", "ZAB90-CDE12-FGH34-IJK56",
    "LMN78-OPQ90-RST12-UVW34", "XYZ56-ABC78-DEF90-GHI12", "JKL34-MNO56-PQR78-STU90",
    "VWX12-YZA34-BCD56-EFG78", "HIJ90-KLM12-NOP34-QRS56", "TUV78-WXY90-ZAB12-CDE34",
    "FGH56-IJK78-LMN90-OPQ12", "RST34-UVW56-XYZ78-ABC90", "DEF12-GHI34-JKL56-MNO78",
    "PQR90-STU12-VWX34-YZA56", "BCD78-EFG90-HIJ12-KLM34", "NOP56-QRS78-TUV90-WXY12",
    "ZAB34-CDE56-FGH78-IJK90", "LMN12-OPQ34-RST56-UVW78", "XYZ90-ABC12-DEF34-GHI56",
    "JKL78-MNO90-PQR12-STU34", "VWX56-YZA78-BCD90-EFG12", "HIJ34-KLM56-NOP78-QRS90",
    "TUV12-WXY34-ZAB56-CDE78", "FGH90-IJK12-LMN34-OPQ56", "RST78-UVW90-XYZ12-ABC34",
    "DEF56-GHI78-JKL90-MNO12", "PQR34-STU56-VWX78-YZA90", "BCD12-EFG34-HIJ56-KLM78",
    "NOP90-QRS12-TUV34-WXY56", "ZAB78-CDE90-FGH12-IJK34", "LMN56-OPQ78-RST90-UVW12",
    "XYZ34-ABC56-DEF78-GHI90", "JKL12-MNO34-PQR56-STU78", "VWX90-YZA12-BCD34-EFG56",
    "HIJ78-KLM90-NOP12-QRS34", "TUV56-WXY78-ZAB90-CDE12", "FGH34-IJK56-LMN78-OPQ90",
    "RST12-UVW34-XYZ56-ABC78", "DEF90-GHI12-JKL34-MNO56", "PQR78-STU90-VWX12-YZA34",
    "BCD56-EFG78-HIJ90-KLM12", "NOP34-QRS56-TUV78-WXY90", "ZAB12-CDE34-FGH56-IJK78",
    "LMN90-OPQ12-RST34-UVW56", "XYZ78-ABC90-DEF12-GHI34", "JKL56-MNO78-PQR90-STU12",
    "VWX34-YZA56-BCD78-EFG90", "HIJ12-KLM34-NOP56-QRS78", "TUV90-WXY12-ZAB34-CDE56",
    "FGH78-IJK90-LMN12-OPQ34", "RST56-UVW78-XYZ90-ABC12", "DEF34-GHI56-JKL78-MNO90",
    "PQR12-STU34-VWX56-YZA78", "BCD90-EFG12-HIJ34-KLM56", "NOP78-QRS90-TUV12-WXY34",
    "ZAB56-CDE78-FGH90-IJK12", "LMN34-OPQ56-RST78-UVW90", "XYZ12-ABC34-DEF56-GHI78",
    "JKL90-MNO12-PQR34-STU56", "VWX78-YZA90-BCD12-EFG34", "HIJ56-KLM78-NOP90-QRS12",
    "TUV34-WXY56-ZAB78-CDE90", "FGH12-IJK34-LMN56-OPQ78", "RST90-UVW12-XYZ34-ABC56"
]

# === ФРАЗЫ ===
PHRASES = [
    "малоимущая блядина ты тут плачь в халупу твоего пахана как ты любишь это делать дочь шалавы шалава ты же понимаешь что ты тут провокатор для члена твоего второго отца то есть тут чисто биологически",
    "ротика бесполезны перед мною своим богом ебырем который будем своим хуем проникать в пространство межног твоей мамаши ебаной свиноблядской шалавы и вытаскивать уже свой хуй я буду с её кишками которые я намажу по твоему ебальнику ебучему сынуля шлюхи ты жирный давай щас тёлка ебаная набирайся духу и отпиши мне тут хотяб больше 5 строек а не юзаю свой т9 который один хуй тебе не поможет сынчело шалавы я щас внатуре буду разъебывать своим членом твои кабины тут никому не всратые терпила ебаная ты че там решил сдаться сопляк ебаный или че я не пойму намотай все свои сопли на свой кулак и продолжай дальше сидеть сомной на фантазии а не страдать тут моих издевательств над тобой чисто запросто проломлю твой череп и повыбиваю нахуй",
    "полостью твои органы из спермы, ты внатцре здесь решил меня перебить я де тебе здесь до упора всажу хуй и заставлю прыгать как кенгуру",
    "она ничего не понимая дальше пошла ко мне ну стучит ко мне в дверь но как оказалось она сильно громко стучала на меня ну точнее громкость желанная мной превышала 1 децибел ну я ей за это полностью весь зубной состав выбил своим богоподобным половым агрегатом ну ясен хуй чтобы ей было проще мне сосать ну после чего же взял ее черепушку и проломил ее нахуй арматурой тем самым показал кто тут на самом деле настоящий хозяин а твой отец в свою очередь просто искал твою мать посколько она пропала ну искал по всем трассам ведь заранее знал кем твоя мать работает и что она просто готова напрыгнуть на член за жвачку и 6 копеек ну так он не нашел ее и вспомнил о моем существовании ведь когда-то ещё в 87 году я как-то приходил к твоей мамаше и просто насильно заставлял ее отдавать мне свое анальное",
    "маня провокации использовать я же в натуре нахуй тебя жалеть тут не буду как всегда в самое подходящее время я тебя тут отпинаю как псину и не более просто ебало свое нахуй не открывай мизоблядское подобное огрызкам которые зарождались для того чтобы тут пезденки полировать своим гнилозубым ротовым отверстием с банальной точки эрудиции если так думать то ты являешься второсортным сыном выебанной шлюхи",
    "отпиши внизу если твоя мамаша сдохла от спида затем передала тебе",
    "взмахом на другую точку галактике произойдёт что то иное и разрушится атмосфера нашей планеты которая защищает нас от не пристойных фаз которые пытаются пройти через воздушную атмосферу для атаки на наши живности я же тут тебе тупому сыну изверга перпендикулярного квадратика который состоит из особых усилий потому что он в системе твоей головы я же тебе тут сыну ебаного дерьма начну ебашить катаной специальной технической для таких случаев с твоей ебаной тушкой истребление твоего лиличеакого позвоночника который состоит из многочисленных дисковых конструкций в которых были всталены гвозди для того чтобы твое тупое неспособное ни к чему тело давало каких то действий и могло передвигаться я обеспечу твоей тушке отвинт данных гвоздей затем шприцом начну выкачивать из твоих позвонков жидкость",
    "придется нахуй уничтожить саму себе тебе ты ебаная нахуй подобная свинообразцам телочка тупоголовая ты внатуре тут блять родилась в надежде того что я не выебу тебе матушку ебаную нахуй ты понимаешь что я тупо на твоих глазах буду резать своим половым аргрегатом промежность твоей ебаной гнилозубой матери ты понимаешь что втои ебаные мелкоразвитые кутяпки против моего члена нахуй",
    "ебанат у кого-то каждое сообщение состоит из слов другие слова есть? Да они у тебя в анале застряли вытащи и себе в рот засунь, я думаю тебе стоит купить себе мозги, ведь ты решил тягаться с умнейшим человеком,в моих словах ты будешь буквально плыть, тоесть набор моих слов тебе никогда не перебить, как ты не понимаешь я тебе огрызку здесь шанс даю чтобы не ливнул от сюда позором, а ты продолжаешь нести неформалые и глупые фразы, на которым всем обсолютно поебать, ты блевота которая никому не интересна,ты интересен только бомжу, ну и для него ты сыграешь роль, будешь отсасывателем хуев, но в прочем твоя повседневная работа уже с той даты когда ты родился, но когда ты родился никому не интересно",
    "еблище ты понимаешь что тебе не сможет помочь даже родная твоя матушка ебаная терпилойдная насадочная блядина на мой половой орган",
    "слышь сынок шалавы принимай напор спермы в своё ебадо как ты это любишь делать я внатуре щас аригатного пидораса тебя выебу во все оставшиеся дырки которая твоя мать шлюханка ежедневно покрывает чтобы",
    "собачье ебало пизда недоразвитое вообще не понимаю хуле вообще родилась хуеплет ебаная ты мне хотя бы часа игнора не покажи или ты слабая и непослушная сучка которая сосет всем пизду?мать твоя шалава мать твою ебал сучка ебаная я тебя видел в клубе с мужиками ты им отсосасывала за 15р чтобы прокормить ребенка и всю свою родню а я же забыл я же их всем зубы выбил и тд желаю тебе бомжатничать отвечаю нахуй я тебя блять побрею блять налысо хуета ебаная подзалупная проститутка тут базарить я вырежу твое еблицо и буду использовать как футбольный мяч и пинать тебя нахуй буду никчемушная да кому ты блять сдалась?тебя отчим будет ебать в пилотку пизда ебаная твоя базарная мамаша упала от моего огромного члена который больше чем у твоих мертвых отцов они по очереди разминали твое очко как у ебаной",
    "понимаеш что ты не способен отбить и едниного моего хпрчка который был вьебан тебе в товй ожирневший пиздак который я разширил своим царским агрегатом жалуий сынк шалавы который был выебан",
    "мумифицированым отцом дигроидное свиное еблище которое способно питать жидкость с моего хуя и задыхаться без моего троста как ингалятора",
    "вафляжуйка ебаная недопустимо слабоумное дите шлюханской чертивной аригатки и не более насадочная залупская лярвообразная дегенеративная жиробаска омерзительная противопоказанная для социализация"
]

# === ПЕРЕМЕННЫЕ ===
activated = False
attack_history = {}
MAX_HISTORY = 15
auto_reply_enabled = True
reply_delay_ms = 100
reply_delay = reply_delay_ms / 1000
messages_sent = 0
active_attacks = {}
start_time = time.time()
stop_attack = False

client = TelegramClient(SESSION, API_ID, API_HASH)

def get_random_phrase_for_attack(chat_id, target_user_id):
    key = (chat_id, target_user_id)
    history = attack_history.get(key, [])
    available = [p for p in PHRASES if p not in history]
    if not available:
        history.clear()
        available = PHRASES.copy()
    phrase = random.choice(available)
    history.append(phrase)
    if len(history) > MAX_HISTORY:
        history.pop(0)
    attack_history[key] = history
    return phrase

# === ФУНКЦИЯ ФЕЙКОВОЙ ЗАГРУЗКИ ===
async def fake_loading(event, key):
    messages = [
        "проверяю наличие ключа в своей базе данных....",
        "проверяю наличие ключа по определённой ссылке.....",
        "устанавливаю ключ.........",
        "инициализация доступа...."
    ]
    
    for msg in messages:
        await asyncio.sleep(1.5)
        await event.reply(msg)
    
    for i in range(1, 101):
        if i <= 25:
            bar = "█" * (i // 4) + "▒" * (25 - i // 4)
            symbols = "*" * (i // 4) + " " * (25 - i // 4)
        elif i <= 50:
            bar = "█" * (i // 4) + "▒" * (25 - i // 4)
            symbols = "***" * (i // 4) + " " * (50 - i // 4)
        elif i <= 75:
            bar = "█" * (i // 4) + "▒" * (25 - i // 4)
            symbols = "*****" * (i // 4) + " " * (75 - i // 4)
        else:
            bar = "█" * (i // 4) + "▒" * (25 - i // 4)
            symbols = "*******" * (i // 4) + " " * (100 - i // 4)
        
        if i % 5 == 0 or i == 100:
            await event.reply(f"{i}%.......{bar} {symbols}")
        
        await asyncio.sleep(0.5)
    
    random_code = ''.join(random.choices('1234567890,;:{}[]()%&', k=15))
    await event.reply(f"✅ SUCCESSFUL DOWNLOAD KEYS {{{{{{{{random_code}}}}}}}}")
    await event.reply("🔓 ДОСТУП ОТКРЫТ! Теперь команды работают.")
    return True

@client.on(events.NewMessage(chats=TARGET_CHAT_IDS))
async def handler(event):
    global activated, auto_reply_enabled, reply_delay_ms, reply_delay, messages_sent, stop_attack
    chat_id = event.chat_id

    if event.out and event.raw_text.startswith('.'):
        command = event.raw_text.lower().strip()

        # === .key ===
        if command.startswith('.key '):
            if activated:
                await event.reply("⚠️ Плагин уже активирован.")
                return
            
            key = command[5:].strip().upper()
            if key in VALID_KEYS:
                # Запускаем фейковую загрузку
                await fake_loading(event, key)
                activated = True
            else:
                await event.reply("❌ Неверный ключ. Получите ключ в канале:\nhttps://t.me/esdaltourna/14")
            return

        # === БЛОКИРОВКА КОМАНД ДО АКТИВАЦИИ ===
        if not activated:
            blocked_commands = ['.trep', '.tgk', '.вв', '.ввмс', '.ро.+', '.ро.-', '.ор', '.офф', '.пинг', '.обв']
            if any(command.startswith(cmd) for cmd in blocked_commands):
                await event.reply("🔒 ДОСТУП ЗАБЛОКИРОВАН\n\nВведите ключ активации:\n.key [ключ]\n\nПолучить ключ: https://t.me/esdaltourna/14")
                return

        # === .понг (не блокируется) ===
        if command == '.понг':
            await event.reply("пинг 🏓")
            return

        # === .trep / .tgk ===
        if command == '.trep' or command == '.tgk':
            if command == '.trep':
                menu = """
[ Список команд ]

.key [ключ] - активировать плагин
.вв [1-10] - установить скорость (сообщ/сек)
.ввмс [1-1000] - установить задержку в мс
.ро.+ - включить автоответ
.ро.- - выключить автоответ
.ор - атаковать цель (в ответ на сообщение)
.офф - остановить атаку в чате
.пинг - проверить пинг плагина
.понг - ответить пинг
.tgk - ссылка на канал с плагинами
.обв [число] - обработка данных (1-500)

Текущая задержка: {delay} мс
Отправлено сообщений: {sent}
Активных атак: {attacks}
Автоответ: {status}
"""
                await event.reply(menu.format(
                    delay=reply_delay_ms,
                    sent=messages_sent,
                    attacks=len(active_attacks),
                    status='ВКЛЮЧЕН' if auto_reply_enabled else 'ВЫКЛЮЧЕН'
                ))
            else:
                await event.reply(
                    "все плагины, начиная от тролля и вредоносных заканчивая полезными только тут.\nhttps://t.me/+qqhOQsEYbXs2N2Y6"
                )
            return

        # === .вв ===
        if command.startswith('.вв '):
            try:
                new_speed = int(command.split()[1])
                if 1 <= new_speed <= 10:
                    reply_delay_ms = int(1000 / new_speed)
                    reply_delay = reply_delay_ms / 1000
                    await event.reply(f"Скорость установлена: {new_speed} сообщ/сек (задержка {reply_delay_ms} мс)")
                else:
                    await event.reply("Ошибка: скорость должна быть от 1 до 10")
            except:
                await event.reply("Ошибка: используй .вв [число]")
            return

        # === .ввмс ===
        if command.startswith('.ввмс '):
            try:
                new_delay = int(command.split()[1])
                if 1 <= new_delay <= 1000:
                    reply_delay_ms = new_delay
                    reply_delay = reply_delay_ms / 1000
                    await event.reply(f"Задержка установлена: {reply_delay_ms} мс")
                else:
                    await event.reply("Ошибка: задержка должна быть от 1 до 1000 мс")
            except:
                await event.reply("Ошибка: используй .ввмс [число]")
            return

        # === .ро.+ ===
        if command == '.ро.+':
            if not auto_reply_enabled:
                auto_reply_enabled = True
                await event.reply("Автоответ включен")
            else:
                await event.reply("Автоответ уже включен")
            return

        # === .ро.- ===
        if command == '.ро.-':
            if auto_reply_enabled:
                auto_reply_enabled = False
                await event.reply("Автоответ выключен")
            else:
                await event.reply("Автоответ уже выключен")
            return

        # === .пинг ===
        if command == '.пинг':
            try:
                start = time.time()
                await client.send_message(chat_id, "ping")
                ping_ms = int((time.time() - start) * 1000)
                
                if ping_ms < 500:
                    status = "отлично"
                elif ping_ms < 1000:
                    status = "хорошо"
                elif ping_ms < 2000:
                    status = "средне"
                else:
                    status = "критично"
                
                await event.reply(f"Пинг: {ping_ms} мс - {status}")
            except Exception as e:
                await event.reply(f"Ошибка при измерении пинга: {e}")
            return

        # === .ор ===
        if command == '.ор':
            if event.reply_to:
                try:
                    replied_msg = await event.get_reply_message()
                    if replied_msg and not replied_msg.out:
                        if hasattr(replied_msg.from_id, 'user_id'):
                            target_user_id = replied_msg.from_id.user_id
                        else:
                            target_user_id = replied_msg.from_id
                        active_attacks[(chat_id, target_user_id)] = True
                        stop_attack = False
                        attack_key = (chat_id, target_user_id)
                        if attack_key in attack_history:
                            attack_history[attack_key] = []
                        phrase = get_random_phrase_for_attack(chat_id, target_user_id)
                        await send_ladder(chat_id, phrase, replied_msg.id)
                        await event.reply(f"Атака на пользователя {target_user_id} начата! Используй .офф для остановки.")
                    else:
                        await event.reply("Ответь на сообщение цели.")
                except Exception as e:
                    await event.reply(f"Ошибка: {e}")
            else:
                await event.reply(".ор должна быть ответом на сообщение цели.")
            return

        # === .офф ===
        if command == '.офф':
            stop_attack = True
            stopped = False
            keys_to_remove = [key for key in active_attacks.keys() if key[0] == chat_id]
            for key in keys_to_remove:
                del active_attacks[key]
                stopped = True
            await asyncio.sleep(0.5)
            if stopped:
                await event.reply("Все атаки в этом чате принудительно остановлены.")
            else:
                await event.reply("Активных атак в этом чате нет.")
            return

        # === .обв ===
        if command.startswith('.обв'):
            try:
                parts = command.split()
                count = 100
                if len(parts) > 1:
                    count = int(parts[1])
                    if count < 1 or count > 500:
                        await event.reply("Ошибка: число должно быть от 1 до 500")
                        return
                else:
                    count = 100
                
                await event.reply(f"Обработка запроса...")
                
                messages = []
                async for msg in client.iter_messages(chat_id, limit=count):
                    if msg and not msg.out:
                        messages.append(msg)
                
                if not messages:
                    await event.reply("Нет данных для обработки.")
                    return
                
                sent = 0
                for i, msg in enumerate(messages[:count]):
                    try:
                        await client(ReportRequest(
                            peer=chat_id,
                            id=[msg.id],
                            reason=2
                        ))
                        sent += 1
                        print(f"[ОБВ] Прогресс: {sent}/{len(messages[:count])} ({int(sent/len(messages[:count])*100)}%)")
                        await asyncio.sleep(0.3)
                    except Exception as e:
                        print(f"[ОБВ] Ошибка: {e}")
                
                await event.reply(f"✅ Готово. Обработано: {sent}")
                print(f"[ОБВ] Завершено. Обработано: {sent}")
                
            except Exception as e:
                await event.reply(f"❌ Ошибка: {e}")
                print(f"[ОБВ] Критическая ошибка: {e}")
            return

    # === ГЛОБАЛЬНЫЙ АВТООТВЕТ ===
    if not event.out and auto_reply_enabled and activated:
        phrase = random.choice(PHRASES)
        await send_ladder(chat_id, phrase, event.id)

    # === АТАКА .ор ===
    if not event.out and activated:
        if hasattr(event.from_id, 'user_id'):
            from_id = event.from_id.user_id
        else:
            from_id = event.from_id

        if (chat_id, from_id) in active_attacks and active_attacks[(chat_id, from_id)]:
            phrase = get_random_phrase_for_attack(chat_id, from_id)
            await send_ladder(chat_id, phrase, event.id)

async def send_ladder(chat_id, phrase, reply_to_msg=None):
    global messages_sent, stop_attack
    words = phrase.split()
    
    for word in words:
        if stop_attack:
            print("Атака принудительно остановлена")
            stop_attack = False
            return
        try:
            if reply_to_msg:
                await client.send_message(chat_id, word, reply_to=reply_to_msg)
            else:
                await client.send_message(chat_id, word)
            messages_sent += 1
            await asyncio.sleep(reply_delay)
        except Exception as e:
            print(f"Ошибка: {e}")
    
    for _ in range(random.randint(1, 3)):
        if stop_attack:
            stop_attack = False
            return
        word = random.choice(words)
        try:
            if reply_to_msg:
                await client.send_message(chat_id, word, reply_to=reply_to_msg)
            else:
                await client.send_message(chat_id, word)
            messages_sent += 1
            await asyncio.sleep(reply_delay)
        except Exception as e:
            print(f"Ошибка: {e}")

# === ТРИГГЕРЫ ДЛЯ ЛС ===
TRIGGER_WORDS = [
    "хуесос",
    "э слышь",
    "пидор",
    "сын бляди",
    "сучка",
    "безмамный",
    "я твою мать ебал"
]

@client.on(events.NewMessage)
async def private_handler(event):
    if event.is_private:
        if event.out:
            return
        text = event.raw_text.lower()
        for word in TRIGGER_WORDS:
            if word.lower() in text:
                phrase = random.choice(PHRASES)
                await send_ladder(event.chat_id, phrase, event.id)
                break

async def main():
    global activated
    await client.start()
    print(f"Бот запущен в {len(TARGET_CHAT_IDS)} группах")
    print(f"ID: {MY_USER_ID}")
    print(f"Текущая задержка: {reply_delay_ms} мс")
    print("🔒 Для активации введите .key [ключ] в любой группе")
    print("🔑 Ключи: https://t.me/esdaltourna/14")
    print("Команды: .trep .вв .ввмс .ро.+ .ро.- .пинг .понг .ор .офф .tgk .обв")
    print("Нажмите Ctrl+C для выхода")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Выход...")
