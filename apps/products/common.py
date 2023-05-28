def user_directory_path(instance, filename):
    return f"products/{instance.product.name}[{instance.product.id}]/{filename}"