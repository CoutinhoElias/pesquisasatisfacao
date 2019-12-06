from django import template

register = template.Library()


@register.filter
def totalizar(contas):
    # print(list(contas))
    valores = [
        c.valor_vendido
        if c.operacao == 'd'
        else c.valor_vendido * -1
        for c in contas
    ]
    return sum(valores)
