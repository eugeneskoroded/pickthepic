from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from . import forms, models, serializers
from PIL import Image
from pickthepic.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
def loginPage(request):
    context = {}
    return render(request, 'index.html', context)


def logOut(request):
    logout(request)
    return redirect('login')


def admin_base(request):
    collections = models.Collection.objects.all()

    return render(request, 'admin_base.html', {'collections': collections})


def create(request):
    if request.method == "POST":
        coll = models.Collection()
        coll.name = request.POST.get('name_field')
        coll.save()
    return HttpResponseRedirect("/admin_base")


def edit(request, slug_collection: str):
    collection = get_object_or_404(models.Collection, slug=slug_collection)
    images = models.Image.objects.filter(collection_id=collection.id)
    return render(request, 'edit.html', {'collection': collection, 'images': images})


def name_change(request, slug_collection: str):
    if request.method == "POST":
        collection = models.Collection.objects.get(slug=slug_collection)
        collection.name = request.POST.get('name_field', collection.name)
        if request.POST.get('collection_show') == 'on':
            collection.show = True
        else:
            collection.show = False
        collection.cover = request.FILES.get('cover_image', collection.cover)
        collection.save()
        return HttpResponseRedirect("/edit/{}".format(collection.slug))


def image_add(request, slug_collection: str):
    if request.method == "POST":
        collection = models.Collection.objects.get(slug=slug_collection)
        image = models.Image(image=request.FILES.get('add_image'), collection=collection)
        image.save()
        return HttpResponseRedirect("/edit/{}".format(collection.slug))


def image_delete(request, slug_collection: str):
    if request.method == "POST":
        collection = models.Collection.objects.get(slug=slug_collection)
        image = models.Image.objects.filter(image=request.POST.get('delete_image'))
        image.delete()
        return HttpResponseRedirect("/edit/{}".format(collection.slug))


class GetCollectionView(APIView):
    def get(self, request):
        queryset = models.Collection.objects.all()
        serializer_for_queryset = serializers.CollectionSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)


class GetCollectionImagesView(APIView):
    def get(self, request, coll_id):
        queryset = models.Image.objects.filter(collection_id=int(coll_id))
        serializer_for_queryset = serializers.ImageSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer_for_queryset.data)


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')
