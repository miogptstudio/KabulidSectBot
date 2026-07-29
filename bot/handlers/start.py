from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database.engine import async_session
from database.crud import get_or_create_user
from database.models import ROLE_LEADER
from bot.config import ADMIN_IDS

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    async with async_session() as session:
        user = await get_or_create_user(
            session,
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )

        if message.from_user.id in ADMIN_IDS and user.role != ROLE_LEADER:
            user.role = ROLE_LEADER
            await session.commit()

    text = (
        f"سلام <b>{user.full_name}</b> 👋\n\n"
        f"به ربات فرقه‌ای و تذهیب خوش اومدی!\n\n"
        f"🏆 رتبه: <b>{user.rank}</b>\n"
        f"⭐ نقش: <b>{user.role}</b>\n"
        f"سطح: {user.level} | XP: {user.xp}\n\n"
        f"📢 عضویت اجباری در کانال:\n"
        f"👉 @kabulid_manhua\n\n"
        f"دستورات اصلی:\n"
        f"/profile — پروفایل\n"
        f"/ranking — لیدربورد (۳ نفر برتر)\n"
        f"/sects — فرقه‌ها\n"
        f"/cultivation — تذهیب\n"
        f"/missions — مأموریت‌ها\n"
        f"/arena — آرنا\n"
        f"/master — استاد و شاگرد\n"
        f"/accounts — چندحسابه
/buildings — ساختمان‌ها و خرید
/craft — ساخت معجون و طلسم
/inventory — کیف و آیتم‌ها
/gender — انتخاب جنسیت
/dual — تذهیب دوگانه
/marry — نامزدی و ازدواج
/divorce — طلاق
/wives — همسران
/invitewedding — دعوت عروسی
/solo — خودارضایی
/pets — حیوانات
/wallet — سکه و سنگ روحی
/hunt — شکار
/virgin — وضعیت بدن
/afterdeath — بعد از مرگ\n"
        f"/duel — دوئل\n"
        f"/guardian — نگهبان\n"
        f"/help — راهنمای کامل"
    )
    await message.answer(text)


@router.message(Command("help", "راهنما"))
async def cmd_help(message: Message):
    text = (
        "📖 <b>راهنمای کامل ربات</b>\n\n"

        "━━━━━━━━━━━━━━\n"
        "⚔️ <b>دوئل و نگهبان</b>\n"
        "/duel — شروع دوئل (ریپلای یا تگ)\n"
        "/guardian — حالت نگهبان\n\n"

        "🏛️ <b>فرقه‌ها</b>\n"
        "/sects — لیست فرقه‌ها\n"
        "/createsect &lt;نام&gt; &lt;نوع&gt;\n"
        "/joinsect &lt;نام&gt;\n"
        "/mysect — فرقه من\n"
        "انواع فرقه: ارتدوکس | بی‌طرف | شیطانی\n\n"

        "🧘 <b>تذهیب</b>\n"
        "/cultivation — وضعیت تذهیب\n"
        "/meditate — مدیتیت (+انرژی)\n"
        "قلمروها: پایه → متوسط → بالا → پیشرفته → خدا\n\n"

        "🎓 <b>استاد و شاگرد</b>\n"
        "/master — وضعیت\n"
        "/takedisciple — قبول شاگرد (ریپلای)\n"
        "/mydisciples — لیست شاگردها\n"
        "/mymaster — استاد من\n\n"

        "⚔️ <b>آرنا</b>\n"
        "/arena — وضعیت آرنا (برنز/نقره/طلا)\n\n"

        "🎯 <b>مأموریت</b>\n"
        "/missions — مشاهده و انتخاب\n\n"

        "👤 <b>چندحسابه</b>\n"
        "/accounts — مدیریت حساب‌ها\n"
        "/createaccount — ساخت حساب\n"
        "/login — ورود به حساب دیگر\n\n"

        "📊 <b>لیدربورد و پروفایل</b>\n"
        "/ranking — ۳ نفر برتر\n"
        "/profile — پروفایل کامل\n\n"

        "━━━━━━━━━━━━━━\n"
        "📢 عضویت اجباری: @kabulid_manhua\n"
        "🛠 پنل مدیریت: /admin"
    )
    await message.answer(text)
