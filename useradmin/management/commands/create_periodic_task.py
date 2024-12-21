from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from django.utils import timezone


class Command(BaseCommand):
    help = "Create or update a periodic task for broadcasting analytics"

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        task_name = "Broadcast Analytics"
        task, created = PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                "interval": schedule,
                "task": "useradmin.tasks.broadcast_analytics_task",
                "args": json.dumps([]),
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Periodic task '{task_name}' created.")
            )
        else:
            task.start_time = timezone.now()  
            task.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Periodic task '{task_name}' already exists. Start time updated."
                )
            )
