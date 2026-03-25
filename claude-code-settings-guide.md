# Claude Code Ayarlar Haritasi — Kusbakisi Rehber

> Her sekmenin ne ise yaradigi, ne zaman lazim olacagi ve pratik orneklerle aciklanmasi.

---

## Dosya Hiyerarsisi: Ayarlar Nerede Yasar?

```
Oncelik (yukari = en guclu)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ▲  Managed (IT/Admin)        → Kurum geneli, ezilEMEZ
 │  CLI bayraklari            → Sadece o oturum
 │  .claude/settings.local    → Sen + bu proje (gitignore)
 │  .claude/settings.json     → Takim + bu proje (git'e eklenir)
 ▼  ~/.claude/settings.json   → Sen + tum projeler
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

| Kapsam | Dosya Yolu | Kimler Etkilenir | Takimla Paylasilir mi? |
|--------|-----------|------------------|----------------------|
| **Kullanici** | `~/.claude/settings.json` | Sen, her projede | Hayir |
| **Proje** | `.claude/settings.json` | Tum katilimcilar | Evet (commit edilir) |
| **Yerel** | `.claude/settings.local.json` | Sadece sen, bu projede | Hayir |
| **Yonetilen** | Admin tarafindan dagitilir | Organizasyondaki herkes | Evet (zorla uygulanir) |

**Ne zaman hangisi?**
- Kisisel tercihlerin (tema, model) → `~/.claude/settings.json`
- Takim standartlari (lint hook'lari, yasakli komutlar) → `.claude/settings.json`
- Gizli API anahtarlarin, kisisel MCP tokenlar → `.claude/settings.local.json`

---

## 1. Izinler (Permissions)

Claude'un neler yapip neler yapamayacagini kontrol eden en kritik sekme.

### Izin Degerlendirme Sirasi

```
deny  →  ask  →  allow
(ilk eslesen kazanir)
```

### Kural Soz Dizimi

| Oruntu | Aciklama | Ornek |
|--------|----------|-------|
| Arac adi | O aracin tum kullanimlari | `"Bash"`, `"Edit"` |
| `Arac(belirtec)` | Belirli kullanim | `"Bash(npm run build)"` |
| `Arac(desen *)` | Joker karakter | `"Bash(npm run *)"` |
| `mcp__sunucu__arac` | MCP arac izni | `"mcp__github__*"` |

### Pratik Ornekler

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",        // npm scriptlerini sor-ma-dan calistir
      "Bash(git status)",       // git status her zaman serbest
      "Edit(/src/**/*.ts)",     // src altindaki TS dosyalarini duzenleyebilir
      "mcp__github__*"          // GitHub MCP araclarinin hepsi serbest
    ],
    "deny": [
      "Bash(rm -rf *)",         // tehlikeli silme ASLA
      "Bash(sudo *)",           // root erisimi ASLA
      "Bash(git push --force*)" // force push engellendi
    ]
  }
}
```

> **Ipucu:** Yeni bir projeye baslarken `deny` listesini once olusturun. Guvensiz komutlari engellemek, guvenli komutlara izin vermekten daha onceliklidir.

### Izin Modlari

| Mod | Ne Yapar | Ne Zaman Kullanilir |
|-----|----------|---------------------|
| `default` | Her arac icin ilk seferinde sorar | Gunluk gelistirme |
| `acceptEdits` | Dosya duzenlemelerini otomatik onaylar | Claude'a dosya islerinde guvendiginde |
| `plan` | Analiz eder ama degistirmez | Kodu incelemek, plan yapmak icin |
| `auto` | Arka plan guvenlik siniflandiricisi karar verir | Hizli iterasyon |
| `bypassPermissions` | Hicbir sey sormaz | **SADECE** izole ortamlar (container/VM) |

> **Ipucu:** Buyuk bir refactor oncesi `plan` moduna gecin. Claude kodu okuyup plan cikarsin, siz onaylayin, sonra `default` moduna donun.

---

## 2. Model Ayarlari

### Model Secimi

| Alias | Guc | Hiz | Ne Zaman |
|-------|-----|-----|----------|
| `sonnet` | ★★★★☆ | Hizli | Gunluk kodlama, PR inceleme, bug fix |
| `opus` | ★★★★★ | Yavas | Mimari kararlar, karmasik mantik, buyuk refactor |
| `haiku` | ★★★☆☆ | En hizli | Basit gorevler, arka plan islemleri |
| `sonnet[1m]` | ★★★★☆ | Orta | Cok buyuk kod tabanlariyla calisirken |
| `opus[1m]` | ★★★★★ | Yavas | Karmasik + cok buyuk baglam gerektiginde |

```json
{
  "model": "opus"
}
```

**Oncelik sirasi:**
1. Oturum ici: `/model opus`
2. Baslatirken: `--model opus`
3. Ortam degiskeni: `ANTHROPIC_MODEL=claude-opus-4-6`
4. Ayar dosyasi: `"model": "opus"`

