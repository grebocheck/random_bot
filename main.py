import random

import settings
import telebot
from telebot import types
import users
import sharas
import winers_db
from datetime import datetime, timedelta
import import_json

bot = telebot.TeleBot(settings.TOKEN)

cance_text = "Відмінити"
markup = types.ReplyKeyboardMarkup()
cance_button = types.KeyboardButton(cance_text)
markup = markup.row(cance_button)

del_markup = types.ReplyKeyboardRemove()

markup_groups = types.ReplyKeyboardMarkup()
for a in import_json.group_list():
    markup_groups.row(a)
markup_groups.row(cance_button)


def load_chace():
    # win_shar = np.load("chace_pid.npy").item()
    # return win_shar
    f = open('chace_pid.txt', 'r')
    data = f.read()
    f.close()
    return eval(data)


time_shar = {}

win_shar = {}
try:
    win_shar = load_chace()
except:
    pass

print(win_shar)

global win_shar_chat_id


def load_win_shar_chat_id():
    f = open('win_shar_chat_id.txt', 'r')
    data = f.read()
    f.close()
    return int(data)


def save_win_shar_chat_id():
    f = open('win_shar_chat_id.txt', 'w')
    f.write(str(win_shar_chat_id))
    f.close()


try:
    win_shar_chat_id = load_win_shar_chat_id()
except:
    pass


def save_chace():
    global win_shar
    # np.save("chace_pid.npy", win_shar)
    f = open('chace_pid.txt', 'w')
    f.write(str(win_shar))
    f.close()


yes_text = "Підтвердити"
markup_yes = types.ReplyKeyboardMarkup()
markup_yes = markup_yes.row(cance_button)
yes_button = types.KeyboardButton(yes_text)
markup_yes = markup_yes.row(yes_button)

del_in_keyboard = types.InlineKeyboardMarkup()


@bot.message_handler(commands=['start'])
def start(message):
    if users.where_user(message.from_user.id):
        bot.send_message(message.chat.id, """Привіт! 😊, якщо бот зависне натисни /start
Виберіть зі списку свою групу ⬇️""", reply_markup=markup_groups)
        bot.register_next_step_handler(message, step_two)
    else:
        bot.send_message(message.chat.id, "Ви вже були зареєстровані 🙃", reply_markup=del_markup)


