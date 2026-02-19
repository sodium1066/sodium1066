"""
Görev Yönetimi Modülü
======================
DEHB icin optimize edilmis görev yönetim sistemi.
- Büyük görevleri otomatik olarak küçük adımlara böler
- Öncelik bazlı sıralama
- Tahmini süre takibi
- Alt görev (subtask) destegi
"""

import json
import os
import uuid
from datetime import datetime


class TaskManager:
    """DEHB dostu görev yönetim sistemi."""

    def __init__(self, config):
        self.config = config
        self.tasks_file = config.get("tasks_file", "tasks.json")
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_tasks(self):
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add_task(self, title, subject=None, priority="medium", estimated_minutes=None):
        """Yeni görev ekler."""
        task = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "subject": subject,
            "priority": priority,
            "estimated_minutes": estimated_minutes,
            "status": "pending",
            "subtasks": [],
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def complete_task(self, task_id):
        """Görevi tamamlanmıs olarak isaretler."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                # Alt görevleri de tamamla
                for sub in task.get("subtasks", []):
                    sub["done"] = True
                self._save_tasks()
                return True
        return False

    def delete_task(self, task_id):
        """Görevi siler."""
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self._save_tasks()

    def update_priority(self, task_id, new_priority):
        """Görevin önceliğini günceller."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["priority"] = new_priority
                self._save_tasks()
                return True
        return False

    def get_pending_tasks(self):
        """Bekleyen görevleri öncelik sırasına göre döndürür."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending = [t for t in self.tasks if t["status"] == "pending"]
        pending.sort(key=lambda t: priority_order.get(t.get("priority", "medium"), 1))
        return pending

    def get_completed_tasks(self):
        """Tamamlanan görevleri döndürür."""
        return [t for t in self.tasks if t["status"] == "completed"]

    def auto_split_task(self, task_id):
        """
        Büyük bir görevi otomatik olarak küçük adımlara böler.
        DEHB icin kritik: Büyük görevler bunaltıcı olabilir,
        küçük adımlar odaklanmayı kolaylastırır.
        """
        for task in self.tasks:
            if task["id"] == task_id:
                estimated = task.get("estimated_minutes")
                title = task["title"]

                if task.get("subtasks"):
                    # Zaten bölünmüs, mevcut alt görevleri göster
                    return task["subtasks"]

                subtasks = self._generate_subtasks(title, estimated)
                task["subtasks"] = subtasks
                self._save_tasks()

                print(f"\n'{title}' görevi su adımlara bölündü:")
                for i, sub in enumerate(subtasks, 1):
                    print(f"  {i}. {sub['title']} (~{sub.get('estimated_minutes', '?')} dk)")

                return subtasks
        return []

    def _generate_subtasks(self, title, estimated_minutes):
        """
        Görev basığına göre alt adımlar üretir.
        Kural: Her alt görev en fazla 15-20 dakika olmalı (DEHB dostu).
        """
        subtasks = []

        if estimated_minutes and estimated_minutes > 30:
            # Tahmini süreye göre böl
            chunk_size = 15  # DEHB icin ideal: 15 dakikalık parcalar
            num_chunks = max(2, estimated_minutes // chunk_size)

            subtasks.append({
                "title": f"{title} - Hazırlık (materyal topla)",
                "estimated_minutes": 5,
                "done": False,
            })

            for i in range(1, num_chunks):
                subtasks.append({
                    "title": f"{title} - Bölüm {i}",
                    "estimated_minutes": chunk_size,
                    "done": False,
                })

            subtasks.append({
                "title": f"{title} - Gözden gecirme ve tekrar",
                "estimated_minutes": 10,
                "done": False,
            })
        else:
            # Genel parcalama sablonu
            subtasks = [
                {
                    "title": f"{title} - Konuyu gözden gecir",
                    "estimated_minutes": 10,
                    "done": False,
                },
                {
                    "title": f"{title} - Ana calısma",
                    "estimated_minutes": 15,
                    "done": False,
                },
                {
                    "title": f"{title} - Pratik / Alıstırma",
                    "estimated_minutes": 10,
                    "done": False,
                },
                {
                    "title": f"{title} - Kısa tekrar",
                    "estimated_minutes": 5,
                    "done": False,
                },
            ]

        return subtasks

    def complete_subtask(self, task_id, subtask_index):
        """Alt görevi tamamlanmıs olarak isaretler."""
        for task in self.tasks:
            if task["id"] == task_id:
                subtasks = task.get("subtasks", [])
                if 0 <= subtask_index < len(subtasks):
                    subtasks[subtask_index]["done"] = True
                    self._save_tasks()

                    # Tüm alt görevler tamam mı kontrol et
                    if all(s["done"] for s in subtasks):
                        print("\nTüm alt adımlar tamamlandı! Görev bitirilebilir.")
                    return True
        return False

    def display_tasks(self):
        """Görevleri ekranda gösterir."""
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()

        if not pending and not completed:
            print("Henüz görev eklenmemis.")
            print("Ipucu: Görev ekleyerek calısmanı planlayabilirsin!")
            return

        if pending:
            print("Bekleyen Görevler:")
            print("-" * 40)
            for task in pending:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    task.get("priority", "medium"), "⚪"
                )
                est = f" (~{task['estimated_minutes']} dk)" if task.get("estimated_minutes") else ""
                subject = f" [{task['subject']}]" if task.get("subject") else ""
                print(f"  {priority_icon} {task['title']}{subject}{est}")

                # Alt görevleri göster
                for sub in task.get("subtasks", []):
                    status = "✓" if sub.get("done") else " "
                    print(f"      [{status}] {sub['title']}")

        if completed:
            print(f"\nTamamlanan ({len(completed)} görev):")
            print("-" * 40)
            for task in completed[-5:]:  # Son 5 tamamlananı göster
                print(f"  ✓ {task['title']}")

    def get_stats(self):
        """Görev istatistiklerini döndürür."""
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()
        return {
            "total": len(self.tasks),
            "pending": len(pending),
            "completed": len(completed),
            "high_priority": len([t for t in pending if t.get("priority") == "high"]),
        }
