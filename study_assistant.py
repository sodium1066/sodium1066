#!/usr/bin/env python3
"""
DEHB Ders Calısma Asistanı - Ana Uygulama
==========================================
DEHB (Dikkat Eksikligi Hiperaktivite Bozuklugu) olan bireyler icin
ozel olarak tasarlanmıs tam otomatik ders calısma asistanı.

Ozellikler:
- DEHB'ye uygun kısa Pomodoro döngüleri (varsayılan 25dk calısma / 5dk mola)
- Otomatik görev parcalama (büyük görevleri küçük adımlara böler)
- Görsel ve sesli hatırlatmalar
- Motivasyon ve ödül sistemi
- Günlük/haftalık ilerleme takibi
- Odaklanma skoru hesaplama
"""

import json
import os
import sys
import time
import signal
from datetime import datetime, timedelta

from pomodoro import PomodoroTimer
from task_manager import TaskManager
from motivation import MotivationSystem
from config import Config


class StudyAssistant:
    """DEHB icin optimize edilmis ders calısma asistanı."""

    def __init__(self, config_path="config.json"):
        self.config = Config(config_path)
        self.pomodoro = PomodoroTimer(self.config)
        self.task_manager = TaskManager(self.config)
        self.motivation = MotivationSystem(self.config)
        self.session_start = None
        self.session_data = {
            "completed_pomodoros": 0,
            "completed_tasks": 0,
            "total_focus_minutes": 0,
            "breaks_taken": 0,
            "focus_score": 0.0,
        }
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, signum, frame):
        print("\n\n--- Oturum sonlandırılıyor ---")
        self._show_session_summary()
        self._save_session()
        sys.exit(0)

    def start(self):
        """Ana calısma oturumunu baslatır."""
        self._clear_screen()
        self._show_welcome()
        self.session_start = datetime.now()

        while True:
            choice = self._show_main_menu()

            if choice == "1":
                self._start_study_session()
            elif choice == "2":
                self._manage_tasks()
            elif choice == "3":
                self._view_progress()
            elif choice == "4":
                self._quick_focus_mode()
            elif choice == "5":
                self._settings()
            elif choice == "6":
                self._show_session_summary()
                self._save_session()
                print("\nBasarılar! Bugün harika is cıkardın! 💪")
                break
            else:
                print("Gecersiz secim, tekrar dene.")

    def _show_welcome(self):
        print("=" * 50)
        print("   DEHB Ders Calısma Asistanı")
        print("=" * 50)
        now = datetime.now()
        print(f"\n   Tarih: {now.strftime('%d.%m.%Y %H:%M')}")

        greeting = self._get_greeting(now.hour)
        print(f"\n   {greeting}")

        streak = self.motivation.get_streak()
        if streak > 0:
            print(f"   Seri: {streak} gün üst üste calıstın!")

        daily_tip = self.motivation.get_daily_tip()
        print(f"\n   Günün ipucu: {daily_tip}")
        print("=" * 50)

    def _get_greeting(self, hour):
        if hour < 6:
            return "Gece kusu! Erken yatmayı unutma."
        elif hour < 12:
            return "Günaydın! Sabah saatleri odaklanmak icin harika."
        elif hour < 17:
            return "Iyi öğleden sonralar! Enerjini yüksek tut."
        elif hour < 21:
            return "Iyi aksamlar! Aksam calısması icin hazır mısın?"
        else:
            return "Gec saatler! Kısa bir oturum yeterli olabilir."

    def _show_main_menu(self):
        print("\n--- Ana Menü ---")
        print("[1] Ders Calısmaya Basla (Pomodoro)")
        print("[2] Görevlerimi Yönet")
        print("[3] Ilerleme Raporlarım")
        print("[4] Hızlı Odaklanma Modu (10dk)")
        print("[5] Ayarlar")
        print("[6] Cıkıs")
        return input("\nSecimin: ").strip()

    def _start_study_session(self):
        """Pomodoro tabanlı calısma oturumu baslatır."""
        self._clear_screen()
        print("\n--- Calısma Oturumu ---\n")

        # Görev sec veya serbest calısma
        task = self._select_task_for_session()

        if task:
            print(f"Görev: {task['title']}")
            if task.get("subtasks"):
                print("Alt adımlar:")
                for i, sub in enumerate(task["subtasks"], 1):
                    status = "✓" if sub.get("done") else " "
                    print(f"  [{status}] {i}. {sub['title']}")

        num_pomodoros = self._ask_pomodoro_count()
        completed = 0

        for i in range(num_pomodoros):
            print(f"\n--- Pomodoro {i+1}/{num_pomodoros} ---")

            # Calısma periyodu
            focus_result = self.pomodoro.start_focus()
            if focus_result["completed"]:
                completed += 1
                self.session_data["completed_pomodoros"] += 1
                self.session_data["total_focus_minutes"] += focus_result["duration_minutes"]

                reward = self.motivation.earn_reward("pomodoro_complete")
                print(f"\n{reward}")

                # Mola
                if i < num_pomodoros - 1:
                    if (i + 1) % self.config.get("long_break_interval", 4) == 0:
                        print("\nUzun mola zamanı! Bunu hak ettin.")
                        self.pomodoro.start_long_break()
                    else:
                        print("\nKısa mola zamanı!")
                        self.pomodoro.start_short_break()
                    self.session_data["breaks_taken"] += 1
            else:
                print("\nPomodoro yarıda kesildi.")
                partial_minutes = focus_result.get("elapsed_minutes", 0)
                self.session_data["total_focus_minutes"] += partial_minutes
                break

        if task and completed > 0:
            self._update_task_progress(task)

        self._calculate_focus_score()
        print(f"\nTamamlanan: {completed}/{num_pomodoros} pomodoro")

    def _select_task_for_session(self):
        pending = self.task_manager.get_pending_tasks()
        if not pending:
            print("Kayıtlı görev yok. Serbest calısma modunda devam ediyorsun.\n")
            return None

        print("Hangi görev üzerinde calısmak istiyorsun?")
        print("[0] Serbest calısma (görev secme)")
        for i, task in enumerate(pending[:5], 1):
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                task.get("priority", "medium"), "⚪"
            )
            print(f"[{i}] {priority_icon} {task['title']}")

        choice = input("\nSecimin: ").strip()
        if choice == "0" or not choice:
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                return pending[idx]
        except ValueError:
            pass
        return None

    def _ask_pomodoro_count(self):
        work_min = self.config.get("work_duration", 25)
        print(f"\nKac pomodoro calısmak istiyorsun? (Her biri {work_min} dk)")
        print("[1] 1 pomodoro - Hafif oturum")
        print("[2] 2 pomodoro - Orta oturum")
        print("[3] 3 pomodoro - Yoğun oturum")
        print("[4] 4 pomodoro - Maraton oturum")

        choice = input("Secimin (varsayılan 2): ").strip()
        try:
            count = int(choice)
            return max(1, min(count, 8))
        except ValueError:
            return 2

    def _update_task_progress(self, task):
        print("\nGörev ilerlemesi nasıl?")
        print("[1] Görevi tamamladım!")
        print("[2] Ilerleme kaydettim, devam edecek")
        print("[3] Takıldım, yardıma ihtiyacım var")

        choice = input("Secimin: ").strip()
        if choice == "1":
            self.task_manager.complete_task(task["id"])
            self.session_data["completed_tasks"] += 1
            reward = self.motivation.earn_reward("task_complete")
            print(f"\nTebrikler! Görev tamamlandı! {reward}")
        elif choice == "3":
            print("\nIpucu: Görevi daha küçük parçalara bölmeyi dene.")
            self.task_manager.auto_split_task(task["id"])

    def _quick_focus_mode(self):
        """10 dakikalık hızlı odaklanma modu - düsük motivasyon anları icin."""
        self._clear_screen()
        print("\n--- Hızlı Odaklanma Modu (10 dk) ---")
        print("\nSadece 10 dakika! Bunu yapabilirsin.")
        print("Telefonunu kapat, tek bir seye odaklan.\n")

        result = self.pomodoro.start_quick_focus()
        if result["completed"]:
            self.session_data["total_focus_minutes"] += 10
            reward = self.motivation.earn_reward("quick_focus")
            print(f"\n10 dakika tamamlandı! {reward}")
            print("Devam etmek ister misin? Bir pomodoro daha yapabilirsin!")
        else:
            elapsed = result.get("elapsed_minutes", 0)
            self.session_data["total_focus_minutes"] += elapsed
            print(f"\n{elapsed:.0f} dakika odaklandın. Bu da bir basarı!")

    def _manage_tasks(self):
        """Görev yönetim menüsü."""
        while True:
            self._clear_screen()
            print("\n--- Görev Yönetimi ---\n")
            self.task_manager.display_tasks()

            print("\n[1] Yeni görev ekle")
            print("[2] Görevi tamamla")
            print("[3] Görevi küçük adımlara böl")
            print("[4] Öncelik değistir")
            print("[5] Görevi sil")
            print("[6] Ana menüye dön")

            choice = input("\nSecimin: ").strip()
            if choice == "1":
                self._add_task_interactive()
            elif choice == "2":
                self._complete_task_interactive()
            elif choice == "3":
                self._split_task_interactive()
            elif choice == "4":
                self._change_priority_interactive()
            elif choice == "5":
                self._delete_task_interactive()
            elif choice == "6":
                break

    def _add_task_interactive(self):
        print("\n--- Yeni Görev ---")
        title = input("Görev adı: ").strip()
        if not title:
            return

        subject = input("Ders/Konu (opsiyonel): ").strip()

        print("Öncelik: [1] Yüksek  [2] Orta  [3] Düsük")
        p_choice = input("Secimin (varsayılan 2): ").strip()
        priority = {"1": "high", "2": "medium", "3": "low"}.get(p_choice, "medium")

        print("Tahmini süre (dakika, opsiyonel): ")
        est = input().strip()
        estimated_minutes = int(est) if est.isdigit() else None

        task = self.task_manager.add_task(
            title=title,
            subject=subject or None,
            priority=priority,
            estimated_minutes=estimated_minutes,
        )

        # DEHB icin otomatik parcalama önerisi
        if estimated_minutes and estimated_minutes > 30:
            print(f"\nBu görev {estimated_minutes} dakika sürebilir.")
            print("DEHB ipucu: Büyük görevleri küçük adımlara bölmek odaklanmayı kolaylastırır.")
            auto = input("Otomatik olarak böleyim mi? (e/h): ").strip().lower()
            if auto == "e":
                self.task_manager.auto_split_task(task["id"])

        print(f"\nGörev eklendi: {title}")

    def _complete_task_interactive(self):
        pending = self.task_manager.get_pending_tasks()
        if not pending:
            print("Tamamlanacak görev yok.")
            input("Devam etmek icin Enter'a bas...")
            return

        print("\nHangi görevi tamamladın?")
        for i, task in enumerate(pending, 1):
            print(f"[{i}] {task['title']}")

        choice = input("Secimin: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                self.task_manager.complete_task(pending[idx]["id"])
                self.session_data["completed_tasks"] += 1
                reward = self.motivation.earn_reward("task_complete")
                print(f"\nTebrikler! {reward}")
        except ValueError:
            pass
        input("Devam etmek icin Enter'a bas...")

    def _split_task_interactive(self):
        pending = self.task_manager.get_pending_tasks()
        if not pending:
            print("Bölünecek görev yok.")
            input("Devam etmek icin Enter'a bas...")
            return

        print("\nHangi görevi bölmek istiyorsun?")
        for i, task in enumerate(pending, 1):
            print(f"[{i}] {task['title']}")

        choice = input("Secimin: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                self.task_manager.auto_split_task(pending[idx]["id"])
                print("Görev küçük adımlara bölündü!")
        except ValueError:
            pass
        input("Devam etmek icin Enter'a bas...")

    def _change_priority_interactive(self):
        pending = self.task_manager.get_pending_tasks()
        if not pending:
            print("Görev yok.")
            input("Devam etmek icin Enter'a bas...")
            return

        print("\nHangi görevin önceliğini değistirmek istiyorsun?")
        for i, task in enumerate(pending, 1):
            print(f"[{i}] {task['title']} ({task.get('priority', 'medium')})")

        choice = input("Secimin: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                print("[1] Yüksek  [2] Orta  [3] Düsük")
                p = input("Yeni öncelik: ").strip()
                new_priority = {"1": "high", "2": "medium", "3": "low"}.get(p, "medium")
                self.task_manager.update_priority(pending[idx]["id"], new_priority)
                print("Öncelik güncellendi!")
        except ValueError:
            pass
        input("Devam etmek icin Enter'a bas...")

    def _delete_task_interactive(self):
        pending = self.task_manager.get_pending_tasks()
        if not pending:
            print("Silinecek görev yok.")
            input("Devam etmek icin Enter'a bas...")
            return

        print("\nHangi görevi silmek istiyorsun?")
        for i, task in enumerate(pending, 1):
            print(f"[{i}] {task['title']}")

        choice = input("Secimin: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pending):
                confirm = input(f"'{pending[idx]['title']}' silinsin mi? (e/h): ").strip().lower()
                if confirm == "e":
                    self.task_manager.delete_task(pending[idx]["id"])
                    print("Görev silindi.")
        except ValueError:
            pass
        input("Devam etmek icin Enter'a bas...")

    def _view_progress(self):
        """Ilerleme raporlarını gösterir."""
        self._clear_screen()
        print("\n--- Ilerleme Raporları ---\n")

        # Bugünkü oturum
        print(">> Bugünkü Oturum:")
        print(f"   Pomodoro: {self.session_data['completed_pomodoros']}")
        print(f"   Görev: {self.session_data['completed_tasks']}")
        print(f"   Odak süresi: {self.session_data['total_focus_minutes']} dk")
        print(f"   Odak skoru: {self.session_data['focus_score']:.1f}/100")

        # Haftalık özet
        print("\n>> Haftalık Özet:")
        weekly = self.motivation.get_weekly_summary()
        if weekly:
            print(f"   Toplam calısma: {weekly.get('total_minutes', 0)} dk")
            print(f"   Toplam pomodoro: {weekly.get('total_pomodoros', 0)}")
            print(f"   Tamamlanan görev: {weekly.get('tasks_completed', 0)}")
            print(f"   En verimli gün: {weekly.get('best_day', 'Henüz veri yok')}")
            print(f"   Seri: {weekly.get('streak', 0)} gün")
        else:
            print("   Henüz yeterli veri yok.")

        # Level ve ödüller
        print("\n>> Seviye ve Ödüller:")
        level_info = self.motivation.get_level_info()
        print(f"   Seviye: {level_info['level']} - {level_info['title']}")
        print(f"   XP: {level_info['xp']}/{level_info['next_level_xp']}")
        progress_bar = self._make_progress_bar(level_info["xp"], level_info["next_level_xp"])
        print(f"   {progress_bar}")

        badges = self.motivation.get_badges()
        if badges:
            print(f"\n   Rozetler: {', '.join(badges)}")

        input("\nDevam etmek icin Enter'a bas...")

    def _settings(self):
        """Ayarlar menüsü."""
        while True:
            self._clear_screen()
            print("\n--- Ayarlar ---\n")
            print(f"[1] Calısma süresi: {self.config.get('work_duration', 25)} dk")
            print(f"[2] Kısa mola: {self.config.get('short_break', 5)} dk")
            print(f"[3] Uzun mola: {self.config.get('long_break', 15)} dk")
            print(f"[4] Uzun mola aralığı: Her {self.config.get('long_break_interval', 4)} pomodoro")
            print(f"[5] Sesli bildirimler: {'Acık' if self.config.get('sound_enabled', True) else 'Kapalı'}")
            print(f"[6] Otomatik görev parcalama: {'Acık' if self.config.get('auto_split', True) else 'Kapalı'}")
            print("[7] Ana menüye dön")

            choice = input("\nSecimin: ").strip()
            if choice == "7":
                break
            elif choice == "1":
                val = input("Yeni calısma süresi (dk, önerilen: 15-30): ").strip()
                if val.isdigit():
                    self.config.set("work_duration", max(5, min(60, int(val))))
                    self.pomodoro.update_config(self.config)
            elif choice == "2":
                val = input("Yeni kısa mola süresi (dk): ").strip()
                if val.isdigit():
                    self.config.set("short_break", max(1, min(15, int(val))))
            elif choice == "3":
                val = input("Yeni uzun mola süresi (dk): ").strip()
                if val.isdigit():
                    self.config.set("long_break", max(5, min(30, int(val))))
            elif choice == "4":
                val = input("Kac pomodoroda bir uzun mola? ").strip()
                if val.isdigit():
                    self.config.set("long_break_interval", max(2, min(6, int(val))))
            elif choice == "5":
                current = self.config.get("sound_enabled", True)
                self.config.set("sound_enabled", not current)
            elif choice == "6":
                current = self.config.get("auto_split", True)
                self.config.set("auto_split", not current)

    def _calculate_focus_score(self):
        """Odaklanma skoru hesaplar (0-100)."""
        pomodoros = self.session_data["completed_pomodoros"]
        minutes = self.session_data["total_focus_minutes"]

        if pomodoros == 0:
            self.session_data["focus_score"] = 0.0
            return

        expected_minutes = pomodoros * self.config.get("work_duration", 25)
        completion_ratio = minutes / expected_minutes if expected_minutes > 0 else 0
        score = min(100, completion_ratio * 80 + pomodoros * 5)
        self.session_data["focus_score"] = round(score, 1)

    def _show_session_summary(self):
        print("\n" + "=" * 50)
        print("   Oturum Özeti")
        print("=" * 50)
        if self.session_start:
            duration = datetime.now() - self.session_start
            minutes = int(duration.total_seconds() / 60)
            print(f"   Toplam süre: {minutes} dk")
        print(f"   Pomodoro: {self.session_data['completed_pomodoros']}")
        print(f"   Görev: {self.session_data['completed_tasks']}")
        print(f"   Odak süresi: {self.session_data['total_focus_minutes']} dk")
        print(f"   Odak skoru: {self.session_data['focus_score']:.1f}/100")
        print("=" * 50)

    def _save_session(self):
        """Oturum verilerini kaydeder."""
        history_file = self.config.get("history_file", "study_history.json")
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []

        session_record = {
            "date": datetime.now().isoformat(),
            **self.session_data,
        }
        history.append(session_record)

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def _make_progress_bar(self, current, total, width=20):
        if total == 0:
            return "[" + " " * width + "]"
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {current}/{total}"

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")


def main():
    assistant = StudyAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
