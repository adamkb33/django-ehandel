from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin as iema


@admin.register(Kunde)
class Kunde(iema):
    pass
@admin.register(Produkt)
class Produkt(iema):
    pass
@admin.register(Order)
class Order(iema):
    pass
@admin.register(OrderElement)
class OrderElement(iema):
    pass
@admin.register(Leveringsadresse)
class Leveringsadresse(iema):
    pass

