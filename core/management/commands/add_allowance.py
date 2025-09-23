from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import F
from core.models import UserProfile

class Command(BaseCommand):
    help = "全ユーザーの available_amount を指定額だけ加算します（1以上の整数のみ）。"

    def add_arguments(self, parser):
        parser.add_argument(
            "--amount",
            required=True,
            type=int,
            help="加算する金額（1以上の整数）",
        )

    def handle(self, *args, **options):
        amount = options["amount"]
        if amount is None or amount < 1:
            raise CommandError("amount は 1 以上の整数で指定してください。例: --amount 100")

        with transaction.atomic():
            updated = UserProfile.objects.update(
                available_amount=F("available_amount") + amount
            )

        self.stdout.write(self.style.SUCCESS(
            f"OK: {updated} 件のユーザープロファイルに {amount} を加算しました。"
        ))
