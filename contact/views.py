from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Contact
from .forms import ContactForm


# Create your views here.
# View all contacts
def contact_list(request):
    query = request.GET.get('search')
    if query:
        contacts = Contact.objects.filter(first_name__icontains=query) | Contact.objects.filter(email__icontains=query)
    else:
        contacts = Contact.objects.all()
    return render(request, 'contact/contact_list.html', {'contacts': contacts})


# Add new contact
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact added successfully!")
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contact/add_contact.html', {'form': form})


# Edit contact
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully!")
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contact/edit_contact.html', {'form': form})


# View contact details
def view_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'contact/view_contact.html', {'contact': contact})


# Delete contact
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Contact deleted successfully!")
    return redirect('contact_list')


# Search contact
def search_contacts(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        contacts = Contact.objects.filter(first_name__icontains=query) | Contact.objects.filter(email__icontains=query)
        return render(request, 'contact/view_contact.html', {'contacts': contacts})
    return render(request, 'contact/view_contact.html')
