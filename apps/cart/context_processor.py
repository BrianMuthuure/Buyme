from .cart import Cart


def cart(request):
    """
    Context processor to make the cart available to all templates.
    """
    return {'cart': Cart(request)}
