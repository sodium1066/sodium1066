"""
Motivasyon ve Ödül Sistemi Modülü
==================================
DEHB icin tasarlanmıs motivasyon mekanizmaları.
- XP ve seviye sistemi (anında ödül geri bildirimi)
- Seri (streak) takibi
- Rozet koleksiyonu
- Günlük ipucları ve motivasyon mesajları
- Haftalık ilerleme özetleri
"""

import json
import os
import random
from datetime import datetime, timedelta


class MotivationSystem:
    """DEHB dostu motivasyon ve ödül sistemi."""

    # Seviye tablosu
    LEVELS = [
        {"level": 1, "title": "Yeni Baslangiç", "xp_required": 0},
        {"level": 2, "title": "Odak Ögrencisi", "xp_required": 100},
        {"level": 3, "title": "Calıskan Arı", "xp_required": 300},
        {"level": 4, "title": "Disiplin Ustası", "xp_required": 600},
        {"level": 5, "title": "Odak Savaşçısı", "xp_required": 1000},
        {"level": 6, "title": "Bilgi Avcısı", "xp_required": 1500},
        {"level": 7, "title": "Akademik Kahraman", "xp_required": 2200},
        {"level": 8, "title": "Üstün Basarılı", "xp_required": 3000},
        {"level": 9, "title": "Ders Efsanesi", "xp_required": 4000},
        {"level": 10, "title": "DEHB Ustası", "xp_required": 5500},
    ]

    # Ödül XP degerleri
    REWARDS = {
        "pomodoro_complete": {"xp": 25, "message": "Pomodoro tamamlandı! +25 XP"},
        "task_complete": {"xp": 50, "message": "Görev tamamlandı! +50 XP"},
        "quick_focus": {"xp": 15, "message": "Hızlı odaklanma basarılı! +15 XP"},
        "streak_bonus": {"xp": 30, "message": "Seri bonusu! +30 XP"},
        "first_session": {"xp": 20, "message": "Günün ilk oturumu! +20 XP"},
    }

    # DEHB ipucları
    TIPS = [
        "Calısma masanı temiz ve düzenli tut. Dağınıklık dikkat dağıtır.",
        "Telefonunu sessiz moda al veya baska bir odaya bırak.",
        "Her pomodoro arasında kalk ve kısa bir yürüyüs yap.",
        "Su icmeyi unutma! Dehidrasyon odaklanmayı azaltır.",
        "Büyük görevler bunaltıcı olabilir. Küçük adımlara böl!",
        "Kendini ödüllendir! Her tamamlanan görev bir basarıdır.",
        "Mükemmel olması gerekmiyor. Baslamak bitirmenin yarısıdır.",
        "Calısma ortamında gürültü varsa kulaklık kullan.",
        "Calısma planını önceden hazırla. Ne yapacağını bilmek odaklanmayı kolaylastırır.",
        "Uyku düzenin calısma verimini doğrudan etkiler. Düzenli uyumaya calıs.",
        "Zor konularla enerjin yüksekken ilgilen, kolay konuları sonraya bırak.",
        "Bir sey calısmaya basladığında ilk 5 dakika en zor kısımdır. Sonra kolaylaşır!",
        "Not almak hem odaklanmayı artırır hem de tekrarı kolaylastırır.",
        "Calıstığın konuyu baska birine anlatmayı hayal et - anlama derinlesir.",
        "Hata yapmak öğrenmenin bir parçası. Kendine sert davranma.",
        "Timer kullanmak DEHB icin cok etkili bir stratejidir. Zamanı görünür kıl!",
        "Calısma sırasında bir sey aklına gelirse hemen bir kağıda yaz, sonra devam et.",
        "Aynı konuyu uzun süre calısmak yerine konular arası gecis yap.",
        "Müzik dinlemek istiyorsan, sözsüz müzik veya lo-fi tercih et.",
        "Kendini baskaları ile kıyaslama. Dünkü kendinle kıyasla.",
    ]

    # Rozet tanımları
    BADGE_DEFINITIONS = {
        "first_pomodoro": {"name": "İlk Adım", "description": "İlk pomodoronu tamamla", "condition": lambda s: s.get("total_pomodoros", 0) >= 1},
        "five_pomodoros": {"name": "Beşli", "description": "5 pomodoro tamamla", "condition": lambda s: s.get("total_pomodoros", 0) >= 5},
        "ten_pomodoros": {"name": "On Numara", "description": "10 pomodoro tamamla", "condition": lambda s: s.get("total_pomodoros", 0) >= 10},
        "fifty_pomodoros": {"name": "Yarım Asır", "description": "50 pomodoro tamamla", "condition": lambda s: s.get("total_pomodoros", 0) >= 50},
        "first_task": {"name": "Görev Avcısı", "description": "İlk görevini tamamla", "condition": lambda s: s.get("tasks_completed", 0) >= 1},
        "ten_tasks": {"name": "Görev Uzmanı", "description": "10 görev tamamla", "condition": lambda s: s.get("tasks_completed", 0) >= 10},
        "three_day_streak": {"name": "Üç Günlük Seri", "description": "3 gün üst üste çalış", "condition": lambda s: s.get("streak", 0) >= 3},
        "seven_day_streak": {"name": "Haftalık Seri", "description": "7 gün üst üste çalış", "condition": lambda s: s.get("streak", 0) >= 7},
        "thirty_day_streak": {"name": "Aylık Seri", "description": "30 gün üst üste çalış", "condition": lambda s: s.get("streak", 0) >= 30},
        "hour_focus": {"name": "Saat Ustası", "description": "Tek seferde 60 dk odaklan", "condition": lambda s: s.get("max_session_minutes", 0) >= 60},
    }

    def __init__(self, config):
        self.config = config
        self.data_file = config.get("motivation_file", "motivation_data.json")
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_data()

    def _default_data(self):
        return {
            "xp": 0,
            "total_pomodoros": 0,
            "tasks_completed": 0,
            "streak": 0,
            "last_study_date": None,
            "badges": [],
            "daily_sessions": [],
            "max_session_minutes": 0,
        }

    def _save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def earn_reward(self, reward_type):
        """Ödül kazanır ve XP ekler."""
        reward = self.REWARDS.get(reward_type)
        if not reward:
            return ""

        self.data["xp"] = self.data.get("xp", 0) + reward["xp"]

        # Istatistikleri güncelle
        if reward_type == "pomodoro_complete":
            self.data["total_pomodoros"] = self.data.get("total_pomodoros", 0) + 1
        elif reward_type == "task_complete":
            self.data["tasks_completed"] = self.data.get("tasks_completed", 0) + 1

        # Seri kontrol
        self._update_streak()

        # Rozet kontrol
        new_badges = self._check_badges()

        # Seviye atlama kontrol
        level_up = self._check_level_up()

        self._save_data()

        message = reward["message"]
        if level_up:
            message += f"\n   🎉 SEVİYE ATLADIN! Yeni seviye: {level_up['title']}"
        for badge in new_badges:
            message += f"\n   🏅 Yeni rozet: {badge}"

        return message

    def _update_streak(self):
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = self.data.get("last_study_date")

        if last_date == today:
            return  # Bugün zaten calıstı

        if last_date:
            last = datetime.strptime(last_date, "%Y-%m-%d")
            diff = (datetime.now() - last).days
            if diff == 1:
                self.data["streak"] = self.data.get("streak", 0) + 1
            elif diff > 1:
                self.data["streak"] = 1  # Seri kırıldı
        else:
            self.data["streak"] = 1

        self.data["last_study_date"] = today

        # Günlük oturum kaydet
        sessions = self.data.get("daily_sessions", [])
        sessions.append({
            "date": today,
            "timestamp": datetime.now().isoformat(),
        })
        # Son 90 günü tut
        cutoff = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        self.data["daily_sessions"] = [s for s in sessions if s["date"] >= cutoff]

    def _check_badges(self):
        """Yeni kazanılan rozetleri kontrol eder."""
        new_badges = []
        current_badges = set(self.data.get("badges", []))

        for badge_id, badge_def in self.BADGE_DEFINITIONS.items():
            if badge_id not in current_badges:
                if badge_def["condition"](self.data):
                    current_badges.add(badge_id)
                    new_badges.append(badge_def["name"])

        self.data["badges"] = list(current_badges)
        return new_badges

    def _check_level_up(self):
        """Seviye atlama kontrol eder."""
        xp = self.data.get("xp", 0)
        current_level = self._get_current_level()
        next_level_idx = current_level["level"]  # 0-indexed olduğu icin

        if next_level_idx < len(self.LEVELS):
            next_level = self.LEVELS[next_level_idx]
            if xp >= next_level["xp_required"]:
                return next_level
        return None

    def _get_current_level(self):
        xp = self.data.get("xp", 0)
        current = self.LEVELS[0]
        for level in self.LEVELS:
            if xp >= level["xp_required"]:
                current = level
            else:
                break
        return current

    def get_level_info(self):
        """Mevcut seviye bilgilerini döndürür."""
        current = self._get_current_level()
        xp = self.data.get("xp", 0)

        # Sonraki seviye icin gereken XP
        next_idx = current["level"]  # level 1 -> index 1 (sonraki)
        if next_idx < len(self.LEVELS):
            next_xp = self.LEVELS[next_idx]["xp_required"]
        else:
            next_xp = xp  # Max level

        return {
            "level": current["level"],
            "title": current["title"],
            "xp": xp,
            "next_level_xp": next_xp,
        }

    def get_streak(self):
        """Mevcut seri günü döndürür."""
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = self.data.get("last_study_date")

        if not last_date:
            return 0

        if last_date == today:
            return self.data.get("streak", 0)

        last = datetime.strptime(last_date, "%Y-%m-%d")
        diff = (datetime.now() - last).days
        if diff <= 1:
            return self.data.get("streak", 0)
        return 0  # Seri kırıldı

    def get_daily_tip(self):
        """Günlük rastgele bir DEHB ipucu döndürür."""
        # Güne göre sabit bir ipucu sec (aynı gün aynı ipucu)
        day_of_year = datetime.now().timetuple().tm_yday
        idx = day_of_year % len(self.TIPS)
        return self.TIPS[idx]

    def get_badges(self):
        """Kazanılan rozet isimlerini döndürür."""
        badge_ids = self.data.get("badges", [])
        badge_names = []
        for bid in badge_ids:
            if bid in self.BADGE_DEFINITIONS:
                badge_names.append(self.BADGE_DEFINITIONS[bid]["name"])
        return badge_names

    def get_weekly_summary(self):
        """Haftalık calısma özetini döndürür."""
        history_file = self.config.get("history_file", "study_history.json")
        if not os.path.exists(history_file):
            return None

        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

        # Son 7 günün verilerini topla
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        recent = [h for h in history if h.get("date", "") >= week_ago]

        if not recent:
            return None

        total_minutes = sum(h.get("total_focus_minutes", 0) for h in recent)
        total_pomodoros = sum(h.get("completed_pomodoros", 0) for h in recent)
        tasks_completed = sum(h.get("completed_tasks", 0) for h in recent)

        # En verimli gün
        daily_minutes = {}
        for h in recent:
            day = h.get("date", "")[:10]
            daily_minutes[day] = daily_minutes.get(day, 0) + h.get("total_focus_minutes", 0)

        best_day = max(daily_minutes, key=daily_minutes.get) if daily_minutes else "N/A"

        # Gün adına cevir
        day_names = {
            0: "Pazartesi", 1: "Salı", 2: "Carsamba",
            3: "Persembe", 4: "Cuma", 5: "Cumartesi", 6: "Pazar",
        }
        try:
            best_day_dt = datetime.strptime(best_day, "%Y-%m-%d")
            best_day_name = day_names.get(best_day_dt.weekday(), best_day)
        except ValueError:
            best_day_name = best_day

        return {
            "total_minutes": total_minutes,
            "total_pomodoros": total_pomodoros,
            "tasks_completed": tasks_completed,
            "best_day": best_day_name,
            "streak": self.get_streak(),
        }