def step_two(message):
    if message.text != cance_text:
        group = message.text
        if group in import_json.group_list():

            users_markup = types.ReplyKeyboardMarkup()
            for a in import_json.stud_list(group):
                users_markup.row(a)
            users_markup.row(cance_button)

            bot.send_message(message.chat.id, "Оберіть зі списку свій ПІБ 🗒", reply_markup=users_markup)
            bot.register_next_step_handler(message, step_three, group)
        else:
            bot.register_next_step_handler(message, step_two)
            bot.send_message(message.chat.id, "Ви некоректно ввели групу! 🤨", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили реєстрацію 😔", reply_markup=del_markup)


def step_three(message, group):
    if message.text != cance_text:
        user_name = message.text
        if user_name in import_json.stud_list(group):
            if users.user_valid(user_name, group):
                mass_h = {}
                for a in sharas.shara_in_group(group):
                    mass_h[a] = 0
                time_shar[message.chat.id] = mass_h
                bot.send_message(message.chat.id,
                                 f"""{user_name}, виберіть ту шару💰, яку хочете виграти 🏆 та підтвердіть свій вибір обравши кнопку «Підтвердити».

Памятай, що ти можеш отримати лише 1 шару!!!""",
                                 reply_markup=markup_yes)
                bot.send_message(message.chat.id, messa(message.chat.id), reply_markup=keyboard_shar(message.chat.id))
                bot.register_next_step_handler(message, step_four, group, user_name)
            else:
                bot.send_message(message.chat.id,
                                 "Цей студент вже зареєстрований, якщо це помилка , повідомте технічну підтримку 😔",
                                 reply_markup=del_markup)
        else:
            bot.send_message(message.chat.id, "Цього студента немає в списку, повідомте технічну підтримку 😔",
                             reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили реєстрацію 😔", reply_markup=del_markup)


def step_four(message, group, user_name):
    if message.text != cance_text and message.text == yes_text:
        telega = message.from_user.username
        if telega == None:
            telega = "телеграм відсутній"
        shars = []
        for a in time_shar[message.chat.id]:
            if time_shar[message.chat.id][a] == 1:
                shars.append(a)
        if shars != []:
            shars_str = ''
            for a in shars:
                shars_str += str(a) + ' '
            now = datetime.now()
            users.insert(user_id=message.from_user.id,
                         user_name=user_name,
                         shars=shars_str,
                         group=group,
                         telegram=telega,
                         date_time=now.strftime("%m/%d/%Y, %H:%M:%S"))
            bot.send_message(message.chat.id, """Вітаю, Ви зареєстровані✅
Бажаємо перемоги 💪""", reply_markup=del_markup)
        else:
            bot.send_message(message.chat.id, "Ви не вибрали шари, реєстрацію відмінено 😔", reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили реєстрацію 😔", reply_markup=del_markup)


@bot.message_handler(commands=['winer'])
def winer(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Введіть номер шары")
        bot.register_next_step_handler(message, winer_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔")


def winer_two(message):
    global win_shar_chat_id
    win_shar_chat_id = message.chat.id
    save_win_shar_chat_id()
    try:
        num = str(int(message.text))
    except Exception as ex:
        print(ex)
        num = 0
    if sharas.shara_num_valid(num):
        sha = sharas.shara_select(int(message.text))
        amo = sha[3]
        if int(amo) > 0:
            winers = []
            mass_p = users.get_all()
            print(mass_p)
            # mass_w = winers_db.get_all()
            # mass_w_two = []
            # for d in mass_w:
            #     mass_w_two.append(d[2])
            # for g in mass_p:
            #     if g[0] in mass_w_two:
            #         mass_p.remove(g)
            # print(mass_p)
            mass_t = []
            for a in mass_p:
                if num in a[2].split(' '):
                    if winers_db.use_valdator(int(num), a[1]):
                        mass_t.append(a)
            len_mass = len(mass_t)
            if len(mass_t) < int(amo):
                amo = len(mass_t)
            if len(mass_t) != 0:
                for a in range(int(amo)):
                    win = random.choice(mass_t)
                    winers.append(win)
                    mass_t.remove(win)
                descr = sha[1]
                groups = sha[2].split(' ')
                amount = sha[3]
                groups_mess = ""
                for a in groups:
                    groups_mess += f"{a}, "
                winers_mess = ''
                for a in winers:
                    winers_mess += f"❌ {a[1]} з групи {a[3]} або ж @{a[4]}" + "\n"
                mess = f"В шарі №{num}" + "\n" + f"{descr}" + "\n" + f"Серед груп: {groups_mess}" + "\n" + f"Кількість шар: {amount}" + "\n" + f"Учасників: {len_mass}"
                bot.send_message(message.chat.id, mess)
                win_shar[message.message_id + 2] = {}
                res = bot.send_message(message.chat.id, winers_mess)
                win_shar[res.id] = {}
                for b in winers:
                    win_shar[res.id][b[0]] = 0
                    try:
                        now = datetime.now()
                        keyboard = types.InlineKeyboardMarkup()
                        keyboard.add(types.InlineKeyboardButton(text="Підтвердити",
                                                                callback_data=f"PID {b[0]} {res.id} {now.strftime('%m/%d/%Y/%H:%M:%S')} {num}"))
                        bot.send_message(b[0],
                                         text=f"Вітаємо, ви перемогли в шарі №{num}, натисніть підтвердить протягом 5хв, щоб підтвердити 😇",
                                         reply_markup=keyboard)
                    except:
                        bot.send_message(message.chat.id, f"Не вдалося відправити згоду на шару учаснику @{b[4]}")
                save_chace()
            else:
                bot.send_message(message.chat.id, "На цю шару немає учасників 😔")
        else:
            bot.send_message(message.chat.id, "Цю шару не можна розіграти, вона скінчилась 😔")
    else:
        bot.send_message(message.chat.id, "Цю шару не можливо знайти, перевірте коректність вводу 😔")


@bot.message_handler(commands=['create_shara'])
def create_shara(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Назвіть викладача, дисципліну та опишіть шару", reply_markup=markup)
        bot.register_next_step_handler(message, create_shara_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


def create_shara_two(message):
    if message.text != cance_text:
        description = message.text
        bot.send_message(message.chat.id, "Введіть групи через пробіл які беруть участь в шарі", reply_markup=markup)
        bot.register_next_step_handler(message, create_shara_three, description)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


def create_shara_three(message, description):
    if message.text != cance_text:
        groups = message.text
        groups_mass = groups.split(' ')
        groups_bd = import_json.group_list()
        count = 0
        for a in groups_mass:
            if a in groups_bd:
                pass
            else:
                count += 1
        if count == 0:
            groups_str = ''
            for a in groups_mass:
                groups_str += str(a) + ' '
            bot.send_message(message.chat.id, "Введіть кількість", reply_markup=markup)
            bot.register_next_step_handler(message, create_shara_four, description, groups_str)
        else:
            bot.send_message(message.chat.id, f"{count} групи немає в бд", reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


def create_shara_four(message, description, groups):
    if message.text != cance_text:
        amount = int(message.text)
        sharas.insert(description=description, groups=groups, amount=amount)
        bot.send_message(message.chat.id, "Шару створено", reply_markup=del_markup)


@bot.message_handler(commands=['delete_shara'])
def delete_shara(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Введіть номер шари", reply_markup=markup)
        bot.register_next_step_handler(message, delete_shara_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


def delete_shara_two(message):
    if message.text != cance_text:
        shara_id = int(message.text)
        try:
            sharas.delete(shara_id)
            bot.send_message(message.chat.id, "Шару видалено", reply_markup=del_markup)
        except:
            bot.send_message(message.chat.id, "Виникла помилка", reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


@bot.message_handler(commands=['update_shara'])
def update_shara(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Введіть номер шари", reply_markup=markup)
        bot.register_next_step_handler(message, update_shara_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


def update_shara_two(message):
    if message.text != cance_text:
        shara_id = int(message.text)
        bot.send_message(message.chat.id, "Назвіть викладача, дисципліну та опишіть шару", reply_markup=markup)
        bot.register_next_step_handler(message, update_shara_three, shara_id)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


def update_shara_three(message, shara_id):
    if message.text != cance_text:
        description = message.text
        bot.send_message(message.chat.id, "Введіть групи через пробіл які беруть участь в шарі", reply_markup=markup)
        bot.register_next_step_handler(message, update_shara_four, shara_id, description)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


def update_shara_four(message, shara_id, description):
    if message.text != cance_text:
        groups = message.text
        groups_mass = groups.split(' ')
        groups_bd = import_json.group_list()
        count = 0
        for a in groups_mass:
            if a in groups_bd:
                pass
            else:
                count += 1
        if count == 0:
            groups_str = ''
            for a in groups_mass:
                groups_str += str(a) + ' '
            bot.send_message(message.chat.id, "Введіть кількість", reply_markup=markup)
            bot.register_next_step_handler(message, update_shara_five, shara_id, description, groups_str)
        else:
            bot.send_message(message.chat.id, f"{count} групи немає в бд", reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви відмінили створення шари 😔", reply_markup=del_markup)


def update_shara_five(message, shara_id, description, groups):
    amount = int(message.text)
    sharas.update_shara(shara_id=shara_id, description=description, groups=groups, amount=amount)
    bot.send_message(message.chat.id, "Шару оновлено!", reply_markup=del_markup)


@bot.message_handler(commands=['all_shara'])
def all_shara(message):
    if message.from_user.username in settings.ADMINS:
        mass = sharas.get_all()
        if mass != []:
            bot.send_message(message.chat.id, "Всі шари:")
            mess = ""
            for a in mass:
                mess = f"""№{a[0]}
{a[1]}
Групи: {a[2]}
Кількість {a[3]} штук
"""
                bot.send_message(message.chat.id, mess)
        else:
            bot.send_message(message.chat.id, "Шари поки не створено")
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


@bot.message_handler(commands=['min_shara'])
def min_shara(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Введіть номер шари яку потрібно відняти", reply_markup=markup)
        bot.register_next_step_handler(message, min_shara_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


def min_shara_two(message):
    if message.text != cance_text:
        try:
            num = int(message.text)
            shara = sharas.shara_select(num)
            new_ammount = int(shara[3]) - 1
            if new_ammount >= 0:
                sharas.update_shara(shara_id=shara[0],
                                    description=shara[1],
                                    groups=shara[2],
                                    amount=new_ammount)
                bot.send_message(message.chat.id, f"Ви відняли 1 шару з №{num}, лишилося {int(shara[3]) - 1} штук",
                                 reply_markup=del_markup)
            else:
                bot.send_message(message.chat.id, "Ця шара нажаль скінчилася 😔", reply_markup=del_markup)
        except:
            bot.send_message(message.chat.id, "Виникла помилка, можливо ви ввели не номер шари 😔",
                             reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви скасували зменшення кількості", reply_markup=del_markup)


@bot.message_handler(commands=['plus_shara'])
def plus_shara(message):
    if message.from_user.username in settings.ADMINS:
        bot.send_message(message.chat.id, "Введіть номер шари яку потрібно збільшити", reply_markup=markup)
        bot.register_next_step_handler(message, min_shara_two)
    else:
        bot.send_message(message.chat.id, "Ви не можете використовувати дану команду 😔", reply_markup=del_markup)


def plus_shara_two(message):
    if message.text != cance_text:
        try:
            num = int(message.text)
            shara = sharas.shara_select(num)
            new_ammount = int(shara[3]) + 1
            sharas.update_shara(shara_id=shara[0],
                                description=shara[1],
                                groups=shara[2],
                                amount=new_ammount)
            bot.send_message(message.chat.id, f"Ви додали 1 шару до №{num}, лишилося {int(shara[3]) + 1} штук",
                             reply_markup=del_markup)
        except:
            bot.send_message(message.chat.id, "Виникла помилка, можливо ви ввели не номер шари 😔",
                             reply_markup=del_markup)
    else:
        bot.send_message(message.chat.id, "Ви скасували збільшення кількості", reply_markup=del_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)
    cdata = call.data.split(' ')
    print(cdata)
    if cdata[0] == "DOB":
        print(cdata[1])
        if call.message.chat.id in time_shar:
            time_shar[call.message.chat.id][int(cdata[1])] = res(time_shar[call.message.chat.id][int(cdata[1])])
            mess = messa(call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=mess,
                                  reply_markup=keyboard_shar(call.message.chat.id))
    elif cdata[0] == "PID":
        now = datetime.now()
        user_id = cdata[1]
        shara_id = cdata[2]
        us_time = datetime.strptime(cdata[3], '%m/%d/%Y/%H:%M:%S')
        shara = cdata[4]
        if int(shara_id) in win_shar:
            if now < us_time + timedelta(minutes=5):
                try:
                    if win_shar[int(shara_id)][int(user_id)] == 0:
                        win_shar[int(shara_id)][int(user_id)] = 1
                        mess = f"Вітаємо, ви підтвердили участь в шарі №{shara}"
                        win_user = users.get_user(int(user_id))
                        winers_db.insert(shara_id=int(shara),
                                         user_id=int(user_id),
                                         user_name=win_user[1],
                                         group=win_user[3],
                                         telegram=win_user[4],
                                         date_time=now.strftime("%m/%d/%Y, %H:%M:%S")
                                         )
                        sha = sharas.shara_select(int(shara))
                        print(sha)
                        new_ammount = int(sha[3]) - 1
                        sharas.update_shara(shara_id=sha[0],
                                            description=sha[1],
                                            groups=sha[2],
                                            amount=new_ammount)
                        bot.edit_message_text(chat_id=call.message.chat.id,
                                              message_id=call.message.message_id,
                                              text=mess,
                                              reply_markup=None
                                              )
                        bot.edit_message_text(chat_id=win_shar_chat_id,
                                              message_id=shara_id,
                                              text=win_mess(int(shara_id)),
                                              )
                        save_chace()
                except Exception as ex:
                    print(ex)
                    bot.send_message(call.message.chat.id, "Виникла помилка, повідомте в тех. підтримку")
            else:
                mess = f"Нажаль 5хв вже пройшло на шару №{shara}"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=mess,
                                      reply_markup=None)
        else:
            mess = f"Ця шара вже не обслуговується, якщо сталася помилка негайно сповістіть тех. підтримку. Шара №{shara}"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=mess,
                                  reply_markup=None)


def res(num):
    if num == 0:
        return 1
    else:
        return 0


def keyboard_shar(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    mass = []
    for a in time_shar[chat_id]:
        mass.append(a)
    for a in mass:
        keyboard.add(types.InlineKeyboardButton(text=a, callback_data=f"DOB {a}"))
    return keyboard


def messa(chat_id):
    mass_a = []
    for a in time_shar[chat_id]:
        mass_a.append(a)
    mess = "Ваші шари:" + "\n"
    for b in mass_a:
        shara = sharas.shara_select(b)
        descr = shara[1]
        groups = shara[2].split(' ')
        amount = shara[3]
        groups_mess = ""
        for a in groups:
            groups_mess += f"{a}, "
        mess += f"{znak(time_shar[chat_id][b])} шара №{b}" + "\n" + f"{descr}" + "\n" + f"Кількість: {amount}" + "\n" + f"Групи {groups_mess}" + "\n"
    return mess


def win_mess(shar_id):
    mass = win_shar[shar_id]
    mess = ''
    for a in mass:
        user = users.get_user(a)
        mess += f'{znak(win_shar[shar_id][a])} {user[1]} з групи {user[3]} або ж @{user[4]}' + "\n"
    return mess


def znak(num):
    if num == 0:
        return "❌"
    else:
        return "✅"


if __name__ == "__main__":
    bot.polling(none_stop=True)
