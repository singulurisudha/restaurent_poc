from django.urls import path
from .api_views import (ItemsListCreate,ItemsRetrieveUpdateDestroy,CategoryListCreateAPIView,
                        CategoryRetrieveUpdateDestroyAPIView,OrderDetailsListCreateAPIView,
                        OrderDetailsRetrieveUpdateDestroyAPIView,SubItemsRetrieveUpdateDestroyAPIView,
                        CMSListCreateView,CMSRetrieveUpdateDestroyView,SubItemsListCreateAPIView,
                        AdminProfileListCreateAPIView,AdminProfileRetrieveUpdateDestroyAPIView,
                        GalleryRetrieveUpdateDestroy,GalleryListCreate,ContactUsListCreate,ContactUsRetrieveUpdateDestroy,
                        SpecialOfferListCreateAPIView,SpecialOfferRetrieveUpdateDestroyAPIView,UserRegistrationView,UserLoginView,
                        AllTablesListCreate,AllTablesRetrieveUpdateDestroy,
                        )

urlpatterns = [



    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail-retrieve-update-destroy'),


    path('items/', ItemsListCreate.as_view(), name='items-list-create'),
    path('items/<int:pk>/', ItemsRetrieveUpdateDestroy.as_view(), name='items-detail-retrieve-update-destroy'),


    path('order-details/', OrderDetailsListCreateAPIView.as_view(), name='order-details-list-create'),
    path('order-details/<int:pk>/', OrderDetailsRetrieveUpdateDestroyAPIView.as_view(), name='order-details-retrieve-update-destroy'),


    path('gallery/', GalleryListCreate.as_view(), name='gallery-list-create'),
    path('gallery/<int:pk>/', GalleryRetrieveUpdateDestroy.as_view(), name='gallery-detail'),


    path('tables/', AllTablesListCreate.as_view(), name='all_tables_list_create'),
    path('tables/<int:pk>/', AllTablesRetrieveUpdateDestroy.as_view(), name='all_tables_retrieve_update_destroy'),


    path('special-offers/', SpecialOfferListCreateAPIView.as_view(), name='special-offer-list-create'),
    path('special-offers/<int:pk>/', SpecialOfferRetrieveUpdateDestroyAPIView.as_view(), name='special-offer-detail'),


    path('cms/', CMSListCreateView.as_view(), name='cms-list-create'),
    path('cms/<int:pk>/', CMSRetrieveUpdateDestroyView.as_view(), name='cms-detail'),

    path('contact-us/', ContactUsListCreate.as_view(), name='cms-list-create'),
    path('contact-us/<int:pk>/', ContactUsRetrieveUpdateDestroy.as_view(), name='cms-detail'),


    path('sub-items/', SubItemsListCreateAPIView.as_view(), name='subitem-list-create'),
    path('sub-items/<int:pk>/', SubItemsRetrieveUpdateDestroyAPIView.as_view(), name='subitem-detail'),


    path('admin-profiles/', AdminProfileListCreateAPIView.as_view(), name='admin-profile-list'),
    path('admin-profiles/<int:pk>/',AdminProfileRetrieveUpdateDestroyAPIView.as_view(), name='admin-profile-detail'),
]