### Efor Seviyesi

| Seviye | Etki | Kullanim |
|--------|------|----------|
| `low` | Minimum dusunme, hizli cevap | Basit sorular, tek satirlik degisiklikler |
| `medium` | Dengeli | Cogu gorev icin ideal |
| `high` | Derin analiz | Karmasik bug'lar, mimari kararlar |
| `max` | Maksimum muhakeme | En zor problemler (sadece oturumda) |

```json
{ "effortLevel": "medium" }
```

> **Ipucu:** Normalde `medium` kullanin, takildiginizda `/effort high` ile gecici olarak artirin.

### Ucuncu Parti Saglayicilar (Bedrock/Vertex)

```json
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456:inference-profile/opus",
    "claude-sonnet-4-6": "us.anthropic.claude-sonnet-4-6-v1"
  }
}
```

> **Ipucu:** Sirket VPN'i arkasindan Anthropic API'ye erisemiyorsaniz, AWS Bedrock veya Google Vertex uzerinden model yonlendirmesi yapin.

---

## 3. Hook'lar (Otomatik Tetikleyiciler)

Claude'un yasam dongusundeki olaylara otomatik tepkiler tayin edin.

### Olay Zamanlama Seması

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

### En Kullanisli Hook Ornekleri

**Her dosya duzenlemesinden sonra otomatik format:**
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
> **Ne zaman:** Takiminizda prettier/eslint kullaniyorsaniz. Claude'un yapacagi her degisiklik otomatik formatlanir.

**Claude beklerken masaustu bildirimi:**
```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude Code' 'Dikkatiniz gerekiyor'"
          }
        ]
      }
    ]
  }
}
```
> **Ne zaman:** Uzun sureli gorevlerde baska sekmede calisirken.

**Korumali dosyalara dokunmayi engelleme:**
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
> **Ne zaman:** Veritabani migration dosyalarini, production config'lerini veya kilit dosyalari kazara degistirmek istemezsiniz.

### Hook Tipleri

| Tip | Aciklama | Kullanim |
|-----|----------|----------|
| `command` | Kabuk komutu calistirir | Format, lint, bildirim |
| `http` | HTTP endpoint'e POST atar | Dis servisler, loglama |
| `prompt` | Tek LLM cagrisi yapar | Basit evet/hayir kararlari |
| `agent` | Alt-ajan baslatir | Karmasik dogrulama |

### Cikis Kodlari

| Kod | Anlam |
|-----|-------|
| `0` | Izin ver / basarili |
| `2` | ENGELLE — islemi durdur |
| Diger | Logla ama devam et |

---

## 4. MCP Sunuculari

Claude'un disaridan arac entegrasyonlari.

### Yapilandirma

```json
// .claude/.mcp.json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["/path/to/github-mcp-server.js"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    },
    "database": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

### Baglanti Turleri

| Tur | Aciklama | Ornek |
|-----|----------|-------|
| **stdio** | Yerel alt-surec | Python/Node script |
| **SSE** | Uzak HTTP/SSE | Bulut API'leri |
| **HTTP** | Uzak HTTP sunucu | Yerel servisler |

> **Ipucu:** Bir MCP sunucusunun tum araclarini topluca acmak icin: `"mcp__sunucu_adi__*"` izin kuralini kullanin.

### Izin Kontrolu

```json
{
  "permissions": {
    "allow": ["mcp__github__*"],           // GitHub MCP hepsi serbest
    "deny": ["mcp__database__drop_table"]  // tablo silme yasak
  }
}
```

---

## 5. Ortam Degiskenleri (env)

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "1",
    "ANTHROPIC_MODEL": "claude-opus-4-6"
  }
}
```

### Kritik Ortam Degiskenleri

| Degisken | Ne Yapar | Ornek |
|----------|----------|-------|
| `ANTHROPIC_API_KEY` | API dogrulamasi | Otomatik ayarlanir |
| `ANTHROPIC_MODEL` | Varsayilan model | `claude-opus-4-6` |
| `CLAUDE_CODE_EFFORT_LEVEL` | Efor seviyesi | `low`, `medium`, `high` |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Alt-ajan modeli | `claude-haiku-4-5` |
| `DISABLE_PROMPT_CACHING` | Onbellegi kapat | `1` |
| `MAX_THINKING_TOKENS` | Sabit dusunme butcesi | `4000` |
| `DEBUG` | Hata ayiklama loglari | `1` |

> **Ipucu:** Alt-ajanlar icin ucuz model kullanmak maliyeti dusurur:
> `"CLAUDE_CODE_SUBAGENT_MODEL": "claude-haiku-4-5"`

---

## 6. Gorunum ve Terminal

### Tema

```json
{ "theme": "dark" }   // "light", "dark", "auto"
```

### Vim Modu

```json
{ "editorMode": "vim" }
```

