# DEHB Ders Calisma Asistani

DEHB (Dikkat Eksikligi Hiperaktivite Bozuklugu) olan bireyler icin ozel olarak tasarlanmis **tam otomatik ders calisma asistani**.

## Ozellikler

- **Pomodoro Zamanlayici**: DEHB'ye uygun kisa calisma donguleriy (varsayilan 25dk calisma / 5dk mola, 15dk'ya kadar dusuruleb)
- **Otomatik Gorev Parcalama**: Buyuk gorevleri kucuk, yonetilebilir adimlara otomatik boler
- **Motivasyon ve Odul Sistemi**: XP, seviye, rozet ve seri takibi ile aninda geri bildirim
- **Hizli Odaklanma Modu**: Dusuk motivasyon anlari icin 10 dakikalik mini oturum
- **Ilerleme Takibi**: Gunluk ve haftalik calisma raporlari, odak skoru hesaplama
- **Sesli Bildirimler**: Timer bitiminde sesli uyari (macOS, Linux, Windows)
- **DEHB Ipuclari**: Her gun farkli, kanitlanmis DEHB stratejileri

## DEHB Icin Neden Bu Asistan?

| Sorun | Cozum |
|-------|-------|
| Buyuk gorevler bunaltici | Otomatik kucuk adimlara bolme |
| Zaman algisi zayif | Gorsel geri sayim ve ilerleme cubugu |
| Motivasyon dalgalanmalari | Aninda XP/rozet odulleri |
| Odaklanma guclugu | Kisa Pomodoro donguleriy (15-25 dk) |
| Baslamak zor | Hizli Odaklanma modu (sadece 10 dk) |
| Sureklin takip kaybediliyor | Otomatik ilerleme kaydi ve raporlar |

## Kurulum

```bash
# Repoyu klonla
git clone https://github.com/sodium1066/sodium1066.git
cd sodium1066

# Calistir (Python 3.7+ gerekli, ek bagimllik yok)
python study_assistant.py
```

## Kullanim

```
=================================================
   DEHB Ders Calisma Asistani
=================================================

--- Ana Menu ---
[1] Ders Calismaya Basla (Pomodoro)
[2] Gorevlerimi Yonet
[3] Ilerleme Raporlarim
[4] Hizli Odaklanma Modu (10dk)
[5] Ayarlar
[6] Cikis
```

## Proje Yapisi

```
study_assistant.py   # Ana uygulama - menu ve oturum yonetimi
pomodoro.py          # Pomodoro zamanlayici modulu
task_manager.py      # Gorev yonetimi ve otomatik parcalama
motivation.py        # XP, seviye, rozet ve motivasyon sistemi
config.py            # Yapilandirma yonetimi
config.json          # Kullanici ayarlari (otomatik olusur)
tasks.json           # Gorev veritabani (otomatik olusur)
study_history.json   # Calisma gecmisi (otomatik olusur)
motivation_data.json # Motivasyon verileri (otomatik olusur)
```

## Ayarlar

Tum ayarlar uygulama icinden degistirilebilir veya `config.json` dosyasi elle duzenlenebilir:

```json
{
  "work_duration": 25,
  "short_break": 5,
  "long_break": 15,
  "long_break_interval": 4,
  "sound_enabled": true,
  "auto_split": true
}
```

## Hakkimda

- @sodium1066 (Yigit Gulenay)
- yigitgulenay@gmail.com
