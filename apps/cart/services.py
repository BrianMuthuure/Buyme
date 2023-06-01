from apps.cart.cart import Cart
from apps.cart.forms import CartAddProductForm
from apps.products.services import ProductService


class CartService:
    @staticmethod
    def add_to_cart(request, product_id):
        """
        Add a product to the cart.
        """
        cart = CartService.get_cart(request)
        product = ProductService.get_product_by_id(product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])

    @staticmethod
    def remove_from_cart(request, product_id):
        """
        Remove a product from the cart.
        """
        cart = CartService.get_cart(request)
        product = ProductService.get_product_by_id(product_id)
        cart.remove(product)

    @staticmethod
    def get_cart(request):
        """
        Get the cart from the session.
        """
        return Cart(request)
