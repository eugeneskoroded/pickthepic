"""pickthepic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ..api import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logOut, name='logout'),
    path('admin_base/', views.admin_base, name='home'),
    path('admin_base/create/', views.create, name='create'),
    path('admin_base/statistics/', views.statistics, name='statistics'),
    path('admin_base/statistics/probs_change/', views.probs_change, name='probs_change'),
    path('admin_base/statistics/stat_change/', views.stat_change, name='stat_change'),
    path('edit/<slug:slug_collection>/', views.edit, name='collection-edit'),
    path('edit/<slug:slug_collection>/name_change/', views.name_change, name='collection-edit_name'),
    path('edit/<slug:slug_collection>/image_add/', views.image_add, name='collection-edit_add'),
    path('edit/<slug:slug_collection>/image_delete/', views.image_delete, name='collection-edit_delete'),
    path('api/collections/', views.GetCollectionView.as_view()),
    path('api/get_variant/', views.GetVariantView.as_view()),
    path('api/variant_a/add_view/', views.AddVariantViewA.as_view()),
    path('api/variant_a/add_conv/', views.AddVariantConvA.as_view()),
    path('api/variant_b/add_view/', views.AddVariantViewB.as_view()),
    path('api/variant_b/add_conv/', views.AddVariantConvB.as_view()),
    path('api/<coll_id>/', views.GetCollectionImagesView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
