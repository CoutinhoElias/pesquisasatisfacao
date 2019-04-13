Boa noite. Este final de semana empaquei brincando um pouco com staticfiles. A intenção é que no bucket eu faça o upload dos arquivos estáticos para uma pasta static porque o padrão do "storages.backends.s3boto.S3BotoStorage" não faz. Então tenho que importar o S3BotoStorage. E é quando me retorna um erro. Segue o que fiz.

Instalei pelo pip o django.storages.redux e o boto

Adicionei:

INSTALLED_APPS = [
    ...,
    'storages',
]

e no final do arquivo:
...
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
...

Até aqui roda bacaninha, mas quando adiciono,

from storages.backends.s3boto import S3BotoStorage

,recebo um erro no collect static:

KeyError: 'collectstatic'
...
raise ImproperlyConfigured("The SECRET_KEY setting must not be empty.")
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.

Alguém tem alguma ideia? Uma outra maneira de fazer a parada?
Valeu

-- 
Você está recebendo esta mensagem porque se inscreveu no grupo "Welcome to the Django 2015" dos Grupos do Google.
Para cancelar inscrição nesse grupo e parar de receber e-mails dele, envie um e-mail para wttd-2015+unsubscribe@googlegroups.com.
Para postar neste grupo, envie um e-mail para wttd-2015@googlegroups.com.
Visite este grupo em https://groups.google.com/group/wttd-2015.
Para ver esta discussão na web, acesse https://groups.google.com/d/msgid/wttd-2015/95640c16-e2c0-475f-ad2d-f9ae7489c386%40googlegroups.com.
Para obter mais opções, acesse https://groups.google.com/d/optout.
