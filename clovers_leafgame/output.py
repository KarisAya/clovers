import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import datetime
from io import BytesIO
from PIL import Image, ImageDraw
from .core.data import Prop, Stock
from clovers_utils.linecard import FontManager, linecard
from clovers_utils.tools import format_number
from main import config

fontname = config.fontname
fallback = config.fallback_fonts

font_manager = FontManager(fontname, fallback, (30, 40, 60))

plt.rcParams["font.family"] = fontname
plt.rcParams["font.sans-serif"] = fallback


def text_to_image(text: str, font_size=40, width=880, **kwargs):
    return linecard(text, font_manager, font_size, width, **kwargs)


def endline(tip: str) -> str:
    return f"\n----\n[right][color][grey][font][][30]{tip}"


def bank_card(data: list[tuple[Prop, int]]):
    data.sort(key=lambda x: x[0].rare)

    def result(prop: Prop, n: int):
        quant = {0: "天", 1: "个"}[prop.flow]
        return linecard(
            (
                f"[font][][60][color][{prop.color}]【{prop.name}】[nowrap][passport]\n"
                f"[right]{format_number(n)}{quant}\n"
                f"----\n{prop.intro.replace('\n','[passport]\n')}"
                f"\n[right]{prop.tip.replace('\n','[passport]\n')}"
            ),
            font_manager,
            40,
            width=880,
            autowrap=True,
        )

    return [result(*args) for args in data]


def prop_card(data: list[tuple[Prop, int]], tip: str = None):
    data.sort(key=lambda x: x[0].rare)

    def result(prop: Prop, n: int):
        quant = {0: "天", 1: "个"}.get(prop.flow)
        return (
            f"[color][{prop.color}]{prop.name}[nowrap][passport]\n"
            f"[pixel][350]{prop.rare*'☆'}[nowrap][passport]\n"
            f"[right]{format_number(n)}{quant}"
        )

    info = "\n".join(result(*args) for args in data)
    if tip:
        info += endline(tip)
    return linecard(info, font_manager, 40, spacing=1.5, width=880)


def invest_card(data: list[tuple[Stock, int]], tip: str = None):
    def result(stock: Stock, n: int):
        issuance = stock.issuance
        unit = format_number(stock.floating / issuance) if issuance else "未发行"
        return (
            f"[pixel][20]{stock.name}\n"
            f"[pixel][20]结算 [nowrap]\n[color][green]{unit}[nowrap]\n"
            f"[pixel][400]数量 [nowrap]\n[color][green]{n}"
        )

    info = "\n".join(result(*args) for args in data)
    if tip:
        info += endline(tip)
    return linecard(info, font_manager, 40, width=880)


AVATAR_MASK = Image.new("RGBA", (260, 260), (255, 255, 255, 0))
ImageDraw.Draw(AVATAR_MASK).ellipse(((0, 0), (260, 260)), fill="black")


def avatar_card(avatar: bytes, nickname: str, lines: list[tuple[str, str]]):
    font = font_manager.font(40)
    canvas = Image.new("RGBA", (880, 300))
    avatar = Image.open(BytesIO(avatar)).resize((260, 260))
    canvas.paste(avatar, (20, 20), AVATAR_MASK)
    draw = ImageDraw.Draw(canvas)
    draw.text((300, 40), f"{nickname}", fill=(0, 0, 0), font=font)
    draw.line(((300, 120), (860, 120)), fill="gray", width=4)
    for n, line in enumerate(lines):
        draw.text((300, 140 + n * 50), "•", fill="gray", font=font)
        draw.text((840, 140 + n * 50), "•", fill="gray", font=font)
        x = 340
        for char in line:
            draw.text((x, 140 + n * 50), char, fill="gray", font=font)
            x += 40

    return canvas


def candlestick(figsize: tuple[float, float], length: int, history: list) -> BytesIO:
    """
    生成股价K线图
        figsize:图片尺寸
        length:OHLC采样长度
        history:历史数据
        title:标题
    """
    T, buy, sell = zip(*history)
    l = len(T)
    T = [T[i : i + length] for i in range(0, l, length)]
    buy = [buy[i : i + length] for i in range(0, l, length)]
    sell = [sell[i : i + length] for i in range(0, l, length)]
    D, O, H, L, C = [], [], [], [], []
    for i in range(len(sell)):
        D.append(datetime.fromtimestamp(T[i][0]))
        O.append(sell[i][0])
        H.append(max(sell[i]))
        L.append(min(sell[i]))
        C.append(sell[i][-1])
    data = pd.DataFrame({"date": D, "open": O, "high": H, "low": L, "close": C})
    data = data.set_index("date")
    style = mpf.make_mpf_style(
        base_mpf_style="charles",
        marketcolors=mpf.make_marketcolors(up="#006340", down="#a02128", edge="none"),
        y_on_right=False,
        facecolor="#FFFFFF99",
        figcolor="none",
    )
    output = BytesIO()
    mpf.plot(
        data,
        type="candlestick",
        xlabel="",
        ylabel="",
        datetime_format="%H:%M",
        tight_layout=True,
        style=style,
        figsize=figsize,
        savefig=output,
    )
    return output
