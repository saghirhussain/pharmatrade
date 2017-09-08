from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from core.forms import UserForm, UserProfileForm, ListingForm, CompanyForm, ReviewForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from core.models import User, UserProfile, Company, Product, Listing, Review
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.db.models import Avg
from django.http import JsonResponse


# Create your vi  ews here.

class LandingPageView(TemplateView):
	template_name = "index2.html"
	model = User
	context_object_name = 'user'

class TestPageView(TemplateView):
	template_name = "send_enquiry.html"

class CompanyPageView(ListView):
	model = Company
	template_name = 'company.html'
	context_object_name = 'company'

class CompanyListView(ListView):
    model = Company
    template_name = "company_list.html"
    paginate_by = 9



class CreateListingView(CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "create_listing.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateListingView, self).form_valid(form)

class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        review_average = Review.objects.filter(company=self.get_object()).aggregate(Avg('rating'))
        review_count = Review.objects.filter(company=self.get_object()).count()
        review_average = list(review_average.values())
        review_average = review_average[0]


        if review_average is not None:
            average_review = int(round(review_average,0))
        else:
            average_review = 0
            

        context['review_list'] = Review.objects.filter(company=self.get_object())
        context['review_average'] = average_review
        context['review_count'] = review_count

        return context


class CreateCompanyView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "create_company.html"

class UpdateListingView(UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = "create_listing.html"

class DeleteListingView(DeleteView):
    model = Listing
    form_class = ListingForm
    template_name = "delete_listing.html"

    success_url = reverse_lazy('listing_list')


class ListingListView(ListView):
    model = Listing
    template_name = "listing_list2.html"
    paginate_by = 9

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listing_detail.html'
    context_object_name = 'listing'

class ProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'create_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProfileCreateView, self).form_valid(form)

class UpdateProfileView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'create_profile.html'
    
class CreateReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "create_review.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.company = self.request.company
        return super(CreateListinghView, self).form_valid(form) 

def review(request, pk):
	user = request.user
	company = Company.objects.get(pk=pk)
	

	if request.method == 'POST':
		form = ReviewForm(request.POST)
		form.instance.user = user
		form.instance.company = company
		if form.is_valid():
			form.save()
			return redirect('company_detail', pk=company.id)
	else:
		form = ReviewForm()
	return render(request, 'create_review.html', {'form': form, 'company': company})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_profile')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def user_profile(request):
    
    user = request.user
    
    # include the userprofile model in the view
    # user_profile = UserProfile(user=user)
    
    user_profile = UserProfile.objects.get(user=user)
    # display the human readable form of the choice field
    gender = user_profile.get_gender_display()

    user_listings = Listing.objects.filter(user=user)

    listing_count = user_listings.count()

    date = user.date_joined.date()
    

   

    # we need to pass all the userprofile model to the template as 'user_profile' then in template use '{{ user_profile.fieldname }}'
    return render_to_response(
            'profile.html',
            {'user_profile': user_profile, 'gender': gender, 'user': user, 'user_listings' : user_listings, 'date': date, 'listing_count': listing_count})


def enquiry(request, pk):
	user = request.user
	listing = Listing.objects.get(pk=pk)
	recepient = listing.user.email
	recepient_firstname = listing.user.userprofile.firstname
	recepient_company = listing.user.userprofile.company.company_name

	return render_to_response(
            'email.html',
            {'user': user, 'listing' : listing, 'pk': pk, 'recepient': recepient, 'recepient_firstname': recepient_firstname, 'recepient_company': recepient_company})



def email(request):
    user = request.user
    sender = user.email
    message = request.GET['message']
    recepient = request.GET['recepient']
    send_mail(
		'Subject: Enquiry from PharmaTrade',
		message,
		sender,
		[recepient],
		fail_silently=False,)
    return render_to_response(
            'enquiry_sent.html',
            {'recepient': recepient})

def search(request):
    if 'search' in request.GET and request.GET['search']:
        search = request.GET['search']
        listings = Listing.objects.filter(product__product_name__icontains=search)
        return render(request, 'filter_results.html',
            {'listings': listings})

    else:
        pitch_search_form = PitchSearch()
        return render_to_response(
            'pitch_search.html',
            {'pitch_search_form': pitch_search_form})

def search_company(request):
    if 'search' in request.GET and request.GET['search']:
        search = request.GET['search']
        companies = Company.objects.filter(company_name__icontains=search)
        return render(request, 'filter_companies.html',
            {'companies': companies})

    else:
        pitch_search_form = PitchSearch()
        return render_to_response(
            'pitch_search.html',
            {'pitch_search_form': pitch_search_form})

def filter(request):
    if request.method == 'GET':
        origin = request.GET['origin']
        if origin == 'all':
        	listings = Listing.objects.all()
        else:
        	listings = Listing.objects.filter(origin=origin)
        # pitches_filter = Pitch.objects.filter(stage=stage).filter(industry=industry)
        # pitches_stage = Pitch.objects.filter(stage=stage)
        # pitches_industry = Pitch.objects.filter(industry=industry)

        return render(request, 'filter_results.html',
            {'listings': listings, 'search': search})

def filter_company(request):
    if request.method == 'GET':
        origin = request.GET['origin']
        if origin == 'all':
        	companies = Company.objects.all()
        else:
        	companies = Company.objects.filter(country=origin)
        return render(request, 'filter_companies.html',
            {'companies': companies, 'search': search})

def filter2(request):
    if request.method == 'GET':
        country = request.GET['origin']
        segment = request.GET['type']
        companies = Company.objects.all()
        companies_filter = Company.objects.filter(country=country).filter(segment=segment)
        companies_country = Company.objects.filter(country=country)
        companies_segment = Company.objects.filter(segment=segment)

        if country == 'all' and segment == 'all':
             return render(request, 'filter_companies.html',
            {'companies': companies })

        elif country == 'all':
            return  render(request, 'filter_companies.html',
            {'companies': companies_country})

        elif segment == 'all':
            return  render(request, 'filter_companies.html',
            {'companies': companies_segment})        

        else:
            return render(request, 'filter_companies.html',
            {'companies': companies_filter})


def retire(request, pk):
    
    retire_listing = Listing.objects.get(pk=pk)
    retire_listing.is_live = False
    retire_listing.end_date = datetime.now()
    retire_listing.save()

    return redirect('user_profile')


# autocomplete the product field when adding a product to a listing
def autocomplete(request):
    if request.is_ajax():
        queryset = Product.objects.filter(product_name__startswith=request.GET.get('search', None))
        list = []        
        for i in queryset:
            list.append(i.product_name)
        data = {
            'list': list,
        }
        return JsonResponse(data)