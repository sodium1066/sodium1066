# Claude Ayarlar Rehberi — Eksiksiz Kusbakisi

> Claude uygulamasindaki (web, masaustu, mobil) **tum** ayar sekmelerinin ne ise yaradigi, icerdigi secenekler ve pratik ipuclariyla aciklanmasi.

---

## Icerik Haritasi

| # | Bolum | Kapsam |
|---|-------|--------|
| 1 | [Genel (General)](#1-genel-general) | Tema, dil, varsayilan model |
| 2 | [Hesap (Account)](#2-hesap-account) | Profil, guvenlik, oturum yonetimi |
| 3 | [Gizlilik (Privacy)](#3-gizlilik-privacy) | Veri egitimi, gizli mod, veri saklama |
| 4 | [Faturalandirma (Billing)](#4-faturalandirma-billing) | Plan yonetimi, odeme, fatura gecmisi |
| 5 | [Kullanim (Usage)](#5-kullanim-usage) | Token tuketimi, hiz siniri, sifirlama |
| 6 | [Yetenekler (Capabilities)](#6-yetenekler-capabilities) | Artifacts, gorsellestirme, arama, bellek, dosya, kod |
| 7 | [Baglayicilar (Connectors)](#7-baglayicilar-connectors) | Gmail, Slack, Notion, GitHub vb. entegrasyonlar |
| 8 | [Claude Code](#8-claude-code) | CLI ayarlari, IDE, MCP, izinler, hook'lar, sandbox |
| 9 | [Cowork](#9-cowork) | Proje alanlari, takim isbirligi, zamanlanmis gorevler |
| 10 | [Claude in Chrome (Beta)](#10-claude-in-chrome-beta) | Tarayici otomasyonu, is akisi kaydi, zamanlanmis gorevler |
| 11 | [Masaustu: Genel](#11-masaustu-uygulamasi--genel) | Bilgisayar Kullanimi, engelli uygulamalar |
| 12 | [Masaustu: Uzantilar (Extensions)](#12-masaustu-uygulamasi--uzantilar-extensions) | MCP eklenti yonetimi, marketplace |
| 13 | [Masaustu: Gelistirici (Developer)](#13-masaustu-uygulamasi--gelistirici-developer) | MCP sunucu loglari, hata ayiklama |

---

## 1. Genel (General)

Uygulamanin gorunumunu ve temel davranisini belirleyen ayarlar.

### Tema

| Secenek | Aciklama |
|---------|----------|
| **Light** | Acik arka plan |
| **Dark** | Koyu arka plan |
| **System** | Isletim sistemi tercihini takip eder |

> **Varsayilan:** System

### Dil (Language)

Claude'un yanitlarinda kullanacagi dili secin. Arayuz dili degil, **yanit dili** ayaridir.

- Turkce, Ingilizce, Almanca, Fransizca, Japonca dahil duzinelerce dil desteklenir.
- Dil ayari tum yeni konusmalara uygulanir.

### Varsayilan Model

Yeni konusmalarda kullanilacak modeli secin:

| Model | Guc | Hiz | Ne Zaman |
|-------|-----|-----|----------|
| **Claude Opus** | ★★★★★ | Yavas | Karmasik muhakeme, uzun analiz |
| **Claude Sonnet** | ★★★★☆ | Dengeli | Gunluk kullanim, cogu gorev |
| **Claude Haiku** | ★★★☆☆ | En hizli | Basit sorular, hizli cevap |

> **Varsayilan:** Claude Sonnet

> **Ipucu:** Konusma basinda modeli degistirebilirsiniz; Genel ayari yalnizca **yeni** konusmalarin baslangic modelini belirler.

---

## 2. Hesap (Account)

Kimlik ve guvenlik bilgilerinizi yoneten bolum.

### Profil Bilgileri

| Alan | Aciklama |
|------|----------|
| **Ad** | Goruntulenen isim |
| **E-posta** | Hesaba bagli birincil e-posta |
| **Abonelik** | Mevcut plan (Free / Pro / Max / Team / Enterprise) |

### Guvenlik

| Ozellik | Aciklama |
|---------|----------|
| **Iki faktorlu dogrulama (2FA)** | Giris guvenligini arttirir |
| **Aktif oturumlar** | Bagli cihazlari goruntuleyin ve oturumlari sonlandirin |
| **Bagli hesaplar** | Google, SSO gibi OAuth baglantilari |
| **Sifre degistirme** | Hesap sifrenizi guncelleyin |

### Hesap Silme

- **Kalici** bir islemdir — geri alinamaz.
- Tum konusmalar, projeler ve veriler silinir.
- Ayarlar > Hesap > "Hesabi Sil" ile erisilir.

> **Ipucu:** Hesap silmeden once onemli konusmalarinizi disa aktarin.

---

## 3. Gizlilik (Privacy)

Claude'un verilerinizi nasil kullandigini kontrol eden en kritik bolum.

### "Claude'u Gelistirmeye Yardim Et" Anahtari

Bu, **en onemli gizlilik kontroludur**.

| Durum | Etki |
|-------|------|
| **ACIK** | Konusmalariniz model egitiminde kullanilabilir; 5 yila kadar saklanir |
| **KAPALI** | Veriler egitimde kullanilmaz; daha kisa saklama suresi uygulanir |

| Plan | Varsayilan Deger |
|------|-----------------|
| Free / Pro / Team | **ACIK** |
| Enterprise | **KAPALI** |

> **Ipucu:** Hassas verilerle calisiyorsaniz bu anahtari mutlaka **KAPALI** konumuna getirin.

### Gizli Mod (Incognito)

- Sohbet penceresinin sag ustundeki **hayalet simgesinden** etkinlestirilir.
- Bu modda yapilan konusmalar:
  - Model egitiminde **kullanilmaz**
  - Daha kisa saklama suresiyle tutulur
  - Konusma gecmisinde gorunmez

> **Ne zaman:** Hassas bilgiler iceren tekil konusmalar icin. Surekli gizlilik istiyorsaniz ana anahtari kapatin.

### Veri Saklama ve Silme

| Islem | Sonuc |
|-------|-------|
| Tekil sohbeti sil | Arayuzden hemen kaybolur; sistemlerden 30 gun icinde silinir |
| Tum gecmisi temizle | Toplu silme desteklenir |
| GDPR/CCPA talepleri | Yasal uyum secenekleri mevcuttur |

### Baglanti Izinleri

- Bagli servisleri (Slack, Google Drive vb.) buradan gorebilirsiniz
- Istenmeyen entegrasyonlarin OAuth izinlerini iptal edebilirsiniz

---

## 4. Faturalandirma (Billing)

Abonelik planlarinizi ve odeme bilgilerinizi yonetin.

### Mevcut Planlar

| Plan | Ucret | Ozellikler |
|------|-------|-----------|
| **Free** | $0 | Sinirli kullanim, temel ozellikler |
| **Pro** | $20/ay | Daha yuksek limitler, oncelikli erisim |
| **Max** | Daha yuksek fiyat | En yuksek limitler, gelismis ozellikler |
| **Team** | Kisi basi fiyatlandirma | Takim isbirligi, organizasyon yonetimi |
| **Enterprise** | Ozel fiyat | Ozel destek, gelismis guvenlik, veri kontrolu |

> **Ipucu:** Pro planinda yillik odeme secenegi mevcuttur (~%17 tasarruf).

### Odeme Yonetimi

| Ayar | Aciklama |
|------|----------|
| **Odeme yontemi** | Kredi karti ekle/guncelle |
| **Otomatik yenileme** | Varsayilan ACIK; kapatilabilir |
| **Plan degistirme** | Yukseltin veya dusurme yapin |
| **Fatura gecmisi** | Gecmis odemeleri goruntuleyin |
| **Iptal** | Free plana dusurur; donem sonuna kadar mevcut plan gecerli |

> **Not:** Fatura tarihini dogrudan degistiremezsiniz. Farkli tarih icin iptal edip tercih ettiginiz tarihte yeniden abone olun.

---

## 5. Kullanim (Usage)

Token tuketiminizi ve hiz sinirlarinizi izleyin.

### Izleme Paneli

| Metrik | Aciklama |
|--------|----------|
| **Token kullanimi** | Gorsel grafik ile gunluk/haftalik tuketim |
| **Istek sikligi** | API isteklerinin zaman dagilimi |
| **Hiz siniri durumu** | Mevcut kotanizin ne kadarini kullandiginiz |
| **Plan bilgisi** | Aktif abonelik kademesi |

### Sifirlama Zamanlari

| Plan | Sifirlama |
|------|-----------|
| **Free** | Gunluk |
| **Pro** | Gunluk, gece yarisi UTC'de |
| **Max** | Haftalik |
| **API** | Surekli token-kovasi sistemi (sabit aralik yok) |

### API Hiz Siniri Kademeleri

| Kademe | Gerekli Depozit | Sinirlar |
|--------|-----------------|----------|
| Tier 1 | $5 | En dusuk RPM/TPM |
| Tier 2 | $50 | Orta |
| Tier 3 | $250 | Yuksek |
| Tier 4 | $400+ | En yuksek |

> **Ipucu:** Hiz sinirina yaklastiginizda Claude sizi uyarir. Limitler plan yukselterek veya API kademesi artirarak genisletilebilir.

---

## 6. Yetenekler (Capabilities)

Claude'un neler yapabilecegini acip kapatan ana kontrol paneli. Her ozellik bagimsiz olarak etkinlestirilebilir.

### Artifacts

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Artifacts** | ACIK | Yan panelde interaktif icerik olusturma (kod, belge, gorsel) |
| **Yapay Zeka Destekli Artifacts** | ACIK | Claude'un otomatik olarak Artifact olusturmasina izin verir |

**Artifacts ne yapar?**
- Kod parcalari, HTML sayfalari, React bilesenleri, SVG gorseller olusturur
- Izole bir sandbox ortaminda calisir (yerel dosyalara erisemez)
- Konusma iceriginden bagimsiz, tekrar kullanilabilir ciktilar uretir

> **Ne zaman kapatin:** Sadece metin tabanli yanitlar istiyorsaniz veya yan panel dikkatinizi dagitiyorsa.

### Satir Ici Gorsellestirmeler (Inline Visualizations)

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Satir ici gorsellestirmeler** | ACIK | Sohbet icinde interaktif grafik, diyagram, beyaz tahta |

**Artifacts ile farki:**
- Gorsellestirmeler **dusunme araclari**dir (surec odakli)
- Artifacts **teslim edilebilir ciktilar**dir (sonuc odakli)

> **Ipucu:** Veri analizi yaparken gorsellestirmeleri acik birakmaniz faydalıdır; Claude karmasik verileri otomatik grafiklerle ozetler.

### Arama ve Referans Sohbetler (Search and Reference Chats)

| Ayar | Varsayilan | Erisilebilirlik |
|------|-----------|-----------------|
| **Sohbet arama** | ACIK | Yalnizca Max, Team, Enterprise |

**Ne yapar?**
- Claude'a "gecen hafta X hakkinda ne konusmustuk?" diye sorabilirsiniz
- Gecmis konusmalari arar ve ilgili bilgileri getirir
- Otomatik degil, **istek uzerine** calisir
- Tum sohbetlerde veya belirli projelerde arama yapilabilir

> **Ipucu:** Onemli kararlari ve notlari projeler icinde organize ederseniz arama daha etkili olur.

### Sohbet Gecmisinden Bellek Olustur (Generate Memory from Chat History)

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Bellek olusturma** | ACIK | Claude konusmalardan tercihlerinizi otomatik ogrenir |

**Ne ogrenir?**
- Iletisim tarzi tercihleri
- Teknik yigin (tech stack) bilgileri
- Calismа aliskanliklari
- Proje baglami

**Yonetim:**
- "Bellegi goruntule ve duzenle" secenegi ile kayitlari inceleyebilirsiniz
- Tek tek bellekleri silebilir veya duzenleyebilirsiniz
- Proje bazli ve hesap geneli bellek ayri tutulur

> **Ipucu:** Periyodik olarak bellegi gozden gecirin. Yanlis ogrenilmis tercihleri silmek, Claude'un yanitlarini iyilestirir.

### Dosya Yuklemeleri ve Goruntu Analizi

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Dosya ve goruntu yukleme** | ACIK | Sohbete dosya ve gorsel yukleme |

**Sinirlar:**

| Parametre | Limit |
|-----------|-------|
| Dosya basina boyut | 30 MB |
| Konusma basina dosya | 20 dosya |
| Konusma basina gorsel | 20 gorsel (API: 600) |
| Gorsel formatlari | PNG, JPEG, GIF, WebP |
| PDF destegi | Ilk 100 sayfa gorsel analiz; sonrasi salt metin |

> **Ipucu:** 4K gorselleri 1080p'ye sikistirmak kaliteyi neredeyse hic etkilemez ama isleme hizini arttirir.

### Bulut Kod Yurutme ve Dosya Olusturma

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Bulut kod yurutme** | KAPALI | Claude'un bulut ortaminda kod calistirmasina izin verir |

**Etkinlestirme sureci:**
1. Organizasyon admini: Organizasyon ayarlari > Yetenekler'den acar
2. Bireysel kullanici: Ayarlar > Yetenekler'den kendi hesabinda etkinlestirir
3. Her iki adim da gereklidir

> **Ne zaman:** Python analiz scriptleri, veri isleme, grafik olusturma gibi gorevlerde Claude'un kodu dogrudan calistirmasini istediginizde.

### Arac Yukleme Tercihi

| Secenek | Aciklama |
|---------|----------|
| **Gerektiginde yukle** | Araclar yalnizca ihtiyac duyuldugunda aktif olur (hafif) |
| **Tumu otomatik yukle** | Tum mevcut araclar her konusmada hazir |

> **Ipucu:** "Gerektiginde yukle" token tuketimini azaltir. Cogu kullanici icin idealdir.

### Ag Erisimi (Network Egress)

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Ag erisimi** | ACIK | Claude'un dis aglara erisim izni |

> **Uyari:** Hassas verilerle calisirken bu ayari kapatmayi dusunun.

---

## 7. Baglayicilar (Connectors)

Claude'u dis servislerle entegre edin. 50'den fazla baglayici mevcuttur.

### Mevcut Baglayici Kategorileri

**Iletisim:**

| Baglayici | Ne Yapar |
|-----------|----------|
| **Gmail** | E-postalari oku, taslak olustur, yanit yaz |
| **Slack** | Kanallari oku, mesaj gonder, is parçaciklari ozetle |
| **Microsoft Teams** | Takim iletisimi entegrasyonu |

**Uretkenlik ve Bilgi:**

| Baglayici | Ne Yapar |
|-----------|----------|
| **Notion** | Sayfa oku/yaz, veritabani sorgula ve guncelle |
| **Google Drive** | Belgeler, tablolar, dosyalar uzerinde calis |
| **Asana** | Gorev yonetimi, proje takibi |
| **Monday.com** | Proje panosu entegrasyonu |

**Tasarim:**

| Baglayici | Ne Yapar |
|-----------|----------|
| **Figma** | FigJam'de akis semasi, Gantt grafigi olusturma |
| **Canva** | Tasarim sablonlari ile calisma |

**Kod ve Gelistirme:**

| Baglayici | Ne Yapar |
|-----------|----------|
| **GitHub** | Depo erisimi, PR inceleme, issue yonetimi |
| **GitLab** | Depo erisimi ve CI/CD takibi |
| **Jira** | Sorun izleme ve sprint yonetimi |

**Finans:**

| Baglayici | Ne Yapar |
|-----------|----------|
| **Stripe** | Odeme islemleri ve musteri verileri |
| **QuickBooks** | Muhasebe ve fatura yonetimi |

### Baglayici Kurulumu

```
1. Ayarlar > Baglayicilar (veya "Ozellestir" > "Baglayicilar")
2. "Uzantilara gozat" tiklayin
3. Eklemek istediginiz baglayiciyi secin
4. Ilk kullanimda OAuth ile dogrulayin
5. Claude'a gereken izinleri verin
```

### Izin Modeli

| Ozellik | Aciklama |
|---------|----------|
| **OAuth dogrulama** | Her servis icin ayri yetkilendirme |
| **Granüler izinler** | Servis bazinda okuma/yazma kontrolu |
| **Erisim iptali** | Istediginiz zaman baglayiciyi kaldiriniz |
| **Oturum surekliligi** | Baglayicilar sohbetler arasi aktif kalir |

> **Fiyatlandirma:** Tum planlarda ek ucret olmadan kullanilabilir.

> **Ipucu:** Bir baglayiciyi yalnizca aktif olarak kullanacaginiz zaman ekleyin. Kullanmadiklginiz entegrasyonlarin izinlerini iptal etmek guvenlik icin iyi bir pratiktir.

---

## 8. Claude Code

Claude Code CLI araci ve IDE entegrasyonu icin ayarlar. Bu bolum, uygulamadaki "Claude Code" sekmesini ve CLI yapilandirmasini birlikte kapsar.

### 8.1 Yapilandirma Hiyerarsisi

Claude Code ayarlari **4 katmanli oncelik sirasi** ile calisir:

```
Oncelik (yukari = en guclu)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ▲  Managed (IT/Admin)        → Kurum geneli, ezilemez
 │  CLI bayraklari            → Sadece o oturum
 │  .claude/settings.local    → Sen + bu proje (gitignore)
 │  .claude/settings.json     → Takim + bu proje (git'e eklenir)
 ▼  ~/.claude/settings.json   → Sen + tum projeler
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

| Kapsam | Dosya Yolu | Kimler Etkilenir | Paylasilir mi? |
|--------|-----------|------------------|---------------|
| **Kullanici** | `~/.claude/settings.json` | Sen, her projede | Hayir |
| **Proje** | `.claude/settings.json` | Tum katilimcilar | Evet (commit) |
| **Yerel** | `.claude/settings.local.json` | Sadece sen, bu projede | Hayir |
| **Yonetilen** | Admin tarafindan dagitilir | Organizasyondaki herkes | Zorla uygulanir |

**Ne zaman hangisi?**
- Kisisel tercihlerin (tema, model) → `~/.claude/settings.json`
- Takim standartlari (lint hook'lari, yasakli komutlar) → `.claude/settings.json`
- Gizli API anahtarlarin → `.claude/settings.local.json`

### 8.2 Genel Talimatlar (Global Instructions)

Tum Claude Code oturumlarinda gecerli olacak kalici talimatlar belirleyin:
- Tercih edilen ton ve cikti formati
- Arka plan bilgisi ve roller
- Istediginiz zaman guncelleyebilirsiniz

### 8.3 Proje Bazli Talimatlar

- Klasor seviyesinde baglam ekleyin
- Genel talimatlari belirli projeler icin ezin
- Klasor secildiginde otomatik uygulanir

### 8.4 Izinler (Permissions)

Claude'un neler yapip neler yapamayacagini kontrol eden en kritik ayar.

**Degerlendirme sirasi:**
```
deny  →  ask  →  allow
(ilk eslesen kazanir)
```

**Kural soz dizimi:**

| Oruntu | Aciklama | Ornek |
|--------|----------|-------|
| Arac adi | O aracin tum kullanimlari | `"Bash"`, `"Edit"` |
| `Arac(belirtec)` | Belirli kullanim | `"Bash(npm run build)"` |
| `Arac(desen *)` | Joker karakter | `"Bash(npm run *)"` |
| `mcp__sunucu__arac` | MCP arac izni | `"mcp__github__*"` |

**Pratik ornek:**
```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Edit(/src/**/*.ts)",
      "mcp__github__*"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(git push --force*)"
    ]
  }
}
```

**Izin modlari:**

| Mod | Ne Yapar | Ne Zaman |
|-----|----------|----------|
| `default` | Her arac icin ilk seferinde sorar | Gunluk gelistirme |
| `acceptEdits` | Dosya duzenlemelerini otomatik onaylar | Dosya islerinde guvendiginizde |
| `plan` | Analiz eder ama degistirmez | Kod inceleme, plan yapma |
| `auto` | Guvenlik siniflandiricisi karar verir | Hizli iterasyon |
| `bypassPermissions` | Hicbir sey sormaz | **SADECE** izole ortamlar |

### 8.5 Model Ayarlari

```json
{ "model": "opus" }
```

**Oncelik sirasi:**
1. Oturum ici: `/model opus`
2. Baslatirken: `--model opus`
3. Ortam degiskeni: `ANTHROPIC_MODEL=claude-opus-4-6`
4. Ayar dosyasi: `"model": "opus"`

**Efor seviyesi:**

| Seviye | Etki | Kullanim |
|--------|------|----------|
| `low` | Minimum dusunme | Basit degisiklikler |
| `medium` | Dengeli | Cogu gorev |
| `high` | Derin analiz | Karmasik problemler |
| `max` | Maksimum muhakeme | En zor gorevler |

### 8.6 Hook'lar (Otomatik Tetikleyiciler)

Claude'un yasam dongusundeki olaylara tepki tanimlayin.

**Olay zamanlama semasi:**
```
Oturum baslar ─→ SessionStart
                    │
Kullanici yazar ─→ UserPromptSubmit
                    │
Claude arac kullanir:
     ├─ PreToolUse    (oncesi — engelleyebilir)
     ├─ [arac calisir]
     └─ PostToolUse   (sonrasi — sonuc isleyebilir)
                    │
Claude durur ────→ Stop
                    │
Oturum biter ───→ SessionEnd
```

**Ornek — Her duzenleme sonrasi otomatik format:**
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

**Ornek — Korumali dosyalara dokunmayi engelleme:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if echo $TOOL_INPUT | jq -r '.file_path' | grep -q 'migration'; then exit 2; fi"
          }
        ]
      }
    ]
  }
}
```

**Hook tipleri:** `command` (kabuk komutu), `http` (POST istegi), `prompt` (LLM cagrisi), `agent` (alt-ajan)

**Cikis kodlari:** `0` = izin ver, `2` = engelle, diger = logla ama devam et

### 8.7 MCP Sunuculari

```json
// .claude/.mcp.json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["/path/to/github-mcp-server.js"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
```

| Baglanti Turu | Aciklama | Ornek |
|---------------|----------|-------|
| **stdio** | Yerel alt-surec | Python/Node script |
| **SSE** | Uzak HTTP/SSE | Bulut API'leri |
| **HTTP** | Uzak HTTP sunucu | Yerel servisler |

### 8.8 Sandbox (Kum Havuzu)

Dosya sistemi ve ag erisimini isletim sistemi seviyesinde sinirlayin:

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowRead": ["/home/user/project"],
      "allowWrite": ["/home/user/project/src"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

### 8.9 Ortam Degiskenleri

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "1",
    "ANTHROPIC_MODEL": "claude-opus-4-6"
  }
}
```

**Kritik degiskenler:**

| Degisken | Ne Yapar |
|----------|----------|
| `ANTHROPIC_API_KEY` | API dogrulamasi |
| `ANTHROPIC_MODEL` | Varsayilan model |
| `CLAUDE_CODE_EFFORT_LEVEL` | Efor seviyesi |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Alt-ajan modeli (maliyet optimizasyonu) |
| `MAX_THINKING_TOKENS` | Dusunme token butcesi |

### 8.10 IDE Entegrasyonu

- VS Code uzantisi ayarlari
- JetBrains IDE yapilandirmasi
- Otomatik IDE baglantisi (`autoConnectIde`)
- Otomatik uzanti kurulumu (`autoInstallIdeExtension`)

---

## 9. Cowork

Proje tabanli calisma alanlari olusturun, takimla isbirligi yapin ve tekrarlayan gorevleri otomatiklestirin.

### Genel Talimatlar

| Ayar | Aciklama |
|------|----------|
| **Genel talimatlar** | Her Cowork oturumunda gecerli olan kalici yonergeler |
| **Duzenleme** | Ayarlar > Cowork > Genel talimatlar yanindaki "Duzenle" |

Belirtebileceginiz seyler:
- Yanit tonu ve formati
- Rol ve uzmanlik alani
- Arka plan bilgisi

### Proje Bazli Baglam

| Ayar | Aciklama |
|------|----------|
| **Klasor talimatlari** | Proje bazinda ozel baglam |
| **Genel talimatlari ezme** | Proje talimatları genel talimatlari ezebilir |
| **Otomatik uygulama** | Proje secildiginde otomatik devreye girer |

### Proje Yonetimi

- Ozel proje calisma alanlari olusturun
- Dosyalar, baglantilar ve talimatlarla organize edin
- Her projenin ayri bellek ve bilgi tabani vardir

### Takim Isbirligi (Team/Enterprise)

| Ozellik | Aciklama |
|---------|----------|
| **Acik projeler** | Tum organizasyon uyeleri gorebilir |
| **Ozel projeler** | Yalnizca davetli uyeler erisebilir |
| **"Duzenleyebilir" rolu** | Talimat, bilgi tabani ve ayarlari degistirebilir |
| **"Goruntuleyebilir" rolu** | Salt okuma erisimi |

### Plugin Marketplace (Team/Enterprise)

- Adminler seçilmis plugin pazaryeri olusturabilir
- Takim uyelerinin gorecegi plugin'leri kontrol edin
- Organizasyon genelinde plugin dagitimi

### Admin Kontrolleri (Team/Enterprise)

| Kontrol | Aciklama |
|---------|----------|
| **Cowork'u ac/kapat** | Organizasyon ayarlari > Yetenekler |
| **Tum kullanicilar icin devre disi** | Organizasyon genelinde kapatma |
| **Plugin erisimi** | Takim seviyesinde plugin izinleri |

### Zamanlanmis Gorevler

| Ozellik | Aciklama |
|---------|----------|
| **Tekrar sikligi** | Gunluk, haftalik, aylik, yillik |
| **Otomatik yurutme** | Zamanlanmis gorevler belirlenen takvimde calisir |
| **Kullanim alani** | Tekrarlayan raporlar, periyodik kontroller |

> **Ipucu:** Haftalik sprint ozeti, gunluk kod kalite raporu gibi tekrarlayan gorevleri zamanlanmis gorev olarak tanimlayin.

---

## 10. Claude in Chrome (Beta)

Claude'u tarayicinizda otomasyon araci olarak kullanin.

> **Durum:** Beta ozelligi — aktif olarak gelistirilmektedir.

### Kurulum

1. Chrome Web Magazi'ndan uzantiyi yukleyin
2. Claude hesabinizla giris yapin
3. Site bazli izinleri yapilandirin

### Temel Ozellikler

#### Tarayici Kontrolu

| Yetenek | Aciklama |
|---------|----------|
| **Web sitelerinde gezinme** | Sayfalari okur, tiklar, form doldurur |
| **Site bazli izinler** | Her site icin ayri yetki |
| **Metin girisi** | Formlara yazma, arama yapma |
| **Navigasyon** | Sayfalar arasi gecis, sekme yonetimi |

#### Is Akisi Kaydi

1. Uzanti panelindeki **kayit simgesine** tiklayin
2. Claude'un ogrenmesini istediginiz adimlari gerceklestirin
3. Claude is akisini ogrenir ve tekrarlayabilir
4. Tekrarlayan tarayici gorevleri icin idealdir

> **Ornek:** "Her sabah X web sitesindeki raporlari indir" gibi bir is akisini kaydedin.

#### Zamanlanmis Gorevler

| Ayar | Aciklama |
|------|----------|
| **Saat simgesi** | Uzanti panelinden erisim |
| **Tekrar sikligi** | Gunluk, haftalik, aylik, yillik |
| **Otomatik yurutme** | Zamanlanan gorev arka planda calisir |

#### "Yapmadan Once Sor" Modu (Ask Before Acting)

| Ayar | Aciklama |
|------|----------|
| **Etkinlestirildiginde** | Claude her islem oncesi plan sunar, onay bekler |
| **Yuksek riskli islemler** | Plan onaylanmis olsa bile ek onay istenir |
| **Sagladigi guvence** | Beklenmedik islemleri engeller |

> **Ipucu:** Ilk kullanimda bu modu **ACIK** tutun. Claude'un davranisina alıstiktan sonra kapatabilirsiniz.

#### Model Secimi

| Plan | Kullanilabilir Model |
|------|---------------------|
| **Pro** | Yalnizca Haiku 4.5 |
| **Max / Team / Enterprise** | Tercih edilen model secilebilir |

#### Bildirimler

| Ayar | Aciklama |
|------|----------|
| **Bildirimler** | ACIK/KAPALI — izin istekleri ve tamamlanma uyarilari |
| **Arka plan gorevi** | Bildirimler acikken gorev arka planda calisabilir |

#### Gorsel Paylasma

- Ekran goruntusunu Claude ile paylasin
- Belirli ekran bolgesini yakalanin
- Gorselleri dogrudan sohbete yukleyin

### Guvenlik Kisitlamalari

| Kisitlama | Aciklama |
|-----------|----------|
| **Varsayilan engel listesi** | Yatirim platformlari, borsa, kripto uygulamalari |
| **Sistem uygulamalari** | Terminal, Finder, Sistem Ayarlari icin ek uyarilar |
| **Ek onay** | Yuksek etkili islemler ek dogrulama gerektirir |

> **Uyumlu tarayicilar:** Chrome, Brave, Edge (Chromium tabanli tum tarayicilar).

---

## 11. Masaustu Uygulamasi — Genel

Masaustu uygulamasina ozel ayarlar.

### Bilgisayar Kullanimi (Computer Use)

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Bilgisayar Kullanimi** | KAPALI | Claude'un bilgisayarinizla etkilesim kurmasina izin verir |

**Model erisilebilirligi:**

| Plan | Model |
|------|-------|
| **Pro** | Yalnizca Haiku 4.5 |
| **Max / Team / Enterprise** | Model secimi mevcut |

> **Ne yapar:** Claude fareyi hareket ettirebilir, tiklayabilir, klavyeyi kullanabilir — bir insan gibi bilgisayari kullanir.

### Engelli Uygulamalar (Denied Apps)

| Ayar | Aciklama |
|------|----------|
| **Engel listesi** | Claude'un erisemeyecegi uygulamalar |
| **Varsayilan engeller** | Yatirim platformlari, borsa, kripto uygulamalari |
| **Ekleme** | Istediginiz uygulamayi listeye ekleyebilirsiniz |

> **Not:** Engellenen uygulamalar Claude'a soru sormadan reddedilir. Ancak Claude, izin verilen bir uygulama uzerinden engelli bir uygulamayi **dolayli olarak** etkileyebilir.

### Uygulama Gizleme (Allow App Hiding)

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Uygulama gizleme** | ACIK | Claude calisirken diger pencereleri gizler |

**ACIK oldigunda:** Claude yalnizca hedef uygulama ile etkilesir — kaza riski azalir.
**KAPALI oldigunda:** Diger pencereler gorunur kalir.

> **Ipucu:** Bu ayari ACIK birakmak, Claude'un yanlis pencereye tiklamasini engeller.

### Ek Izinler

| Uygulama | Risk Notu |
|----------|-----------|
| **Terminal/Kabuk** | Genis sistem erisimi — ek uyari verilir |
| **Finder/Dosya Sistemi** | Dosya islemleri — ek uyari verilir |
| **Sistem Ayarlari** | Sistem yapilandirmasi — ek uyari verilir |

---

## 12. Masaustu Uygulamasi — Uzantilar (Extensions)

MCP tabanli eklentileri yonetin.

### Uzanti Gezgini

| Islem | Aciklama |
|-------|----------|
| **"Uzantilara gozat"** | Anthropic tarafindan incelenmis araclari goruntuler |
| **Tek tikla kurulum** | Uzantiyi secin ve yukleyin |
| **Yapilandirma** | API anahtari, dosya yolu gibi gereken ayarlari girin |

### Gelismis Ayarlar

| Islem | Aciklama |
|-------|----------|
| **"Gelismis ayarlar"** | Uzanti Gelistirici bolumune erisim |
| **Baglanti durumu** | Kurulu uzantilarin durum izlemesi |
| **MCP sunucu loglari** | Hata ayiklama icin log goruntuleme |

### Ozel Uzanti Yukleme

| Dosya Formati | Aciklama |
|---------------|----------|
| `.mcpb` | MCP Bundle — standart uzanti paketi |
| `.dxt` | Eski format (legacy) |

**Kurulum:**
1. "Uzanti Yukle..." tiklayin
2. `.mcpb` veya `.dxt` dosyasini secin
3. Yapilandirma istemlerini tamamlayin
4. `manifest.json` icindeki `user_config` alanlarini doldurun

### Calisma Zamani Destegi

| Ortam | Durum |
|-------|-------|
| **Node.js** | Dahili Node.js ile calisan MCP sunuculari |
| **Python** | Python MCP sunuculari desteklenir |
| **Binary** | Derlenrnis binary MCP sunuculari |
| **Docker** | Docker MCP entegrasyonu |

### Sorun Giderme

1. Yapilandirma ayarlarinda eksik alan var mi kontrol edin
2. API anahtarlari / kimlik bilgilerinin dogru oldugunu dogrulayin
3. Dosya yollarinin erisilebilir oldugunu kontrol edin
4. **macOS:** Sistem Tercihleri > Guvenlik ve Gizlilik > uyariları kontrol edin
5. **Windows:** Claude Desktop'un dizin erisim izinlerini dogrulayin
6. Uzanti Gelistirici bolumundeki loglari inceleyin

---

## 13. Masaustu Uygulamasi — Gelistirici (Developer)

Gelismis hata ayiklama ve gelistirici araclari.

### Uzanti Gelistirici Bolumu

| Ozellik | Aciklama |
|---------|----------|
| **Ozel uzanti olusturma** | Kendi masaustu uzantinizi gelistirin |
| **Ozel `.mcpb` yukleme** | Test amacli uzanti yukleyin |
| **Test ve hata ayiklama** | Uzantilari calistirma ortaminda test edin |
| **Kurulum arayuzu** | Uzanti yapilandirma paneli |

### MCP Sunucu Yonetimi

| Ozellik | Aciklama |
|---------|----------|
| **Baglanti durumu** | Tum MCP sunucularinin canli durumu |
| **Yerel sunucular** | Yerel MCP sunucu baglantilarini izleme |
| **Uzak sunucular** | Uzak MCP sunucu durum kontrolu |
| **Docker** | Docker MCP entegrasyon durumu |

### Loglama ve Hata Ayiklama

| Ozellik | Aciklama |
|---------|----------|
| **MCP sunucu loglari** | Baglanti ve islem loglari |
| **Baglanti hatalari** | Hata mesaji detaylari |
| **Yapilandirma sorunlari** | Ayar uyumsuzluklarini tespit |
| **Performans izleme** | Sunucu yanit surelerini gozlemleme |

> **Ipucu:** Bir uzanti calismiyorsa ilk adim her zaman Gelistirici bolumundeki loglari kontrol etmektir.

---

## Ek: Bellek ve Kisisellestirme

Claude'un sizi tanimasi ve tercihlerinizi hatirlamasi icin kullanilan sistem.

### Bellek Turleri

| Tur | Kapsam | Aciklama |
|-----|--------|----------|
| **Otomatik bellek** | Hesap geneli | Konusmalardan ogrenilen tercihler |
| **Kullanici tercihleri** | Hesap geneli | Elle girilen iletisim tarzi, arka plan bilgisi |
| **Proje bellegi** | Proje bazli | Her projeye ozel baglam ve ogrenilmis bilgiler |

### Otomatik Bellek

| Ayar | Varsayilan | Aciklama |
|------|-----------|----------|
| **Otomatik bellek** | ACIK | Konusmalardan tercih ogrenmesini etkinlestirir |

**Neler ogrenilir?**
- Derleme komutlari ve proje yapisi
- Hata ayiklama tercihleri
- Mimari notlar ve kararlar
- Kod tarzi tercihleri
- Is akisi aliskanliklari

**Yonetim:**
- Ayarlar > Yetenekler > "Bellegi goruntule ve duzenle"
- Tek tek kayitlari silebilir veya duzenleyebilirsiniz
- Tamamen sifirlamak mumkundur

> **Ipucu:** Ayda bir bellek kayitlarinizi gozden gecirin. Eskimis veya yanlis ogrenilmis tercihleri temizlemek yanitlarin kalitesini arttirir.

### Kullanici Tercihleri

| Alan | Ornek |
|------|-------|
| **Iletisim tarzi** | "Kisa ve teknik yanitlar tercih ederim" |
| **Arka plan** | "Senior backend gelistiriciyim, Go ve Python kullaniyorum" |
| **Genel tercihler** | "Kod orneklerinde yorum satirlari ekle" |

> Ayarlar > Kullanici Tercihleri'nden istediginiz zaman guncelleyebilirsiniz.

---

## Hizli Baslangic Sablonlari

### Bireysel Gelistirici (Claude Code)

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(npm *)", "Bash(git *)"],
    "deny": ["Bash(rm -rf *)", "Bash(sudo *)"]
  }
}
```

### Takim Projesi (Claude Code)

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(npm run *)", "Edit(/src/**)"],
    "deny": ["Bash(git push --force*)", "Bash(sudo *)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "npx prettier --write $(jq -r '.tool_input.file_path')" }]
      }
    ]
  }
}
```

### Kurumsal / Yonetilen (Claude Code)

```json
{
  "availableModels": ["sonnet", "haiku"],
  "model": "sonnet",
  "permissions": {
    "deny": ["Bash(sudo *)", "Bash(curl * | bash)", "Bash(wget *)"]
  },
  "sandbox": {
    "enabled": true,
    "network": {
      "allowedDomains": ["*.sirket.com", "github.com"]
    }
  },
  "allowManagedPermissionRulesOnly": true
}
```

---

## Varsayilan Degerler Ozet Tablosu

| Ayar | Varsayilan |
|------|-----------|
| Tema | System |
| Model | Claude Sonnet |
| Claude'u gelistirmeye yardim et | ACIK (Free/Pro/Team), KAPALI (Enterprise) |
| Gizli mod | KAPALI (konusma bazli) |
| Artifacts | ACIK |
| Yapay zeka destekli Artifacts | ACIK |
| Satir ici gorsellestirmeler | ACIK |
| Sohbet arama | ACIK (yalnizca Max/Team/Enterprise) |
| Bellek olusturma | ACIK |
| Dosya yuklemeleri | ACIK |
| Bulut kod yurutme | KAPALI (cift adimli etkinlestirme gerekir) |
| Arac yukleme | Gerektiginde yukle |
| Ag erisimi | ACIK |
| Bilgisayar Kullanimi (Desktop) | KAPALI |
| Uygulama gizleme (Desktop) | ACIK |
| Otomatik yenileme (Billing) | ACIK |
| Otomatik bellek | ACIK |
| Otomatik IDE baglantisi (Code) | KAPALI |
| Otomatik IDE uzanti kurulumu (Code) | ACIK |

---

## Klavye Kisayollari ve Hizli Komutlar

### Claude Code CLI Komutlari

| Komut | Ne Yapar |
|-------|----------|
| `/config` | Ayarlari interaktif duzenleme |
| `/model opus` | Modeli degistir |
| `/effort high` | Efor seviyesini artir |
| `/vim` | Vim modunu ac |
| `/cost` | Maliyet ozetini goster |
| `/compact` | Baglami sikistir |
| `/permissions` | Izin kurallarini duzenle |
| `/terminal-setup` | Terminal entegrasyonunu ayarla |
| `/theme` | Tema degistir |

### Satir Sonu Giris Yontemleri

| Yontem | Nasil |
|--------|-------|
| Ters slash | `\` + Enter |
| Shift+Enter | iTerm2, WezTerm, Ghostty, Kitty'de dogrudan |
| Option+Enter | Mac'te "Use Option as Meta Key" acik olmali |

---

*Bu rehber Claude uygulamasinin (web, masaustu, mobil) tum ayar sekmelerini kapsar. Interaktif kesfetmek icin uygulamada Ayarlar menusunu veya Claude Code'da `/config` komutunu kullanin.*
