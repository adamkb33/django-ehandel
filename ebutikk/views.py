from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import *
from .utils import *
from .forms import *

import json
import datetime


def logginn(request):

    if request.method == 'POST':

        brukernavn = request.POST.get('brukernavn')
        passord = request.POST.get('passord')

        bruker = authenticate(request, username=brukernavn, password=passord)

        if bruker is not None:
            login(request, bruker)
            return redirect('butikk')

    context = {}

    return render(request, 'ebutikk/autentisering/logginn.html', context)


def registrerKunde(request):

    form = lageBruker(request.POST)

    if request.method == 'POST':

        if form.is_valid():

            bruker = form.save()
            fornavn = request.POST['first_name']
            etternavn = request.POST['last_name']
            email = request.POST['email']

            kunde = Kunde.objects.create(
                bruker=bruker,
                fornavn=fornavn,
                etternavn=etternavn,
                email=email,
            )
            kunde.save()

            bruker = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            if bruker is not None:
                login(request, bruker)

            return redirect('butikk')

    context = {'form': form}

    return render(request, 'ebutikk/autentisering/registrering.html', context)

def loggut(request):

    logout(request)

    return redirect('butikk')

def butikk(request):

    handel = orderFunksjon(request)
    handlevogn = handel['handlevogn']

    produkter = Produkt.objects.all()

    context = {'produkter': produkter, 'handlevogn': handlevogn}

    return render(request, 'ebutikk/nettbutikk/butikk.html', context)


def handlevogn(request):

    handel = orderFunksjon(request)
    order = handel['order']
    elementer = handel['elementer']
    handlevogn = handel['handlevogn']

    context = {'order': order, 'elementer': elementer,
               'handlevogn': handlevogn}

    return render(request, 'ebutikk/nettbutikk/handlevogn.html', context)


def utsjekk(request):

    handel = orderFunksjon(request)
    order = handel['order']
    elementer = handel['elementer']
    handlevogn = handel['handlevogn']

    context = {'order': order, 'elementer': elementer,
               'handlevogn': handlevogn}

    return render(request, 'ebutikk/nettbutikk/utsjekk.html', context)


def oppdaterElementer(request):

    data = json.loads(request.body)
    produktId = data['produktId']
    handling = data['handling']

    kunde = request.user.kunde
    produkt = Produkt.objects.get(id=produktId)
    order, created = Order.objects.get_or_create(kunde=kunde, status=False)

    orderelement, created = OrderElement.objects.get_or_create(
        order=order, produkt=produkt)

    if handling == 'adder':
        orderelement.antall = (orderelement.antall + 1)

    elif handling == 'trekk':
        orderelement.antall = (orderelement.antall - 1)
        if orderelement.antall <= 0:
            orderelement.antall = 1

    orderelement.save()

    if handling == 'slett':
        orderelement.delete()

    print('id2:', produktId, 'handling:', handling)

    return JsonResponse('Data er behandlet', safe=False)


def behandlingAvOrder(request):
    orderInfo = json.loads(request.body)
    order_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        kunde = request.user.kunde
        order, created = Order.objects.get_or_create(kunde=kunde, status=False)
    else:
        kunde, order = gjestOrder(request, orderInfo)

    belop = float(orderInfo['Kunde']['Belop'])
    order.ordrenr = order_id

    if belop == order.total_pris:
        order.status = True

    print(order)
    print(kunde)
    order.save()

    if order.frakt == True:
        Leveringsadresse.objects.create(
            kunde=kunde,
            order=order,
            adresse=orderInfo['Frakt-Informasjon']['Adresse'],
            by=orderInfo['Frakt-Informasjon']['By'],
            fylke=orderInfo['Frakt-Informasjon']['Fylke'],
            postnr=orderInfo['Frakt-Informasjon']['Postnr'],
        )

    return JsonResponse('Order godkjent', safe=False)
