from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from . import forms, models, serializers
#from ..pickthepic.settings import MEDIA_ROOT
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
import requests
import scipy.stats as sp
import numpy as np

key_imgbb = '24b9c134a36f15aee02b36285d79b9c5'
imgbb_upload_url = "https://api.imgbb.com/1/upload"


# Create your views here.
def conv_interval(n_views, n_conv, alpha=0.95):
    if n_views >= 2 and n_views > n_conv:
        x = [1 for i in range(n_conv)]
        x.extend([0 for i in range(n_views - n_conv)])
        x_mean = np.mean(x)
        d = np.var(x, ddof=1) * n_views / (n_views - 1)
        step = sp.t.ppf((alpha + 1) / 2, n_views - 1) * np.sqrt(d / n_views)
        interval = [round(x_mean - step, 2), round(x_mean + step, 2)]
        return interval
    else:
        return [0, 0]


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
        name_ = request.POST.get('name_field')
        if name_:
            coll.name = name_
        else:
            coll.name = 'NAME'
        coll.save()
    return HttpResponseRedirect("/admin_base")


def statistics(request):
    queryset = models.Statistics.objects.all()
    serializer_for_queryset = serializers.StatSerializer(
        instance=queryset,
        many=True
    )
    return render(request, 'statistics.html', {'statistics': serializer_for_queryset.data[0]})


def probs_change(request):
    if request.method == "POST":
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        statistics = models.Statistics.objects.get(id='1')
        statistics.a_prob = float(request.POST.get('a_prob_field', statistics.a_prob).split(',')[0])
        statistics.b_prob = float(request.POST.get('b_prob_field', statistics.b_prob).split(',')[0])
        statistics.save()
        return HttpResponseRedirect('/admin_base/statistics')


def stat_change(request):
    if request.method == 'POST':
        statistics = models.Statistics.objects.get(id='1')
        statistics.a_conversion = round(statistics.a_views_conv / statistics.a_views, 2)
        statistics.b_conversion = round(statistics.b_views_conv / statistics.b_views, 2)
        statistics.a_ci_bot, statistics.a_ci_top = conv_interval(statistics.a_views, statistics.a_views_conv)
        statistics.b_ci_bot, statistics.b_ci_top = conv_interval(statistics.b_views, statistics.b_views_conv)
        statistics.save()

        return HttpResponseRedirect('/admin_base/statistics')


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
        # cover
        img = request.FILES.get('cover_image')
        if img:
            payload = {
                "key": key_imgbb,
                "image": base64.b64encode(img.read()),
            }
            imgbb_res = requests.post(imgbb_upload_url, payload)
            imgbb_url = imgbb_res.json()['data']['url']
            collection.cover = imgbb_url
        collection.save()
        return HttpResponseRedirect("/edit/{}".format(collection.slug))


def image_add(request, slug_collection: str):
    if request.method == "POST":
        collection = models.Collection.objects.get(slug=slug_collection)
        img = request.FILES.get('add_image')
        payload = {
            "key": key_imgbb,
            "image": base64.b64encode(img.read()),
        }
        imgbb_res = requests.post(imgbb_upload_url, payload)
        imgbb_url = imgbb_res.json()['data']['url']
        image = models.Image(image=imgbb_url, collection=collection)
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


class GetVariantView(APIView):
    def get(self, request):
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        variant = np.random.choice(['A', 'B'], p=[serializer_for_queryset.data[0]['a_prob'] / 100,
                                                  serializer_for_queryset.data[0]['b_prob'] / 100])
        variant = {'variant': variant}
        return Response(variant)


class AddVariantViewA(APIView):
    def get(self, request):
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        current_views = serializer_for_queryset.data[0]['a_views']
        current_views += 1
        queryset.update(a_views=current_views)
        return Response('GACHI')


class AddVariantConvA(APIView):
    def get(self, request):
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        current_views_conv = serializer_for_queryset.data[0]['a_views_conv']
        current_views_conv += 1
        queryset.update(a_views_conv=current_views_conv)
        return Response('GACHI')


class AddVariantViewB(APIView):
    def get(self, request):
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        current_views = serializer_for_queryset.data[0]['b_views']
        current_views += 1
        queryset.update(b_views=current_views)
        return Response('GACHI')


class AddVariantConvB(APIView):
    def get(self, request):
        queryset = models.Statistics.objects.all()
        serializer_for_queryset = serializers.StatSerializer(
            instance=queryset,
            many=True
        )
        current_views_conv = serializer_for_queryset.data[0]['b_views_conv']
        current_views_conv += 1
        queryset.update(b_views_conv=current_views_conv)
        return Response('GACHI')


class LoginUser(LoginView):
    form_class = forms.LoginUserForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')
