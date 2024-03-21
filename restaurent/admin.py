from django.contrib import admin

from .models import (gallery, items, 
                     specialoffers, 
                     cms, contactUs,
                     AllTables, BookTheTable,category,
                     items,SubItems,AdminProfile,OrderDetails)



admin.site.register(gallery)

admin.site.register(items)

admin.site.register(specialoffers)



admin.site.register(cms)

admin.site.register(contactUs)



admin.site.register(AllTables)

admin.site.register(BookTheTable)



admin.site.register(category)

admin.site.register(SubItems)

admin.site.register(AdminProfile)



admin.site.register(OrderDetails)
