from rest_framework.exceptions import ValidationError


def validate_data_order_detail(serializer_instance, data):

    if not data.get('product'):
        data['partial'] = True
        data['product'] = serializer_instance.instance.product

    if data['cuantity'] <= 0:
        raise ValidationError(
            detail=('cuantity must be greater than 0'))

    if data.get('partial'):
        remaining_stock = data['product'].stock + \
            serializer_instance.instance.cuantity - data['cuantity']
    else:
        remaining_stock = data['product'].stock - data['cuantity']
    if remaining_stock < 0:
        raise ValidationError(
            detail=(f'out of stock, stock:{data["product"].stock}'))
    data['product'].stock = remaining_stock
    serializer_instance.context['remaining_stock'] = remaining_stock
    return data
