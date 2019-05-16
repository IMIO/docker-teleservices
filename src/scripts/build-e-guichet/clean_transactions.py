#usage : sudo -u combo combo-manage tenant_command runscript -d COMMUNE.guichet-citoyen.be clean_transactions.py $1
#$1 : all > cancel all transactions for all forms.
#$1 : filter like stationnement/38/ > Remove transaction for *stationnement forms. Demand number 38?

from combo.apps.lingo.models import BasketItem, timezone
import sys

items = None
if len(sys.argv) <= 1 or sys.argv[1] == 'all':
    items = BasketItem.objects.all()
else:
    items = BasketItem.objects.filter(source_url__endswith=sys.argv[1])

for item in items:
    item.cancellation_date = timezone.now()
    item.save()

