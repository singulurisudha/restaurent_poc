from rest_framework import serializers
import re
from datetime import timedelta
from .models import (
    category,
    items,
    SubItems,
    OrderDetails,
    cms,
    AdminProfile,
    contactUs, 
    gallery,
    specialoffers,
    AllTables
    )

from django.db.models import Q

from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data.get('is_staff'):
            superuser = User.objects.create_superuser(**validated_data)
            return superuser
        else:
            user = User.objects.create_user(**validated_data)
            return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ForgetPasswordUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = specialoffers
        fields = ['id', 'title', 'description', 'price', 'image', 
                  'discount', 'status', 'display_order', 'is_deleted', 'created_at', 'updated_at']
        

    def validate(self, data):
        # Validate the 'status' field
        status = data.get('status')
        if status not in [0, 1]:
            raise serializers.ValidationError({'status': 'Status should be either 0 or 1.'})

        # Validate the 'title' field
        title = data.get('title')
        if specialoffers.objects.filter(title=title).exists():
            raise serializers.ValidationError({'title': 'A special offer with this title already exists.'})

        return data

    def create(self, validated_data):
        return specialoffers.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Check if the 'title' field is being updated and if the new title already exists
        new_title = validated_data.get('title')
        if new_title and new_title != instance.title and specialoffers.objects.filter(title=new_title).exists():
            raise serializers.ValidationError({'title': 'A special offer with this title already exists.'})

        # Update the instance with the validated data
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.status = validated_data.get('status', instance.status)
        instance.display_order = validated_data.get('display_order', instance.display_order)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()
    


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactUs
        fields = ['id', 'name', 'email', 'message', 'phone', 'reason_contact', 'subscribe', 'created_at', 'updated_at']


    def validate_email(self, value):
        """
        Validate email format.
        """
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_phone(self, value):
        """
        Validate phone number format.
        """
        if not re.match(r'^[0-9]{10}$', value):
            raise serializers.ValidationError("Enter a valid 10-digit phone number.")
        return value

    def create(self, validated_data):
        name = validated_data.get('name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')

        if not name:
            raise serializers.ValidationError({'name': 'Name field is required'})
        if not email:
            raise serializers.ValidationError({'email': 'Email field is required'})
        if not phone:
            raise serializers.ValidationError({'phone': 'Phone field is required'})

        if not name.replace(" ", "").isalpha():
            raise serializers.ValidationError("Name should contain only alphabets.")

        existing_profiles = contactUs.objects.filter(name=name, email=email, phone=phone)
        if existing_profiles.exists():
            raise serializers.ValidationError({'A profile with these details already exists.'})


        # Check if a contactUs instance already exists with the same data
        existing_instance = contactUs.objects.filter(**validated_data).first()
        if existing_instance:
            raise serializers.ValidationError({'A profile with these details already exists.'})
        
        existing_instance_name_phone_email = contactUs.objects.filter(name=validated_data.get('name'),
                                                     email=validated_data.get('email'),
                                                     phone=validated_data.get('phone')).first()
        if existing_instance_name_phone_email:
            raise serializers.ValidationError({'A profile with these name,email,phone already exists.'})
        
        existing_instance_phone_email = contactUs.objects.filter(
                                                     email=validated_data.get('email'),
                                                     phone=validated_data.get('phone')).first()
        if existing_instance_phone_email:
            raise serializers.ValidationError({'A profile with these email,phone already exists.'})
        
        existing_email = contactUs.objects.filter(email=validated_data.get('email')).first()
        if existing_email:
            raise serializers.ValidationError({'A profile with this email already exists.'})
        
        existing_phone = contactUs.objects.filter(phone=validated_data.get('phone')).first()
        if existing_phone:
            raise serializers.ValidationError({'A profile with this phone already exists.'})
            

        # If not, create a new instance
        return contactUs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing ContactUs instance.
        """

        # existing_instance = contactUs.objects.filter(**validated_data).first()
        # if existing_instance:
        #     return existing_instance
        
        existing_instance_name_phone_email = contactUs.objects.filter(name=validated_data.get('name'),
                                                     email=validated_data.get('email'),
                                                     phone=validated_data.get('phone')).first()
        if existing_instance_name_phone_email:
            raise serializers.ValidationError({'A profile with these name,email,phone already exists.'})
        
        existing_instance_phone_email = contactUs.objects.filter(
                                                     email=validated_data.get('email'),
                                                     phone=validated_data.get('phone')).first()
        if existing_instance_phone_email:
            raise serializers.ValidationError({'A profile with these email,phone already exists.'})
        
        existing_email = contactUs.objects.filter(email=validated_data.get('email')).first()
        if existing_email:
            raise serializers.ValidationError({'A profile with this email already exists.'})
        
        existing_phone = contactUs.objects.filter(phone=validated_data.get('phone')).first()
        if existing_phone:
            raise serializers.ValidationError({'A profile with this phone already exists.'})
            

        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.message = validated_data.get('message', instance.message)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.reason_contact = validated_data.get('reason_contact', instance.reason_contact)
        instance.subscribe = validated_data.get('subscribe', instance.subscribe)
        instance.save()
        return instance


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = gallery
        fields = ['id', 'image_title', 'item_desc', 'thumb_image', 'image', 'status', 'display_order', 'is_deleted', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Validate the image_title and status fields.
        """
        image_title = data.get('image_title')
        status = data.get('status')

        if not image_title:
            raise serializers.ValidationError({'image_title': 'Image title field is required'})
        if not re.match("^[a-zA-Z\s]*$", image_title):
            raise serializers.ValidationError({'image_title': 'Image title should only contain alphabets and spaces.'})

        if status not in [0, 1]:
            raise serializers.ValidationError({'status': 'Status should have a value of 0 or 1.'})

        return data

    def create(self, validated_data):
        """
        Create and return a new Gallery instance.
        """
        return gallery.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Gallery instance.
        """
        image_title = validated_data.get('image_title', instance.image_title)

        # Check if the updated image_title already exists for another instance
        if gallery.objects.filter(image_title=image_title).exists():
            raise serializers.ValidationError({ 'A gallery with this image title already exists.'})

        # Update the instance with validated data
        instance.image_title = image_title
        instance.item_desc = validated_data.get('item_desc', instance.item_desc)
        instance.thumb_image = validated_data.get('thumb_image', instance.thumb_image)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)
        instance.display_order = validated_data.get('display_order', instance.display_order)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()

        return instance


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['id', 'full_name', 'email_address', 'phone_number', 'photo', 'is_deleted', 'created_at', 'updated_at']

    # Validation methods remain the same
        

    def validate_email(self, value):
        """
        Validate email format.
        """
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        if not re.match(r'^[0-9]{10}$', value):
            raise serializers.ValidationError("Enter a valid 10-digit phone number.")
        return value

    def create(self, validated_data):
        full_name = validated_data.get('full_name')
        email_address = validated_data.get('email_address')
        phone_number = validated_data.get('phone_number')

        # Check for existing profiles with the same full_name, email_address, and phone_number
        existing_profiles = AdminProfile.objects.filter(
            full_name__iexact=full_name,
            email_address=email_address,
            phone_number=phone_number
        )

        if existing_profiles.exists():
            existing_fields = {
                'An admin profile with this full name, email address, and phone number already exists.'
            }
            raise serializers.ValidationError(existing_fields)

        return AdminProfile.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        full_name = validated_data.get('full_name', instance.full_name)
        email_address = validated_data.get('email_address', instance.email_address)
        phone_number = validated_data.get('phone_number', instance.phone_number)

        # Check if the updated full_name, email_address, and phone_number already exist in other profiles
        existing_profiles = AdminProfile.objects.filter(
            full_name__iexact=full_name,
            email_address=email_address,
            phone_number=phone_number
        ).exclude(id=instance.id)

        if existing_profiles.exists():
            raise serializers.ValidationError({
                'non_field_errors': ['An admin profile with this updated full name, email address, and phone number already exists.']
            })

        instance.full_name = full_name
        instance.email_address = email_address
        instance.phone_number = phone_number
        instance.save()

        return instance


class CMSSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = cms
        fields = ['id', 'page_title', 'short_description', 'long_description',
                   'banner_image', 'banner_text1', 'banner_text2', 'banner_text3', 'status', 'is_deleted', 
                  'created_at', 'updated_at']

    def validate(self, value):
        """
        Check if the page title contains alphabets (lowercase and uppercase) and is not already taken.
        """
        status = self.initial_data.get('status', None)

        # Check if the value contains only alphabets and whitespace
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Page title should contain only alphabets.")

        # Check if status has a valid value
        if status not in [0, 1]:
            raise serializers.ValidationError({'status': 'Status should have a value of 0 or 1.'})

        return value.lower()  # Convert name to lowercase

    
    def create(self, validated_data):
        # Extract validated data
        page_title = validated_data.get('page_title')

        # Check if a CMS page with the same title already exists
        if cms.objects.filter(page_title=page_title).exists():
            raise serializers.ValidationError({'page_title': 'A cms page with this title already exists.'})

        # Create and return the new CMS instance
        return cms.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        # Extract validated data
        page_title = validated_data.get('page_title', instance.page_title)

        # If the page title is being updated, check for uniqueness
        if page_title != instance.page_title and cms.objects.filter(page_title__iexact=page_title).exists():
            raise serializers.ValidationError({'page_title': 'A CMS page with this title already exists.'})

        # Update the instance with validated data
        instance.page_title = page_title
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.long_description = validated_data.get('long_description', instance.long_description)
        instance.banner_image = validated_data.get('banner_image', instance.banner_image)
        instance.banner_text1 = validated_data.get('banner_text1', instance.banner_text1)
        instance.banner_text2 = validated_data.get('banner_text2', instance.banner_text2)
        instance.banner_text3 = validated_data.get('banner_text3', instance.banner_text3)
        instance.status = validated_data.get('status', instance.status)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()

        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"


    def validate_status(self, value):
        """
        Validate that the status field has a value of 0 or 1.
        """
        if value not in [0, 1]:
            raise serializers.ValidationError("Status should have a value of 0 or 1.")

    def validate_category_name(self, value):
        """
        Check if category_name consists only of alphabets and spaces.
        """
        if not re.match("^[A-Za-z ]+$", value):
            raise serializers.ValidationError("Category name must contain only alphabets and spaces.")
        return value

    def create(self, validated_data):
        """
        Create and return a new category instance.
        """
        category_name = validated_data.get('category_name')
        if not category_name:
            raise serializers.ValidationError("Category name cannot be empty.")
        if category.objects.filter(category_name=category_name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        
        return category.objects.create(**validated_data)
       

    def update(self, instance, validated_data):
        """
        Update and return an existing category instance.
        """
        category_name = validated_data.get('category_name')
        if category_name and category_name != instance.category_name:
            if category.objects.exclude(id=instance.id).filter(category_name=category_name).exists():
                raise serializers.ValidationError(f"Category with the name '{category_name}' already exists.")
            instance.category_name = category_name

        # Update other fields
        instance.category_desc = validated_data.get('category_desc', instance.category_desc)
        instance.image = validated_data.get('image', instance.image)
        instance.status = validated_data.get('status', instance.status)
        instance.display_order = validated_data.get('display_order', instance.display_order)
        instance.show_on_our_menu = validated_data.get('show_on_our_menu', instance.show_on_our_menu)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)

        instance.save()
        return instance
    

  
class ItemsSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True,required=False)
    category_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = items
        fields = [
            'id',
            'category_id',
            'category_name',
            'item_name',
            'item_desc',
            'price',
            'image',
            'popular',
            'status',
            'display_order',
            'display_order_for_special_item',
            'status_for_special_item',
            'discount_description_for_special_item',
            'description_for_special_item',
            'selection_type',
            'display_order_for_our_menu',
            'status_for_our_menu',
            'created_at',
            'updated_at',
        ]
    

    def validate_status(self, value):
        """
        Validate that the status field has a value of 0 or 1.
        """
        if value not in [0, 1]:
            raise serializers.ValidationError("Status should have a value of 0 or 1.")


    def validate_category_id(self, value):
        try:
            category_instance = category.objects.get(pk=value)
        except category.DoesNotExist:
            raise serializers.ValidationError("The category with the provided ID does not exist.")
        
        if category_instance.status != 1:
            raise serializers.ValidationError("The selected category is not active.")
        
        return value

    def create(self, validated_data):
        category_id = validated_data.get('category_id')
        item_name = validated_data.get('item_name')

        # Check if category_id is provided
        if category_id is None:
            raise serializers.ValidationError("Category ID is required.")

        # Check if an item with the same name already exists in the category
        if items.objects.filter(category_id=category_id, item_name=item_name).exists():
            raise serializers.ValidationError("Only one category can have multiple items with the same name.")

        # Retrieve the category instance
        try:
            category_instance = category.objects.get(pk=category_id)
        except category.DoesNotExist:
            raise serializers.ValidationError("The category with the provided ID does not exist.")

        # Assign the category instance to the validated data
        validated_data['category_id'] = category_instance

        # Call the superclass create method to create the item
        return super().create(validated_data)

    def update(self, instance, validated_data):
    # Pop 'category_id' from validated_data if it exists
        category_id = validated_data.pop('category_id', None)

        # Update other fields of the instance
        instance.item_name = validated_data.get('item_name', instance.item_name)
        instance.item_desc = validated_data.get('item_desc', instance.item_desc)
        instance.price = validated_data.get('price', instance.price)
        instance.image = validated_data.get('image', instance.image)
        instance.popular = validated_data.get('popular', instance.popular)
        instance.status = validated_data.get('status', instance.status)
        instance.display_order = validated_data.get('display_order', instance.display_order)
        instance.display_order_for_special_item = validated_data.get('display_order_for_special_item', instance.display_order_for_special_item)
        instance.status_for_special_item = validated_data.get('status_for_special_item', instance.status_for_special_item)
        instance.discount_description_for_special_item = validated_data.get('discount_description_for_special_item', instance.discount_description_for_special_item)
        instance.description_for_special_item = validated_data.get('description_for_special_item', instance.description_for_special_item)
        instance.selection_type = validated_data.get('selection_type', instance.selection_type)
        instance.display_order_for_our_menu = validated_data.get('display_order_for_our_menu', instance.display_order_for_our_menu)
        instance.status_for_our_menu = validated_data.get('status_for_our_menu', instance.status_for_our_menu)

        if category_id is not None:
            try:
                category_instance = category.objects.get(pk=category_id)
            except category.DoesNotExist:
                raise serializers.ValidationError("The category with the provided ID does not exist.")
                
            instance.category_id = category_instance

        # Save the instance
        instance.save()
        
        # Check if an item with the same name already exists in the category
        if instance.category_id and instance.item_name:
            if items.objects.filter(category_id=instance.category_id, item_name=instance.item_name).exists():
                raise serializers.ValidationError("The category with this item name already exists...")

        return instance




    def get_category_name(self, obj):
        if obj.category_id:
            return {
                'id': obj.category_id.id,
                'category_name': obj.category_id.category_name
            }
        return None


class SubItemsSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(write_only=True,required=False)
    class Meta:
        model = SubItems
        fields = [
            'id',
            'item_id',
            'sub_item_title',
            'price',
            'short_description',
            'status',
            'is_deleted',
            'created_at',
            'updated_at',
        ]   




    def validate_status(self, value):
        """
        Validate that the status field has a value of 0 or 1.
        """
        if value not in [0, 1]:
            raise serializers.ValidationError("Status should have a value of 0 or 1.") 
    
    def validate_item_id(self, value):
        """
        Validate the existence and status of the related item.
        """
        try:
            item_instance = items.objects.get(pk=value)
        except items.DoesNotExist:
            raise serializers.ValidationError("The item with the provided ID does not exist.")
        
        if item_instance.status != 1:
            raise serializers.ValidationError("The selected item is not active.")
        
        return value

    def validate(self, data):
        item_id = data.get('item_id')
        # if item_id is None:
        #     raise serializers.ValidationError("Item ID is required.")
        
        sub_item_title = data.get('sub_item_title')
        if SubItems.objects.filter(item_id=item_id, sub_item_title=sub_item_title).exists():
            raise serializers.ValidationError("This sub-item already exists for above items.")
        
        return data

    def create(self, validated_data):
        item_id = validated_data.pop('item_id')
        try:
            item_instance = items.objects.get(pk=item_id)
        except items.DoesNotExist:
            raise serializers.ValidationError("The item with the provided ID does not exist.")
            
        validated_data['item_id'] = item_instance
        return super().create(validated_data)



    def update(self, instance, validated_data):
        item_id = validated_data.pop('item_id', None)
        if item_id:
            try:
                item_instance = items.objects.get(pk=item_id)
            except items.DoesNotExist:
                raise serializers.ValidationError("The item with the provided ID does not exist.")
                    
            validated_data['item_id'] = item_instance

        sub_item_title = validated_data.get('sub_item_title')
        if sub_item_title:
            # Check if a subitem with the same title already exists
            existing_subitem = SubItems.objects.filter(item_id=validated_data.get('item_id'),sub_item_title=sub_item_title).exists()
            if existing_subitem:
                raise serializers.ValidationError("A subitem with the same title already exists.")

        instance.sub_item_title = validated_data.get('sub_item_title', instance.sub_item_title)
        instance.price = validated_data.get('price', instance.price)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.status = validated_data.get('status', instance.status)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)

        instance.save()
        
        return instance

    


class OrderDetailsSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(write_only=True)
    subitem_id = serializers.IntegerField(write_only=True)

    order_items=serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderDetails
        fields = ['id',
                  'item_id',
                  'order_items', 
                  'subitem_id', 
                  'total_price', 
                  'name', 
                  'surname', 
                  'street_number', 
                  'city', 
                  'phone_number', 
                  'email', 
                  'is_deleted', 
                  'created_at', 
                  'updated_at'
                ]
        
    
    def validate_email(self, value):
        """
        Validate email format.
        """
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        if not re.match(r'^[0-9]{10}$', str(value)):
            raise serializers.ValidationError("Enter a valid 10-digit phone number.")
        return value

    def create(self, validated_data):
        # Extract the item_id and subitem_id data
        item_id = validated_data.pop('item_id')
        subitem_ids = validated_data.pop('subitem_id', [])  # Default to an empty list if not provided

        # Retrieve the associated item instance
        item_instance = items.objects.get(id=item_id)

        # Retrieve or create the associated subitem instances
        subitem_instances = SubItems.objects.filter(id=subitem_ids)

        # Check if order details with the same item and subitems already exist
        existing_order_details = OrderDetails.objects.filter(
            item_id=item_instance,
            subitem_id__in=subitem_instances,
            name=validated_data.get('name'),
        ).exists()

        if existing_order_details:
            raise serializers.ValidationError("Order details with the same item, subitems, name already exists...")
        



        existing_order_name_phn_em = OrderDetails.objects.filter(
             phone_number=validated_data.get('phone_number'),
             email=validated_data.get('email'),
            name=validated_data.get('name'),
        ).exists()

        if existing_order_name_phn_em:
            raise serializers.ValidationError("Order details with the name , phone , email already exists...")
        

        existing_order_details_phone_email = OrderDetails.objects.filter(
        phone_number=validated_data.get('phone_number'),
        email=validated_data.get('email')
        ).exists()

        if existing_order_details_phone_email:
            raise serializers.ValidationError("Order details with email, and phone number already exist.")
        

        if OrderDetails.objects.filter(phone_number=validated_data.get('phone_number')).exists():
            raise serializers.ValidationError(" phone number already exists in Order details...")
        

        if OrderDetails.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError(" email already exists in Order details...")
        
        
        # Create the order details instance
        order_details = OrderDetails.objects.create(item_id=item_instance, **validated_data)

        # Assign the subitem instances to the order details instance
        order_details.subitem_id.set(subitem_instances)

        return order_details

    

    def update(self, instance, validated_data):
        # Update fields from validated data
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.street_number = validated_data.get('street_number', instance.street_number)
        instance.city = validated_data.get('city', instance.city)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)

        # Update item_id
        item_id = validated_data.get('item_id')
        if item_id:
            instance.item_id = items.objects.get(id=item_id)

        # Update subitem_id
        subitem_ids = validated_data.get('subitem_id', [])
        instance.subitem_id.set(SubItems.objects.filter(id=subitem_ids))

        # Check if another OrderDetails instance with the same name exists
        if OrderDetails.objects.exclude(id=instance.id).filter(name=instance.name).exists():
            raise serializers.ValidationError("Order details with the same name  already exist.")
        
        # Check if another OrderDetails instance with the same name exists
        if OrderDetails.objects.exclude(id=instance.id).filter(
                                                               phone_number=instance.phone_number,
                                                               ).exists():
            raise serializers.ValidationError("Order details with the same phone_number already exist.")
        
        # Check if another OrderDetails instance with the same name exists
        if OrderDetails.objects.exclude(id=instance.id).filter(email=validated_data.get('email', instance.email)).exists():
            raise serializers.ValidationError("Order details with the same email already exist.")




        if OrderDetails.objects.exclude(id=instance.id).filter(name=instance.name,
                                                               item_id=item_id,
                                                               subitem_id=subitem_ids).exists():
            raise serializers.ValidationError("Order details with the same item_id , subitem_id and name already exist.")


        # Check if another OrderDetails instance with the same phone number exists
        if OrderDetails.objects.exclude(id=instance.id).filter(phone_number=instance.phone_number,
                                                               email=validated_data.get('email', instance.email)).exists():
            raise serializers.ValidationError("Order details with the same phone number and email already exist.")


        # Check if another OrderDetails instance with the same name exists
        if OrderDetails.objects.exclude(id=instance.id).filter(name=instance.name,
                                                               phone_number=instance.phone_number,
                                                               email=validated_data.get('email', instance.email)).exists():
            raise serializers.ValidationError("Order details with the same name,phone_number,email already exist.")

        


        instance.save()
        return instance


    def get_order_items(self, obj):
        try:
            item = obj.item_id
            # Retrieve all subitems associated with the order details
            subitems = obj.subitem_id.all() 
            subitem_data = []
            for subitem in subitems:
                subitem_data.append({
                    'subitem_id': subitem.id,
                    'subitem_title': subitem.sub_item_title
                })
            return {
                'item_id': item.id, 
                'item_name': item.item_name,
                'subitems': subitem_data
            }  
        except items.DoesNotExist:
            return None
        

class AllTablesSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = ['booked', 'available']

    def validate_status(self, value):
        lowercase_value = value.lower()
        lowercase_choices = [choice.lower() for choice in self.STATUS_CHOICES]
        print("Lowercase choices:", lowercase_choices)
        print("Lowercase value:", lowercase_value)
        if lowercase_value not in lowercase_choices:
            raise serializers.ValidationError('Invalid status choice. Status must be one of: {}'.format(', '.join(self.STATUS_CHOICES)))
        return value

    # def validate_status(self, value):
    #     lowercase_value = value.lower()
    #     lowercase_choices = [choice.lower() for choice in self.STATUS_CHOICES]
    #     if lowercase_value not in lowercase_choices:
    #         raise serializers.ValidationError('Invalid status choice. Status must be one of: {}'.format(', '.join(self.STATUS_CHOICES)))
    #     return value


    class Meta:
        model = AllTables
        fields = ['id', 'table_name', 'no_of_seats', 'status', 'from_time', 'to_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_table_name(self, value):
        if AllTables.objects.exclude(id=self.instance.id if self.instance else None).filter(table_name__iexact=value).exists():
            raise serializers.ValidationError('Table name must be unique.')
        return value

    # def validate_positive_integer(self, value):
    #     if not 1 <= value <= 20:
    #         raise serializers.ValidationError('Number of seats must be between 1 and 20.')
    #     return value
    def validate_positive_integer(self, value):
        if value is not None and (value < 1 or value > 20):
            raise serializers.ValidationError('Number of seats must be between 1 and 20.')
        elif value is not None and value < 0:
            raise serializers.ValidationError('Number of seats cannot be negative.')
        return value
    
    def validate_no_of_seats(self, value):
        if value is not None and not 1 <= value <= 20:
            raise serializers.ValidationError('Number of seats must be between 1 and 20.')
        return value
    

    def validate(self, data):
        from_time = data.get('from_time')
        to_time = data.get('to_time')

        if from_time and to_time:
            if from_time >= to_time:
                raise serializers.ValidationError({'to_time': 'End time must be after start time.'})

        return data
        

from .models import BookTheTable, AllTables
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime, time
from django.utils import timezone



    
#AllTablesSerializer Code
class AllTablesSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = ['booked', 'available']

    def validate_status(self, value):
        lowercase_value = value.lower()
        lowercase_choices = [choice.lower() for choice in self.STATUS_CHOICES]
        print("Lowercase choices:", lowercase_choices)
        print("Lowercase value:", lowercase_value)
        if lowercase_value not in lowercase_choices:
            raise serializers.ValidationError('Invalid status choice. Status must be one of: {}'.format(', '.join(self.STATUS_CHOICES)))
        return value


    class Meta:
        model = AllTables
        fields = ['id', 'table_name', 'no_of_seats', 'status', 'from_time', 'to_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_table_name(self, value):
        if AllTables.objects.exclude(id=self.instance.id if self.instance else None).filter(table_name__iexact=value).exists():
            raise serializers.ValidationError('Table name must be unique.')
        return value

    def validate_positive_integer(self, value):
        if value is not None and (value < 1 or value > 20):
            raise serializers.ValidationError('Number of seats must be between 1 and 20.')
        elif value is not None and value < 0:
            raise serializers.ValidationError('Number of seats cannot be negative.')
        return value
    
    def validate_no_of_seats(self, value):
        if value is not None and not 1 <= value <= 20:
            raise serializers.ValidationError('Number of seats must be between 1 and 20.')
        return value
    

    def validate(self, data):
        from_time = data.get('from_time')
        to_time = data.get('to_time')

        if from_time and to_time:
            if from_time >= to_time:
                raise serializers.ValidationError({'to_time': 'End time must be after start time.'})

        return data



#BookTheTableSerializer code
class BookTheTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTheTable
        fields = ['id', 'table_id', 'customer_name', 'phone_number', 'email_address', 'total_members', 'date', 'timings', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        
    def validate(self, data):
        # Common validations
        table_id = data.get('table_id')
        date = data.get('date')
        timings = data.get('timings')
        total_members = data.get('total_members')

        if table_id is None:
            raise serializers.ValidationError({'table_id': 'Table ID cannot be null.'})

        if not isinstance(table_id, AllTables):
            raise serializers.ValidationError({'table_id': 'Invalid table ID provided.'})

        if total_members is not None and total_members <= 0:
            raise serializers.ValidationError("Total members must be a positive integer.")

        # Return validated data
        return data
    
    def validate_phone_number(self, value):
        pattern = r'^\d{10}$'  # 10 digits phone number pattern
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid phone number format. Phone number must be exactly 10 digits.")
        return value

    def validate_email_address(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Invalid email address format.")
        return value
    
    
    
    def create(self, validated_data):
        # Create method-specific validations
        table_id = validated_data.get('table_id')
        date = validated_data.get('date')
        timings = validated_data.get('timings')
        total_members = validated_data.get('total_members')

        # Validate total members
        if total_members is not None and total_members <= 0:
            raise serializers.ValidationError("Total members must be a positive integer.")
        
        # Check if the table is available for booking
        if table_id:
            if not table_id.status == 'Available':
                raise serializers.ValidationError({'table_id': 'Selected table is not available for booking.'})

        if total_members is not None and total_members > table_id.no_of_seats:
            raise serializers.ValidationError(f'This table has only {table_id.no_of_seats} seats. You cannot book for {total_members} members.')

        # Validate booking date
        current_date = datetime.now().date()
        if date < current_date:
            raise serializers.ValidationError({'date': 'Booking date cannot be in the past.'})

        # Validate booking time
        current_time = datetime.now().time()
        if date == current_date and timings <= current_time:
            raise serializers.ValidationError({'timings': 'Booking time cannot be in the past.'})
        
        # Validate operating hours
        operating_hours_start = time(5, 0)
        operating_hours_end = time(23, 0)
        if not (operating_hours_start <= timings <= operating_hours_end):
            raise serializers.ValidationError({'timings': 'Booking time must be within operating hours (5 a.m. to 11 p.m.).'})
        
            # Validate existing bookings
        existing_bookings = BookTheTable.objects.filter(table_id=table_id, date=date, timings__gte=timings)
        if existing_bookings.exists():
            latest_booking = existing_bookings.latest("timings")
            booking_duration = datetime.combine(date, latest_booking.timings) + timedelta(hours=1)
            end_time = booking_duration.time()
            raise serializers.ValidationError({'timings': f'This table is not available for booking at {timings}. Please choose a time after {end_time} or select another table.'})

        # Create the object
        return BookTheTable.objects.create(**validated_data)
 
    def update(self, instance, validated_data):
    # Update method-specific validations
        timings = validated_data.get('timings')
        date = validated_data.get('date')
        table_id = validated_data.get('table_id')

        # Validate if booking date is in the past
        current_date = datetime.now().date()
        if date < current_date:
            raise serializers.ValidationError({'date': 'Booking date cannot be in the past.'})

        # Validate if booking time is within operating hours
        operating_hours_start = time(5, 0)  # Assuming opening time is 5:00 AM
        operating_hours_end = time(23, 0)   # Assuming closing time is 11:00 PM
        if not (operating_hours_start <= timings <= operating_hours_end):
            raise serializers.ValidationError({'timings': 'Booking time must be within operating hours (5 a.m. to 11 p.m.).'})

        # If the booking date is today, check if the time is in the past
        if date == current_date:
            current_time = datetime.now().time()
            if timings <= current_time:
                raise serializers.ValidationError({'timings': 'Booking time cannot be in the past for today\'s date.'})

        # Check if there is another booking for the same date, time, and table
        existing_booking = BookTheTable.objects.filter(table_id=table_id, date=date, timings=timings).exclude(id=instance.id).first()
        if existing_booking:
            raise serializers.ValidationError({'timings': f'This table is already booked for the same date and time.'})

        # Update the object
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email_address = validated_data.get('email_address', instance.email_address)
        instance.total_members = validated_data.get('total_members', instance.total_members)
        instance.date = validated_data.get('date', instance.date)
        instance.timings = validated_data.get('timings', instance.timings)
        instance.table_id = validated_data.get('table_id', instance.table_id)  # Update table_id field
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()
        return instance
