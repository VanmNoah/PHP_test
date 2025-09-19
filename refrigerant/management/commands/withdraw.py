from django.core.management.base import BaseCommand
from django.db.models import F
from ...models import Vessel
import threading

class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        vessel = Vessel.objects.create(name="Test Vessel", content=50.0)
        vessel_id = vessel.id
        self.stdout.write("Simulating condition...")
        self.run_simulation(vessel_id)

    def run_simulation(self, vessel_id: int):
        barrier = threading.Barrier(2)

        def user1():
            barrier.wait()
            updated = Vessel.objects.filter(
                id=vessel_id, content__gte=10
            ).update(content=F('content') - 10)
            if not updated:
                self.stdout.write(self.style.WARNING(
                    "⚠️ Het vat is leeg of heeft onvoldoende inhoud voor 10 kg."
                ))

        def user2():
            barrier.wait()
            updated = Vessel.objects.filter(
                id=vessel_id, content__gte=10
            ).update(content=F('content') - 10)
            if not updated:
                self.stdout.write(self.style.WARNING(
                    "⚠️ Het vat is leeg of heeft onvoldoende inhoud voor 10 kg."
                ))

        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=vessel_id)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
