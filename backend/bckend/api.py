# import the required libraries
from rest_framework import routers
from db_api import views as myapp_views

# registering each viewset with router which in turn will generate the URL paths
router = routers.DefaultRouter()
router.register('register', myapp_views.RegisterViewSet, basename='All Users')
router.register('bookcollection', myapp_views.BookCollectionViewSet, basename='collection')

