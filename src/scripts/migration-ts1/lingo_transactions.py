#find lingo transactions for 1 item in kart
#usage : sudo -u combo combo-manage tenant_command runscript -d COMMUNE-citoyen.DOMAIN lingo_transactions.py form_slug command_id
#sample : sudo -u combo combo-manage tenant_command runscript -d lalouviere-citoyen.lescommunes.Be lingo_transactions.py commande-de-tickets-repas 84

from combo.apps.lingo.models import BasketItem
import sys
slug = '/{}/{}/'.format(sys.argv[1], sys.argv[2])
BasketItem.objects.filter(source_url__endswith=slug)[0].transaction_set.all()
# [<Transaction: Transaction object>, <Transaction: Transaction object>]
BasketItem.objects.filter(source_url__endswith=slug)[0].transaction_set.all()[0].bank_data

