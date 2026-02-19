"""
Pomodoro Zamanlayıcı Modülü
============================
DEHB icin optimize edilmis Pomodoro zamanlayıcı.
- Kısa calısma döngüleri (varsayılan 25dk, 15dk'ya kadar düsürülebilir)
- Görsel geri sayım
- Mola hatırlatmaları
- Hızlı odaklanma modu (10dk)
"""

import time
import sys
import os


class PomodoroTimer:
    """DEHB dostu Pomodoro zamanlayıcı."""

    def __init__(self, config):
        self.config = config
        self.work_duration = config.get("work_duration", 25)
        self.short_break = config.get("short_break", 5)
        self.long_break = config.get("long_break", 15)
        self.sound_enabled = config.get("sound_enabled", True)

    def update_config(self, config):
        self.config = config
        self.work_duration = config.get("work_duration", 25)
        self.short_break = config.get("short_break", 5)
        self.long_break = config.get("long_break", 15)
        self.sound_enabled = config.get("sound_enabled", True)

    def start_focus(self):
        """Ana calısma zamanlayıcısını baslatır."""
        duration = self.work_duration * 60
        print(f"\n⏱  Calısma basladı! ({self.work_duration} dakika)")
        print("   Odaklan, yapabilirsin!")
        print("   Iptal icin Ctrl+C\n")

        result = self._run_timer(duration, "Calısma")
        return result

    def start_short_break(self):
        """Kısa mola zamanlayıcısı."""
        duration = self.short_break * 60
        print(f"\n☕ Kısa mola! ({self.short_break} dakika)")
        print("   Kalk, gerin, su ic!\n")
        self._run_timer(duration, "Mola")
        self._play_sound("break_end")
        print("\nMola bitti! Hazır mısın?")

    def start_long_break(self):
        """Uzun mola zamanlayıcısı."""
        duration = self.long_break * 60
        print(f"\n🌿 Uzun mola! ({self.long_break} dakika)")
        print("   Yürüyüs yap, atıstırmalık al, dinlen.\n")
        self._run_timer(duration, "Uzun Mola")
        self._play_sound("break_end")
        print("\nUzun mola bitti! Enerjin yenilendi.")

    def start_quick_focus(self):
        """10 dakikalık hızlı odaklanma modu."""
        duration = 10 * 60
        print("\n⚡ Hızlı Odaklanma! (10 dakika)")
        print("   Sadece 10 dakika. Basla!\n")
        result = self._run_timer(duration, "Hızlı Odak")
        return result

    def _run_timer(self, total_seconds, label):
        """Zamanlayıcıyı calistırır ve ilerlemeyi gösterir."""
        start_time = time.time()
        elapsed = 0

        try:
            while elapsed < total_seconds:
                remaining = total_seconds - elapsed
                mins = int(remaining // 60)
                secs = int(remaining % 60)

                # Ilerleme cubugu
                progress = elapsed / total_seconds
                bar_width = 30
                filled = int(bar_width * progress)
                bar = "█" * filled + "░" * (bar_width - filled)
                percent = int(progress * 100)

                sys.stdout.write(
                    f"\r   [{bar}] {percent:3d}% | {mins:02d}:{secs:02d} kaldı | {label}"
                )
                sys.stdout.flush()

                # DEHB motivasyon mesajları - belirli aralıklarda
                self._show_encouragement(elapsed, total_seconds)

                time.sleep(1)
                elapsed = time.time() - start_time

            sys.stdout.write(
                f"\r   [{'█' * 30}] 100% | 00:00 kaldı | {label} ✓   \n"
            )
            sys.stdout.flush()

            self._play_sound("timer_complete")

            return {
                "completed": True,
                "duration_minutes": round(total_seconds / 60, 1),
                "elapsed_minutes": round(elapsed / 60, 1),
            }

        except KeyboardInterrupt:
            elapsed_final = time.time() - start_time
            sys.stdout.write("\n")
            return {
                "completed": False,
                "duration_minutes": round(total_seconds / 60, 1),
                "elapsed_minutes": round(elapsed_final / 60, 1),
            }

    def _show_encouragement(self, elapsed, total):
        """Belirli aralıklarla DEHB dostu motivasyon mesajları gösterir."""
        progress = elapsed / total if total > 0 else 0

        # Sadece belirli yüzdelerde mesaj göster (yüzde noktalarında)
        messages = {
            0.25: "\n   💪 Ceyrek yol tamam! Devam et!",
            0.50: "\n   🎯 Yarı yoldasın! Harikasın!",
            0.75: "\n   🔥 Neredeyse bitti! Son hamle!",
            0.90: "\n   ⭐ Son düzlük! Az kaldı!",
        }

        # Sadece tam yüzde noktalarında tetikle (1 saniyelik pencere)
        for threshold, message in messages.items():
            target_second = int(total * threshold)
            if abs(elapsed - target_second) < 1:
                print(message)
                break

    def _play_sound(self, sound_type):
        """Sesli bildirim calar."""
        if not self.sound_enabled:
            return

        try:
            if sys.platform == "darwin":
                # macOS
                if sound_type == "timer_complete":
                    os.system('afplay /System/Library/Sounds/Glass.aiff 2>/dev/null &')
                elif sound_type == "break_end":
                    os.system('afplay /System/Library/Sounds/Ping.aiff 2>/dev/null &')
            elif sys.platform == "linux":
                # Linux - terminal bell
                sys.stdout.write("\a")
                sys.stdout.flush()
            elif sys.platform == "win32":
                import winsound
                if sound_type == "timer_complete":
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                elif sound_type == "break_end":
                    winsound.MessageBeep(winsound.MB_OK)
        except Exception:
            pass  # Ses calamazsa sessizce devam et
