from django.shortcuts import render, get_object_or_404
from .models import Listing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .choices import price_choices, bedroom_choices, state_choices


# Create your views here.

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get("page")
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    listings = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listings
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by("-list_date")

    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get("keywords")
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # city
    if "city" in request.GET:
        city = request.GET.get("city")
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if "state" in request.GET:
        state = request.GET.get("state")
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET.get("bedrooms")
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # price
    if "price" in request.GET:
        price = request.GET.get("price")
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'queryset_list': queryset_list,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'values': request.GET,
    }
    return render(request, 'listings/search.html', context)
