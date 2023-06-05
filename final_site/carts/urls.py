from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from . import views
from .api_views import *
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'CartViewSet',CartViewSet,basename='cartviewset')


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/cart/', include(router.urls)),
    path('api/getcart',CartListCreateView.as_view(),name='cartlistcreate'),
    path('api/add_cart/<int:product_id>/',add_cart,name='add_cart'),
    path('api/remove_cart/<int:product_id>/<int:cart_item_id>/',remove_cart,name='remove_cart'),
    path('api/remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('api/CartRetrieveUpdateDestroyView',CartRetrieveUpdateDestroyView.as_view(),name='CartRetrieveUpdateDestroyView'),
    path('api/CartItemRetrieveUpdateDestroyView',CartItemRetrieveUpdateDestroyView.as_view(),name='CartItemRetrieveUpdateDestroyView'),
  
]


