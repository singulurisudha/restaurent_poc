from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

from rest_framework import generics
from .models import (
category, 
items, 
OrderDetails, 
cms,
SubItems,
contactUs,
AdminProfile,
gallery,
specialoffers,
AllTables,
)

from restaurent.serializers import (
OrderDetailsSerializer,
ContactUsSerializer,
CategorySerializer,
SubItemsSerializer,
ItemsSerializer,
CMSSerializer,
AdminProfileSerializer,
GallerySerializer,
SpecialOfferSerializer,
UserRegistrationSerializer,
UserLoginSerializer,
ForgetPasswordUpdateSerializer,
AllTablesSerializer
)




class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Use filter to get a queryset of users with the given email
            users = User.objects.filter(email=email)

            if users.exists():
                user = users.first()

                # Check the password for the first user in the queryset
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'tokens': {
                            'access': str(refresh.access_token),
                            'refresh': str(refresh)
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"detail": "Email is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        serializer = ForgetPasswordUpdateSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)

                # Reset the password
                user.set_password(password)
                user.save()

                return Response({"detail": "Password reset successfully"}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AllTablesListCreate(generics.ListCreateAPIView):
    queryset = AllTables.objects.filter(is_deleted=False).order_by('id')
    serializer_class = AllTablesSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # current_time = timezone.now()
        # print("Current time:", current_time)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Table created successfully","status code":status.HTTP_201_CREATED, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllTablesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = AllTables.objects.all()
    serializer_class = AllTablesSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Table updated successfully","status code":status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({"message": "Table soft-deleted successfully","status code":status.HTTP_204_NO_CONTENT}, status=status.HTTP_204_NO_CONTENT)
    
#AllTables Restore API View
class AllTablesRestore(generics.GenericAPIView):
    queryset = AllTables.objects.all()
    serializer_class = AllTablesSerializer

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs['pk'], is_deleted=True)
        instance.is_deleted = False
        instance.save()
        serializer = self.get_serializer(instance)
        return Response({"message": "Table restored successfully","status code":status.HTTP_200_OK, "data": serializer.data}, status=status.HTTP_200_OK)


class ContactUsListCreate(generics.ListCreateAPIView):
    queryset = contactUs.objects.all()
    serializer_class = ContactUsSerializer


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Contact Us fetched successfully",
            "statusCode": status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Contact Us created successfully",
                "status_code": status.HTTP_201_CREATED,
                "result":serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = contactUs.objects.all()
    serializer_class = ContactUsSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Contact Us retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Contact Us not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Contact Us updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Contact Us not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "Contact Us deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "Contact Us not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)


class GalleryListCreate(generics.ListCreateAPIView):
    queryset = gallery.objects.all()
    serializer_class = GallerySerializer



    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Gallery fetched successfully",
            "statusCode": status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Gallery created successfully",
                "statusCode": status.HTTP_201_CREATED,
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class GalleryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = gallery.objects.all()
    serializer_class = GallerySerializer


    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Gallery retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Gallery not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Gallery updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Gallery not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "Gallery deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "Gallery not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)


    




class AdminProfileListCreateAPIView(generics.ListCreateAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "message": "Admin Profile created successfully",
                "status_code": status.HTTP_201_CREATED
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Admin Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "message": "Categories fetched successfully",
            "statusCode": status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Category created successfully",
                "statusCode": status.HTTP_201_CREATED,
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Category retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Category not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Category updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Category not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "Category deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "Category not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)



class ItemsListCreate(generics.ListCreateAPIView):
    queryset = items.objects.all()
    serializer_class = ItemsSerializer

    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "Items fetched successfully",
            "status code":status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the item
            serializer.save()
            return Response({
                "message": "Item created successfully",
                "status_code": status.HTTP_201_CREATED,
                "result": serializer.data,
                
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to create item",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors,
           
        }, status=status.HTTP_400_BAD_REQUEST)




class ItemsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = items.objects.all()
    serializer_class = ItemsSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Item retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Item not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Item updated successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
               
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            "message": "Item deleted successfully",
            "status_code": status.HTTP_204_NO_CONTENT
        }, status=status.HTTP_204_NO_CONTENT)
    


class SubItemsListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubItems.objects.all()
    serializer_class = SubItemsSerializer

    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "Sub-Items fetched successfully",
            "status code":status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the subitem
            serializer.save()
            return Response({
                "message": "Successfully created sub-item...",
                "status_code": status.HTTP_201_CREATED,
                "result":serializer.data,
            }, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubItemsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubItems.objects.all()
    serializer_class = SubItemsSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Sub Item retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Sub Item not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
    

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Sub Item updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Sub Item not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "Sub Item deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "Sub Item not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
    


class CMSListCreateView(generics.ListCreateAPIView):
    """
    List all cms instances or create a new cms instance.
    """
    queryset = cms.objects.all()
    serializer_class = CMSSerializer



    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "Content fetched successfully",
            "status code":status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the subitem
            serializer.save()
            return Response({
                "message": "Content Successfully created sub-item...",
                "status_code": status.HTTP_201_CREATED,
                "result":serializer.data,
            }, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CMSRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a cms instance.
    """
    queryset = cms.objects.all()
    serializer_class = CMSSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "content retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "content not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
    

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "content updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "content not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "content deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "content not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        


class SpecialOfferListCreateAPIView(generics.ListCreateAPIView):
    queryset = specialoffers.objects.all()
    serializer_class = SpecialOfferSerializer


    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "special offer fetched successfully",
            "status code":status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the subitem
            serializer.save()
            return Response({
                "message": "special offer Successfully created,...",
                "status_code": status.HTTP_201_CREATED,
                "result":serializer.data,
            }, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialOfferRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = specialoffers.objects.all()
    serializer_class = SpecialOfferSerializer


    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "special offer retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "special offer not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "special offer updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "special offer not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "special offer deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "special offer not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    


  

class OrderDetailsListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response({
            "message": "Order details fetched successfully",
            "status code":status.HTTP_200_OK,
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the subitem
            serializer.save()
            return Response({
                "message": "Order details Successfully created sub-item...",
                "status_code": status.HTTP_201_CREATED,
                "result":serializer.data,
            }, status=status.HTTP_201_CREATED)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance)
            return Response({
                "message": "Order details retrieved successfully",
                "status_code": status.HTTP_200_OK,
                "result": serializer.data,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Order details not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Order details updated successfully",
                    "status_code": status.HTTP_200_OK,
                    "result": serializer.data,
                    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "Order details not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({
                "message": "Order details deleted successfully",
                "status_code": status.HTTP_204_NO_CONTENT
            }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "message": "Order details not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

    


