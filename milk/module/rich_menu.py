from linebot.models import RichMenu, RichMenuSize, RichMenuBounds, RichMenuArea, DatetimePickerAction, MessageAction
import datetime

milk_rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=True,
    name="milk rich menu",
    chat_bar_text="Open Menu",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1617, height=843),
            action=DatetimePickerAction(data="action=calc_month", mode="date", initial=datetime.date.today())
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1617, y=0, width=2500 - 1617, height=843),
            action=MessageAction(text="ミス")
        ),
    ]
)
