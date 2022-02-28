import json
from .models import *


def gjestBruker(request):

    try:
        handlevognCookie = json.loads(request.COOKIES['handlevogn'])
    except:
        handlevognCookie = {}

    elementer = []
    order = {'total_pris': 0, 'total_antall': 0, 'frakt': False}
    handlevogn = order['total_antall']

    for i in handlevognCookie:
        try:
            handlevogn += handlevognCookie[i]['antall']

            produkt = Produkt.objects.get(id=i)
            total_pris = (produkt.pris * handlevognCookie[i]['antall'])

            order['total_pris'] += total_pris
            order['total_antall'] = handlevogn

            element = {
                'produkt': {
                    'id': produkt.id,
                    'navn': produkt.navn,
                    'pris': produkt.pris,
                    'bilde': produkt.bilde
                },
                'antall': handlevognCookie[i]['antall'],
                'total_pris': total_pris
            }
            elementer.append(element)

            if produkt.digital == False:
                order['frakt'] = True
        except:
            pass

    return {'order': order, 'elementer': elementer, 'handlevogn': handlevogn}


def orderFunksjon(request):

    if request.user.is_authenticated:
        kunde = request.user.kunde
        order, created = Order.objects.get_or_create(kunde=kunde, status=False)
        elementer = order.orderelement_set.all()
        print(elementer)
        handlevogn = order.total_antall
    else:
        gjest = gjestBruker(request)
        order = gjest['order']
        elementer = gjest['elementer']
        handlevogn = gjest['handlevogn']

    return {'order': order, 'elementer': elementer, 'handlevogn': handlevogn}


def gjestOrder(request, orderInfo):

    print('Bruker ikke innlogget')
    print('Cookie', request.COOKIES)
    print(orderInfo)

    navn = orderInfo['Kunde']['Navn']
    etternavn = orderInfo['Kunde']['Etternavn']
    email = orderInfo['Kunde']['Email']

    COOKIE = gjestBruker(request)
    produkter = COOKIE['elementer']
    
    print('COOKIE', COOKIE)

    kunde, created = Kunde.objects.get_or_create(
        email=email
    )

    kunde.fornavn = navn
    kunde.etternavn = etternavn
    kunde.save()

    order = Order.objects.create(
        kunde=kunde,
        status=False
    )

    for i in produkter:
        produkt = Produkt.objects.get(id=i['produkt']['id'])

        orderElement = OrderElement.objects.create(
            produkt=produkt,
            order=order,
            antall=i['antall'],
        )

    return kunde, order
