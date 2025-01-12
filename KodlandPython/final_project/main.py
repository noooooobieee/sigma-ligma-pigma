from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, BotCommand, ChatPermissions, ChatMember, ChatAdministratorRights
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio
import random

# Установите токен вашего бота
TOKEN = "сам придумай"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Команда /start
@router.message(Command(commands=["start"]))
async def start_command(message: Message):
    await message.reply("Привет! Я модератор-бот. Для списка команд используйте /help.")

# Команда /help
@router.message(Command(commands=["help"]))
async def help_command(message: Message):
    commands = [
        '/start - Запустить бота',
        '/help - Список команд',
        '/mute - Отключить возможность отправки сообщений',
        '/unmute - Включить возможность отправки сообщений',
        '/ban - Забанить пользователя',
        '/unban - Разбанить пользователя',
        '/kick - Исключить пользователя',
        '/warn - Выдать предупреждение',
        '/clear - Очистить чат',
        '/set_title - Установить название чата',
        '/set_description - Установить описание чата',
        '/pin - Закрепить сообщение',
        '/unpin - Открепить сообщение',
        '/admins - Показать список администраторов',
        '/grant - Выдать разрешения пользователю',
        '/invite - Получить ссылку для приглашения бота',
        '/random_user - Выбрать случайного пользователя из чата',
        '/random_number - Сгенерировать случайное число от 1 до 100',
        '/random_choice - Случайный выбор из списка вариантов',
    ]
    await message.reply("\n".join(commands))

# Команда /mute
@router.message(Command(commands=["mute"]))
async def mute_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=False),
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} был отключен от чата.")

# Команда /unmute
@router.message(Command(commands=["unmute"]))
async def unmute_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=ChatPermissions(can_send_messages=True),
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} был восстановлен в чате.")

# Команда /ban
@router.message(Command(commands=["ban"]))
async def ban_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} был забанен.")

# Команда /unban
@router.message(Command(commands=["unban"]))
async def unban_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} был разбанен.")

# Команда /kick
@router.message(Command(commands=["kick"]))
async def kick_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id
    )
    await bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} был исключён из чата.")

# Команда /warn
@router.message(Command(commands=["warn"]))
async def warn_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    await message.reply(f"Пользователю {message.reply_to_message.from_user.full_name} выдано предупреждение.")

# Команда /clear
@router.message(Command(commands=["clear"]))
async def clear_command(message: Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.reply("Чат был очищен.")

# Команда /set_title
@router.message(Command(commands=["set_title"]))
async def set_title_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Укажите название чата.")
        return

    new_title = args[1]
    await bot.set_chat_title(message.chat.id, new_title)
    await message.reply(f"Название чата изменено на: {new_title}")

# Команда /set_description
@router.message(Command(commands=["set_description"]))
async def set_description_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Укажите описание чата.")
        return

    new_description = args[1]
    await bot.set_chat_description(message.chat.id, new_description)
    await message.reply(f"Описание чата изменено.")

# Команда /pin
@router.message(Command(commands=["pin"]))
async def pin_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение.")
        return

    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    await message.reply("Сообщение закреплено.")

# Команда /unpin
@router.message(Command(commands=["unpin"]))
async def unpin_command(message: Message):
    await bot.unpin_chat_message(message.chat.id)
    await message.reply("Сообщение откреплено.")

# Команда /admins
@router.message(Command(commands=["admins"]))
async def admins_command(message: Message):
    chat_administrators = await bot.get_chat_administrators(chat_id=message.chat.id)
    admin_list = [admin.user.full_name for admin in chat_administrators]
    await message.reply("Список администраторов:\n" + "\n".join(admin_list))

# Команда /grant
@router.message(Command(commands=["grant"]))
async def grant_command(message: Message):
    if not message.reply_to_message:
        await message.reply("Эту команду нужно использовать в ответ на сообщение пользователя.")
        return

    permissions = ChatPermissions(
        can_send_messages=True,
        can_invite_users=True,
        can_pin_messages=True
    )

    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=permissions
    )
    await message.reply(f"Пользователь {message.reply_to_message.from_user.full_name} получил расширенные разрешения.")

# Команда /invite
@router.message(Command(commands=["invite"]))
async def invite_command(message: Message):
    try:
        invite_link = await bot.export_chat_invite_link(chat_id=message.chat.id)
        await message.reply(f"Пригласите бота в другой чат, используя эту ссылку: {invite_link}")
    except Exception as e:
        await message.reply(f"Ошибка при генерации ссылки приглашения: {e}")

# Команда /random_user
@router.message(Command(commands=["random_user"]))
async def random_user_command(message: Message):
    members = await bot.get_chat_member_count(message.chat.id)
    random_index = random.randint(0, members - 1)
    random_member = await bot.get_chat_member(message.chat.id, random_index)
    await message.reply(f"Случайный пользователь: {random_member.user.full_name}")

# Команда /random_number
@router.message(Command(commands=["random_number"]))
async def random_number_command(message: Message):
    number = random.randint(1, 100)  # Генерируем случайное число от 1 до 100
    await message.reply(f"Случайное число: {number}")

# Команда /random_choice
@router.message(Command(commands=["random_choice"]))
async def random_choice_command(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Укажите варианты через запятую. Пример: /random_choice вариант1, вариант2, вариант3")
        return

    choices = [choice.strip() for choice in args[1].split(",")]
    selected_choice = random.choice(choices)
    await message.reply(f"Случайный выбор: {selected_choice}")


# Установка команд для меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Список команд"),
        BotCommand(command="mute", description="Отключить пользователя"),
        BotCommand(command="unmute", description="Включить пользователя"),
        BotCommand(command="ban", description="Забанить пользователя"),
        BotCommand(command="unban", description="Разбанить пользователя"),
        BotCommand(command="kick", description="Исключить пользователя"),
        BotCommand(command="warn", description="Выдать предупреждение"),
        BotCommand(command="clear", description="Очистить чат"),
        BotCommand(command="set_title", description="Установить название чата"),
        BotCommand(command="set_description", description="Установить описание чата"),
        BotCommand(command="pin", description="Закрепить сообщение"),
        BotCommand(command="unpin", description="Открепить сообщение"),
        BotCommand(command="admins", description="Показать список администраторов"),
        BotCommand(command="grant", description="Выдать разрешения пользователю"),
        BotCommand(command="invite", description="Получить ссылку для приглашения бота"),
        BotCommand(command="random_user", description="Выбрать случайного пользователя из чата"),
        BotCommand(command="random_number", description="Сгенерировать случайное число от 1 до 100"),
        BotCommand(command="random_choice", description="Случайный выбор из списка вариантов"),
    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
