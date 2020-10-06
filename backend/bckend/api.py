from rest_framework import routers
from db_api import views as myapp_views

router = routers.DefaultRouter()
router.register('register', myapp_views.RegisterViewSet, basename='All Users')
router.register('bookcollection', myapp_views.BookCollectionViewSet, basename='collection')

