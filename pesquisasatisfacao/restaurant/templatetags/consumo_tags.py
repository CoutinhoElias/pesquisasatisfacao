from django import template

register = template.Library()


@register.filter
def totalizar(contas):
    # print(list(contas))
    valores = [
        c.total
        for c in contas
    ]
    return sum(valores)
