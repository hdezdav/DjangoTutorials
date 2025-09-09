from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.urls import reverse
from django import forms


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: David",
        })
        return context


class ContactPageView(TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Contacto"
        context["subtitle"] = "Contáctanos"
        context["email"] = "correo@ejemplo.com"
        context["address"] = "Calle 123 #321, Medellín, Colombia"
        context["phone"] = "+57 300101001"
        return context


class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 500},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1200},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 70},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 30},
    ]


class ProductIndexView(View):
    template_name = "products/index.html"

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products,
        }
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = "products/show.html"

    def get(self, request, id):
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse("home"))

        viewData = {
            "title": product["name"] + " - Online Store",
            "subtitle": product["name"] + " - Product information",
            "product": product,
        }
        return render(request, self.template_name, viewData)


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return price


class ProductCreateView(View):
    template_name = "products/create.html"

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create product",
            "form": form,
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {
                "title": "Product Created",
                "name": form.cleaned_data["name"],
                "price": form.cleaned_data["price"],
            }
            return render(request, "products/created.html", viewData)
        else:
            viewData = {
                "title": "Create product",
                "form": form,
            }
            return render(request, self.template_name, viewData)
