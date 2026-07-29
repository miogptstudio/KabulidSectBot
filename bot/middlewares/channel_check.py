from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.enums import ChatMemberStatus

CHANNEL_USERNAME = "kabulid_manhua"  # بدون @


class ChannelMembershipMiddleware(BaseMiddleware):
    """اجباری کردن عضویت در کانال"""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data["bot"]
        user = None

        if isinstance(event, Message):
            user = event.from_user
        elif isinstance(event, CallbackQuery):
            user = event.from_user

        if not user:
            return await handler(event, data)

        # ادمین‌ها و رهبر از چک معاف هستن (اختیاری)
        # فعلاً همه باید عضو باشن

        try:
            member = await bot.get_chat_member(
                chat_id=f"@{CHANNEL_USERNAME}",
                user_id=user.id
            )
            if member.status in (
                ChatMemberStatus.MEMBER,
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.CREATOR,
                ChatMemberStatus.RESTRICTED  # گاهی restricted هم عضو حساب می‌شه
            ):
                return await handler(event, data)
        except Exception:
            # اگر ربات ادمین کانال نباشه یا خطایی پیش بیاد
            pass

        # کاربر عضو نیست
        text = (
            "⛔️ برای استفاده از ربات باید اول در کانال عضو بشی:\n\n"
            f"👉 https://t.me/{CHANNEL_USERNAME}\n\n"
            "بعد از عضویت، دوباره /start رو بزن."
        )

        if isinstance(event, Message):
            await event.answer(text)
        elif isinstance(event, CallbackQuery):
            await event.answer("اول باید عضو کانال بشی!", show_alert=True)
            try:
                await event.message.answer(text)
            except Exception:
                pass

        return  # ادامه نده
