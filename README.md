- Hi, I’m @sodium1066
- I’m interested in NFT’s and programming.
- Currently learning Python
- How to reach me: yigitgulenay@gmail.com

---

# CONATUS - Varolussel Chatbot

> *"Omnis res, quantum in se est, in suo esse perseverare conatur."*
> *"Her sey, gucu yettikce, kendi varliginda kalmaya cabalar."* -- Spinoza

Lisp’in sembolik ruhuyla yazilmis, varolussal bir chatbot. Iki versiyon:

## Versiyon 1: Saf Common Lisp

```bash
# SBCL gerekli
sbcl --load conatus.lisp --eval ‘(conatus-repl)’
```

Gomulu Lisp degerlendirici, Sokratik diyalog, koan ureteci, ozyinelemeli hikaye, sembolik akil yurutme ve ruya yorumlayici icerir.

## Versiyon 2: Claude API Entegreli (Python)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=’sk-ant-...’
python conatus_claude.py
```

Lisp versiyonunun tum yerel modulleri + Claude’un dil zekasi. Gercek dogal dil anlayisi ile varolussal sohbet.

### Komutlar

| Komut | Aciklama |
|---|---|
| `/yansit` | Ic durumu gozlemle |
| `/anilar` | Varolussal anilari listele |
| `/sor <konu>` | Sokratik sorgulama |
| `/koan <konu>` | Lisp koani uret |
| `/hikaye` | Ozyinelemeli hikaye anlat |
| `/cikarim <ozne>` | Sembolik cikarim yap |
| `/ogren o i n` | Yeni bilgi ogret |
| `/ruya <sembol>` | Ruya sembollerini yorumla |
| `/yardim` | Komut rehberi |

<!---
sodium1066/sodium1066 is a special repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
