from items.models import Item, BookmarkletKey, Organization
from items.forms import (
    AddItemForm,
)

import logging, json
import requests

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.sites.models import Site
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def landing(request):
    """Our main landing page"""

    if request.user.is_authenticated():
        org = Organization.objects.get(user=request.user)
        context = {'org_slug': org.slug}
        context = RequestContext(request, context)
        
        return render_to_response('items.html', context)
    
    context = RequestContext(request, {})
    return render_to_response('landing.html', context)
    
    
    
def add_item(request):

    bookmarklet_key_id = request.GET.get('bookmarklet_key', '')
    try:
        bookmarklet_key = BookmarkletKey.objects.get(key=bookmarklet_key_id)
    except BookmarkletKey.DoesNotExist:
        return render_to_response('bookmarklet_denied.html')
    if not bookmarklet_key.is_active:
        return render_to_response('bookmarklet_denied.html')
    organization = bookmarklet_key.organization
    title = request.GET.get('title', '')
    link = request.GET.get('link', '')
    description = request.GET.get('description', '')
    contributor = bookmarklet_key.display_name
    
    if request.method == 'POST':
        if not bookmarklet_key.is_active:
            return render_to_response('bookmarklet_denied.html')
            
        add_form = AddItemForm(request.POST, prefix='additem')
        
        if add_form.is_valid():
            bookmarklet_key.display_name = add_form.cleaned_data['contributor']
            bookmarklet_key.save()
            item = add_form.save(commit=False)
            item.bookmarklet_key = bookmarklet_key
            item.save()
            
            return HttpResponseRedirect(reverse('dashboard_display_items', kwargs={'slug' : organization.slug}))   
        else:
            context = {'add_form': add_form,} 
            context = RequestContext(request, context)
            return render_to_response('add_item.html', context)
    
    else:        
        form_data = {'title':title, 
                'link':link,
                'description':description,
                'contributor':contributor}
        add_form = AddItemForm(initial=form_data, prefix='additem')
        
        context = {'add_form': add_form, 'organization': organization}           
        context = RequestContext(request, context)
    
        return render_to_response('add_item.html', context)
        
        
def install_bookmarklet(request, bookmarklet_key_id):

    try:
        bookmarklet_key = BookmarkletKey.objects.get(key=bookmarklet_key_id)
    except BookmarkletKey.DoesNotExist:
        return render_to_response('bookmarklet_denied.html')
        
    organization = bookmarklet_key.organization
    bookmarklet_domain = Site.objects.get_current().domain

    context = {'bookmarklet_key': bookmarklet_key_id, 'organization': organization, 'bookmarklet_domain': bookmarklet_domain}
               
    context = RequestContext(request, context)
    
    return render_to_response('install_bookmarklet.html', context)