# sudo -u combo combo-manage tenant_command runscript -d local.example.net lingo_create_regie.py
import eopayment
import sys
from combo.apps.lingo.models import Regie

service_opt = '''
              {"platform": "test",
               "secret_key": "002001000000001_KEY1",
               "merchant_id": "002001000000001",
               "key_version": "1"
              }'''

Regie(label='Atos test',
      slug='atos_test',
      description='Atos test',
      service_options=service_opt,
      text_on_success="Votre paiement a été pris en compte. Si votre demande est validée par nos services, vous recevrez très prochainement votre document par voie postale. Si votre demande n'est pas valide, vous serez prévenu par e-mail et remboursé de la somme perçue dans les meilleurs délais",
      service=eopayment.SIPS2,
      is_default=True).save()


#      extra_fees_ws_url="https://{}-passerelle.{}/extra-fees/calcul-des-frais-de-port/compute".format(sys.argv[1],sys.argv[2]),
