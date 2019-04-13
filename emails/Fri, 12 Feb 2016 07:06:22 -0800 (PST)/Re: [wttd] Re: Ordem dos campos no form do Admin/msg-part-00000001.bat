Felipe aqui não funcionou, eu tenho 4 models diferentes Pessoa(com vários dados), Endereço,E-mail, Telefone.

Qdo eu uso essa sua notação, ele da erro dizendo que a classe pessoa não possui endereço 

Models.py

Class Pessoa():
    Nome
    Cpf
    ...

Class Telefone():
    Telefone

Class endereço ():
     Endereco

Class Email():
     Email

Forms.py
Class Meta():
    field = ('nome', 'cpf', ... , ''telefone', 'endereco', 'e-mail')
    ...

Como solucionaria? Alguma ideia?

-- 
Você está recebendo esta mensagem porque se inscreveu no grupo "Welcome to the Django 2015" dos Grupos do Google.
Para cancelar inscrição nesse grupo e parar de receber e-mails dele, envie um e-mail para wttd-2015+unsubscribe@googlegroups.com.
Para postar neste grupo, envie um e-mail para wttd-2015@googlegroups.com.
Visite este grupo em https://groups.google.com/group/wttd-2015.
Para ver esta discussão na web, acesse https://groups.google.com/d/msgid/wttd-2015/74a5ec85-0fbc-470c-9c64-c89c5a4f0e1e%40googlegroups.com.
Para obter mais opções, acesse https://groups.google.com/d/optout.
