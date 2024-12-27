from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Complaint, EmpowermentResource
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Product
from .forms import ProductForm 
from django.http import HttpResponseForbidden



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'register.html')

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('quote_page')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def quote_page(request):
    quotes = [
        "Empowered women empower women.",
        "A woman is the full circle. Within her is the power to create, nurture, and transform.",
        "The future is female.",
    ]
    return render(request, 'quote_page.html', {'quotes': quotes})

@login_required
def file_complaint(request):
    if request.method == 'POST':
        description = request.POST['description']
        complaint = Complaint(user=request.user, description=description)
        complaint.save()
        return redirect('quote_page')
    return render(request, 'file_complaint.html')

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['number']
        description = request.POST['complaint']

        # Save complaint to the database
        complaint = Complaint(
            user=request.user,
            name=name,
            email=email,
            phone_number=phone_number,
            description=description
        )
        complaint.save()
        return redirect('quote_page')
    return render(request, 'file_complaint.html')

@login_required
def empowerment_resources(request):
    resources = EmpowermentResource.objects.all()
    return render(request, 'empowerment_resources.html', {'resources': resources})

@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        complaints = Complaint.objects.all()
        return render(request, 'admin_dashboard.html', {'users': users, 'complaints': complaints})
    return redirect('quote_page')

@login_required
def resolve_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.status = 'Resolved'
    complaint.save()
    return redirect('admin_dashboard')

@login_required
def delete_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('admin_dashboard')
    return redirect('quote_page')

@login_required
def councelling(request):
    # Pass necessary context data to the template, such as quotes or resources
    return render(request, 'councelling.html')

@login_required
def job_oppurtunity(request):
    # Add any necessary context or data to pass to the template if needed
    return render(request, 'job_oppurtunity.html')


@login_required
def products(request):
    return render(request, 'product.html')



from .forms import ProductForm
from .models import Product
@login_required
def sell_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # Associate the product with the logged-in user
            product.save()
            return redirect('sell_product')  # Redirect to the same page or another page
    else:
        form = ProductForm()

    # Display all products to all users
    products = Product.objects.all()
    return render(request, 'sell_product.html', {'form': form, 'products': products})



@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Allow only the owner to update the product
    if product.user != request.user:
        return HttpResponseForbidden("You are not allowed to update this product.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('sell_product')  # Redirect to the product list page after updating
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form, 'product': product})




# View to delete a product
@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Allow only the owner to delete the product
    if product.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this product.")

    if request.method == 'POST':
        product.delete()
        return redirect('sell_product')  # Redirect to the product list page after deletion

    return render(request, 'delete_product.html', {'product': product})
