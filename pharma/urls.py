"""pharma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

import core.views as coreviews
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/$', coreviews.LandingPageView.as_view(), name='home'),
    url(r'^listing/$', coreviews.ListingListView.as_view(), name='listing_list'),
    url(r'^listing/(?P<pk>\d+)/$', coreviews.ListingDetailView.as_view(), name='listing_detail'),
    url(r'^listing/create$', coreviews.CreateListingView.as_view(), name='create_listing'),
    url(r'^listing/edit/(?P<pk>\d+)/$', coreviews.UpdateListingView.as_view(), name='update_listing'),
    url(r'^listing/delete/(?P<pk>\d+)/$', coreviews.DeleteListingView.as_view(), name='delete_listing'),
    url(r'^listing/enquiry/(?P<pk>\d+)/$', coreviews.enquiry, name='enquiry'),
    url(r'^company/$', coreviews.CompanyListView.as_view(), name='company_list'),
    url(r'^company/(?P<pk>\d+)/$', coreviews.CompanyDetailView.as_view(), name='company_detail'),
    url(r'^company/create$', coreviews.CreateCompanyView.as_view(), name='create_company'),
    url(r'^company/review/(?P<pk>\d+)/$', coreviews.review, name='create_review'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', coreviews.signup, name='signup'),
    url(r'^profile/$', coreviews.user_profile, name='user_profile'),
    url(r'^profile/create$', coreviews.ProfileCreateView.as_view(), name='create_profile'),
    url(r'^profile/edit/(?P<pk>\d+)/$', coreviews.UpdateProfileView.as_view(), name='update_profile'),
    url(r'^test/$', coreviews.TestPageView.as_view(), name='test'),
    url(r'^email/$', coreviews.email, name='email'),
    url(r'^search/$', coreviews.search, name='search_results'),
    url(r'^filter/$', coreviews.filter, name='filter_results'),
    url(r'^search-company/$', coreviews.search_company, name='search_company'),
    url(r'^filter-company/$', coreviews.filter_company, name='filter_company'),
    url(r'^retire/(?P<pk>\d+)/$', coreviews.retire, name='listing_retire'),
    url(r'^ajax/autocomplete/$', coreviews.autocomplete, name='ajax_autocomplete')
    
   

    
]

# if settings.DEBUG:
#         urlpatterns += patterns('django.views.static', (r'media/(?P<path>.*)','serve',
#             {'document_root': settings.MEDIA_ROOT}), )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

