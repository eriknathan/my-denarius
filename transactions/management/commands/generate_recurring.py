import calendar
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Gera transações recorrentes para o mês atual.'

    def handle(self, *args, **options):
        today = timezone.localdate()
        templates = Transaction.objects.filter(
            is_recurring=True,
            recurrence_day__isnull=False,
        ).select_related('account', 'category')

        created = 0
        for tpl in templates:
            day = tpl.recurrence_day
            last_day = calendar.monthrange(today.year, today.month)[1]
            effective_day = min(day, last_day)
            target_date = datetime.date(today.year, today.month, effective_day)

            already_exists = Transaction.objects.filter(
                user=tpl.user,
                description=tpl.description,
                account=tpl.account,
                category=tpl.category,
                transaction_type=tpl.transaction_type,
                date=target_date,
                is_recurring=False,
            ).exists()

            if not already_exists:
                Transaction.objects.create(
                    user=tpl.user,
                    account=tpl.account,
                    category=tpl.category,
                    description=tpl.description,
                    amount=tpl.amount,
                    transaction_type=tpl.transaction_type,
                    date=target_date,
                    notes=tpl.notes,
                    is_recurring=False,
                )
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'{created} transação(ões) recorrente(s) gerada(s).')
        )
