"""
Yapılandırma Modülü
====================
Uygulama ayarlarını yönetir.
Varsayılan degerler DEHB icin optimize edilmistir.
"""

import json
import os


DEFAULT_CONFIG = {
    # Pomodoro ayarları
    "work_duration": 25,         # Calısma süresi (dk) - DEHB icin 15-25 dk ideal
    "short_break": 5,            # Kısa mola (dk)
    "long_break": 15,            # Uzun mola (dk)
    "long_break_interval": 4,    # Kac pomodoroda bir uzun mola

    # Bildirim ayarları
    "sound_enabled": True,       # Sesli bildirimler
    "encouragement_enabled": True,  # Motivasyon mesajları

    # Görev ayarları
    "auto_split": True,          # Otomatik görev parcalama
    "max_task_minutes": 30,      # Bu süreyi asan görevler bölünür

    # Dosya yolları
    "tasks_file": "tasks.json",
    "history_file": "study_history.json",
    "motivation_file": "motivation_data.json",
}


class Config:
    """Uygulama yapılandırma yöneticisi."""

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.settings = dict(DEFAULT_CONFIG)
        self._load()

    def _load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    self.settings.update(user_config)
            except (json.JSONDecodeError, IOError):
                pass  # Varsayılan ayarları kullan

    def save(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def reset(self):
        self.settings = dict(DEFAULT_CONFIG)
        self.save()
