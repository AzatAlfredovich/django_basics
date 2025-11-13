from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.services import get_products_from_cache, get_products_by_category


class CategoryProductView(ListView):
    model = Product
    template_name = "catalog/category_product.html"
    context_object_name = "products"

    def get_queryset(self):
        # Получаем ID категории из URL
        category_id = self.kwargs["category_id"]
        # Используем вспомогательную функцию для получения продуктов
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем полный список категорий в контекст
        context["categories"] = Category.objects.all()
        current_category = Category.objects.get(id=self.kwargs["category_id"])
        context["current_category_name"] = current_category.name

        return context


class ProductListView(ListView):
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем все категории и передаем их в шаблон
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        return get_products_from_cache()

    # catalog/product_list.html


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    # fields = ("name", "description", "image", "category", "price")
    success_url = reverse_lazy("catalog:home")

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser:
            return ProductForm
        elif user == self.object.owner:
            return ProductForm
        elif user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        else:
            raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        # Проверяем права на удаление
        if not (
            request.user.is_superuser
            or request.user == self.get_object().owner
            or request.user.has_perm("catalog.delete_product")
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение отправлено!")


# def home(request):
#     products = Product.objects.all()
#     context = {"products": products}
#     return render(request, "home.html", context)


# def contacts(request):
#     return render(request, "contacts.html")


# def contact_message(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         message = request.POST.get("message")
#         return HttpResponse(f"Спасибо, {name}! Ваше сообщение отправлено!")
#     return render(request, "catalog/contacts.html")


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {"product": product}
#     return render(request, "product_detail.html", context)
