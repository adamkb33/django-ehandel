from django.db import models
from django.contrib.auth.models import User


class Kunde(models.Model):
    bruker = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    fornavn = models.CharField(max_length=200, null=True, blank=True)
    etternavn = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):

        return str(self.fornavn) + " " + str(self.etternavn)

class Produkt(models.Model):
    navn = models.CharField(max_length=200, null=True, blank=True)
    pris = models.DecimalField(max_digits=9, decimal_places=2)
    bilde = models.ImageField(default='def_bilde.png')
    digital = models.BooleanField(default=False)

    def __str__(self):

        return self.navn


class Order(models.Model):
    kunde = models.ForeignKey(
        Kunde, on_delete=models.SET_NULL, null=True, blank=True)
    ordrenr = models.CharField(max_length=200, null=True, blank=True)
    opprettet = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):

        order = str(self.ordrenr)
        kunde = str(self.kunde)

        if kunde == 'None':
            kunde = 'Gjest'

        if order == 'None':
            return 'Ikke godkjent, ' + kunde
        else:
            return order + ", " + kunde
    
    @property
    def frakt(self):
        frakt = False
        elementer = self.orderelement_set.all()
        for element in elementer:
            if element.produkt.digital == False:
                frakt = True
        return frakt

    @property
    def total_pris(self):
        orderelementer = self.orderelement_set.all()
        total_sum = sum([i.total_pris for i in orderelementer])

        return total_sum

    @property
    def total_antall(self):
        orderelementer = self.orderelement_set.all()
        total_antall = sum([i.antall for i in orderelementer])

        return total_antall

class OrderElement(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    antall = models.IntegerField(default=0, null=True, blank=True)
    lagt_til = models.DateTimeField(auto_now=True)

    def __str__(self):

        kunde = str(self.order.kunde)
        ordrenr = str(self.order.ordrenr)

        if kunde == 'None':
            kunde = 'Gjest Bruker'

        if ordrenr == 'None':
            ordrenr = 'Ikke godkjent'

        return  ordrenr + ", " + kunde 

    @property
    def total_pris(self):

        return self.antall * self.produkt.pris

class Leveringsadresse(models.Model):
    kunde = models.ForeignKey(Kunde, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    by = models.CharField(max_length=200, null=True, blank=True)
    fylke = models.CharField(max_length=200, null=True, blank=True)
    postnr = models.CharField(max_length=200, null=True, blank=True)
    opprettet = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.fylke + ', ' + self.postnr + ', ' + self.by +  ', ' + self.adresse

        