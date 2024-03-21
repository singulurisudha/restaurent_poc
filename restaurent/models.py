from django.db import models

# Create your models here.


class contactUs(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    message = models.CharField(max_length=2000, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    reason_contact = models.CharField(max_length=2000, null=True, blank=True)
    subscribe = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = "Contact"
            verbose_name_plural = "Contact Us"

    def __str__(self):
        return str(self.name) 

class gallery(models.Model):
    image_title = models.CharField(max_length=50, null=True, blank=True)
    item_desc = models.CharField(max_length=2000, null=True, blank=True)
    thumb_image = models.FileField(upload_to='images/', null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    status = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
            verbose_name = "gallery"
            verbose_name_plural = "gallerys"

    def __str__(self):
        return str(self.image_title)  
    
class cms(models.Model):
    page_title = models.CharField(max_length=50, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    banner_image = models.FileField(upload_to='images/', null=True)
    banner_text1 = models.TextField(null=True, blank=True)
    banner_text2 = models.TextField(null=True, blank=True)
    banner_text3 = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
            verbose_name = "Cms"
            verbose_name_plural = "Cms"

    def __str__(self):
        return str(self.page_title) 
    

 

class specialoffers(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(max_length=10, null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    discount = models.TextField( null=True, blank=True)
    status = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
          
    class Meta:
        verbose_name = "Special Offer"
        verbose_name_plural = "Special Offers"
    
    def __str__(self):
        return str(self.title) 
    
class category(models.Model):
    category_name = models.CharField(max_length=50, null=True, blank=True)
    category_desc = models.CharField(max_length=2000, null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True, blank=True)
    status = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    show_on_our_menu = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categorys"
    
    def __str__(self):
        return str(self.category_name)    
        
class items(models.Model):
    SELECTION_TYPE = (
        ("Single","Single"),
        ("Multiple","Multiple")
    )
    
    category_id = models.ForeignKey(category, on_delete=models.CASCADE ,null=True, blank=True)
    item_name = models.CharField(max_length=50, null=True, blank=True)
    item_desc = models.CharField(max_length=2000, null=True, blank=True)
    price = models.FloatField(max_length=10, null=True, blank=True)
    image = models.FileField(upload_to='images/', null=True)     
    popular = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    display_order = models.IntegerField(default=0)
    
    display_order_for_special_item = models.IntegerField(default=0)
    status_for_special_item = models.BooleanField(default=False)
    discount_description_for_special_item  = models.TextField( null=True, blank=True)
    description_for_special_item = models.TextField(null=True, blank=True)
    selection_type = models.CharField(max_length = 100,choices=SELECTION_TYPE,null = True)
    
    display_order_for_our_menu = models.IntegerField(default=0)
    status_for_our_menu = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return str(self.item_name)  
    
class SubItems(models.Model):
    SELECTION_TYPE = (
        ("Single","Single"),
        ("Multiple","Multiple")
    )

    item_id = models.ForeignKey(items, on_delete=models.CASCADE, null=True, blank=True)
    sub_item_title = models.CharField(max_length = 100)
    price = models.FloatField(default=0.0,null=True)
    short_description = models.TextField(null=True, blank=True)
    status = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = "Sub Item"
        verbose_name_plural = "Sub Items"

    def __str__(self):
        return str(self.sub_item_title)  


class OrderDetails(models.Model):
    item_id = models.ForeignKey(items, on_delete=models.CASCADE,null=True,related_name='order_items')
    subitem_id = models.ManyToManyField(SubItems,related_name='order_subitems')
    total_price = models.CharField(max_length = 256)
    name = models.CharField(max_length = 256)
    surname = models.CharField(max_length = 256)
    street_number = models.CharField(max_length = 256)
    city = models.CharField(max_length = 256)
    phone_number = models.CharField(max_length = 56)
    email = models.CharField(max_length = 256)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name = "Order Detail"
        verbose_name_plural = "Order Details"

        

class AllTables(models.Model):
    STATUS_CHOICES = (
        ("Available","Available"),
        ("Booked","Booked"),
        ("Cancelled","Cancelled")
    )

    table_name = models.CharField(max_length = 100)
    no_of_seats = models.IntegerField()
    from_time = models.TimeField()
    to_time = models.TimeField()
    status = models.CharField(choices=STATUS_CHOICES,max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Add The Table"
        verbose_name_plural = "Add The Tables"

    def __str__(self):
        return str(self.table_name)  


class BookTheTable(models.Model):
    table_id = models.ForeignKey(AllTables, on_delete=models.SET_NULL ,null=True, blank=True)
    name = models.CharField(max_length = 256)
    phone_number = models.CharField(max_length = 50)
    email_address = models.EmailField(max_length=100)
    total_members = models.IntegerField()
    date = models.DateField(null=True,blank=True)
    timings = models.TimeField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Table Booking Details"
        verbose_name_plural = "Table Booking Details"

    def __str__(self):
        return str(self.name) 
    
class AdminProfile(models.Model):
    full_name = models.CharField(max_length = 256)
    email_address = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length = 50)
    photo = models.FileField(upload_to='images/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profile"

    def __str__(self):
        return str(self.full_name) 
    

    