> **Ipucu:** Vim kullanicisiyseniz `/vim` ile aninda acin. `Esc`, `i`, `dd`, `yy` gibi temel keybinding'ler desteklenir.

### Durum Cubugu (Status Line)

```json
{
  "statusLine": "{{model}} | %{{context_percentage}} baglam | {{git_branch}}"
}
```

**Kullanilabilir degiskenler:** `{{model}}`, `{{context_percentage}}`, `{{context_used}}`, `{{context_total}}`, `{{working_dir}}`, `{{git_branch}}`

> **Ipucu:** Baglam yuzdesini gorunur tutmak, ne zaman `/compact` calistirmaniz gerektigini anlamanizi saglar.

### Klavye Ayarlari

```json
// ~/.claude/keybindings.json
{
  "global": {
    "ctrl+l": "clearHistory",
    "ctrl+d": "exit"
  }
}
```

### Satir Sonu Giris Yontemleri

| Yontem | Nasil |
|--------|-------|
| Ters slash | `\` + Enter |
| Shift+Enter | iTerm2, WezTerm, Ghostty, Kitty'de dogrudan |
| Option+Enter | Mac'te Terminal ayarindan "Use Option as Meta Key" acin |

---

## 7. Baglam Yonetimi ve Dosyalar

### Ek Dizinler

Projenin disindaki klasorlere erisim verin:

```json
{
  "additionalDirectories": [
    "/home/user/shared-libs",
    "~/design-tokens"
  ]
}
```
> **Ne zaman:** Monorepo disindaki paylasilan kutuphane veya config dosyalarina erismeniz gerektiginde.

### Hassas Dosyalari Haric Tutma

```json
{
  "excludedFiles": [
    "**/.env",
    "**/*.secret",
    "**/node_modules/**",
    "**/.git/**"
  ]
}
```
> **Ne zaman:** Claude'un okumamasini istediginiz gizli dosyalar veya gereksiz buyuk klasorler varsa.

### Otomatik Sikistirma

```json
{
  "contextManagement": {
    "autoCompact": true,
    "compactThreshold": 0.85
  }
}
```
> **Ne zaman:** Uzun oturumlarda baglam penceresi dolarken otomatik sikistirma istiyorsaniz. %85 esik degeri cogu durum icin idealdir.

---

## 8. Sandbox (Kum Havuzu)

Claude'un dosya sistemi ve ag erisimini isletim sistemi seviyesinde sinirlayin.

```json
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowRead": ["/home/user/project"],
      "allowWrite": ["/home/user/project/src"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"]
    }
  }
}
```

> **Ne zaman:** Guvenmediginiz MCP sunuculari veya uretim ortamina yakin sistemlerde calisirken. Dosya sistemi ve ag erisimini en dar kapsamda tutun.

---

## 9. Skill'ler ve Alt-Ajanlar

### Skill Dizini

```
.claude/skills/
├── lint-fix.md       ← /lint-fix ile cagirilir
├── deploy-staging.md ← /deploy-staging ile cagirilir
└── review-pr.md      ← /review-pr ile cagirilir
```

### Skill Sablonu

```markdown
---
name: lint-fix
description: Lint hatalarini otomatik duzeltir
tags: [lint, format]
---

Projedeki tum lint hatalarini bul ve duzelt.
`npm run lint -- --fix` komutunu calistir.
```

### Alt-Ajan Yapilandirmasi

```
.claude/agents/
└── security-reviewer.md
```

```markdown
---
name: security-reviewer
description: Guvenlik incelemesi yapar
model: opus
tools: [Read, Grep, Glob]
permissions:
  defaultMode: plan
---

Kod degisikliklerini OWASP Top 10 aciklarina karsi incele.
```

> **Ipucu:** Alt-ajanlara `plan` modu verin — sadece okuyup raporlasinlar, degisiklik yapmasinlar.

---

## 10. Kimlik Dogrulama ve Maliyet

### Giris

```bash
claude login              # Anthropic hesabi
claude login --team       # Takim hesabi
```

### Maliyet Takibi

Oturum ici: `/cost` komutu

> **Ipucu:** `CLAUDE_CODE_SUBAGENT_MODEL` ile alt-ajanlari haiku'ya cekmek, toplam maliyeti %60-70 dusurur.

---

## Hizli Baslangic Sablon Karsilastirmasi

### Bireysel Gelistirici

```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(npm *)", "Bash(git *)"],
    "deny": ["Bash(rm -rf *)", "Bash(sudo *)"]
  },
  "theme": "dark"
}
```

### Takim Projesi

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
  },
  "excludedFiles": ["**/.env", "**/*.key"]
}
```

### Kurumsal / Yonetilen

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

## Komut Hatirlat Karti

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

---

*Bu rehber Claude Code'un tum ana ayar kategorilerini kapsar. Interaktif kesfetmek icin oturumda `/config` komutunu kullanin.*
