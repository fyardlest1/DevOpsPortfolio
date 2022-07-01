from django.urls import path, include
from . import views

app_name = 'store'

# URLConf
urlpatterns = [
	path('', views.homepage.as_view(), name='home'),
	path('products/', views.product_list),
	path('products/<int:id>/', views.product_detail),
	path('collections/', views.collection_list),
	path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]