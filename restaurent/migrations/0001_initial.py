# Generated by Django 4.2.5 on 2024-03-21 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=256)),
                ('email_address', models.EmailField(max_length=100)),
                ('phone_number', models.CharField(max_length=50)),
                ('photo', models.FileField(blank=True, null=True, upload_to='images/')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Admin Profile',
                'verbose_name_plural': 'Admin Profile',
            },
        ),
        migrations.CreateModel(
            name='AllTables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=100)),
                ('no_of_seats', models.IntegerField()),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
                ('status', models.CharField(blank=True, choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Cancelled', 'Cancelled')], max_length=255, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Add The Table',
                'verbose_name_plural': 'Add The Tables',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=50, null=True)),
                ('category_desc', models.CharField(blank=True, max_length=2000, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('status', models.IntegerField(default=0)),
                ('display_order', models.IntegerField(default=0)),
                ('show_on_our_menu', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
        migrations.CreateModel(
            name='cms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_title', models.CharField(blank=True, max_length=50, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('long_description', models.TextField(blank=True, null=True)),
                ('banner_image', models.FileField(null=True, upload_to='images/')),
                ('banner_text1', models.TextField(blank=True, null=True)),
                ('banner_text2', models.TextField(blank=True, null=True)),
                ('banner_text3', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cms',
                'verbose_name_plural': 'Cms',
            },
        ),
        migrations.CreateModel(
            name='contactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(blank=True, max_length=2000, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('reason_contact', models.CharField(blank=True, max_length=2000, null=True)),
                ('subscribe', models.CharField(blank=True, max_length=50, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contact Us',
            },
        ),
        migrations.CreateModel(
            name='gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_title', models.CharField(blank=True, max_length=50, null=True)),
                ('item_desc', models.CharField(blank=True, max_length=2000, null=True)),
                ('thumb_image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('status', models.IntegerField(default=0)),
                ('display_order', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'gallerys',
            },
        ),
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(blank=True, max_length=50, null=True)),
                ('item_desc', models.CharField(blank=True, max_length=2000, null=True)),
                ('price', models.FloatField(blank=True, max_length=10, null=True)),
                ('image', models.FileField(null=True, upload_to='images/')),
                ('popular', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('display_order', models.IntegerField(default=0)),
                ('display_order_for_special_item', models.IntegerField(default=0)),
                ('status_for_special_item', models.BooleanField(default=False)),
                ('discount_description_for_special_item', models.TextField(blank=True, null=True)),
                ('description_for_special_item', models.TextField(blank=True, null=True)),
                ('selection_type', models.CharField(choices=[('Single', 'Single'), ('Multiple', 'Multiple')], max_length=100, null=True)),
                ('display_order_for_our_menu', models.IntegerField(default=0)),
                ('status_for_our_menu', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurent.category')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='specialoffers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, max_length=10, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/')),
                ('discount', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('display_order', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Special Offer',
                'verbose_name_plural': 'Special Offers',
            },
        ),
        migrations.CreateModel(
            name='SubItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_item_title', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0.0, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurent.items')),
            ],
            options={
                'verbose_name': 'Sub Item',
                'verbose_name_plural': 'Sub Items',
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('surname', models.CharField(max_length=256)),
                ('street_number', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=56)),
                ('email', models.CharField(max_length=256)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='restaurent.items')),
                ('subitem_id', models.ManyToManyField(related_name='order_subitems', to='restaurent.subitems')),
            ],
            options={
                'verbose_name': 'Order Detail',
                'verbose_name_plural': 'Order Details',
            },
        ),
        migrations.CreateModel(
            name='BookTheTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=100)),
                ('total_members', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
                ('timings', models.TimeField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('table_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurent.alltables')),
            ],
            options={
                'verbose_name': 'Table Booking Details',
                'verbose_name_plural': 'Table Booking Details',
            },
        ),
    ]
