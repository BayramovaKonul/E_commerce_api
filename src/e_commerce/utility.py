def calculate_cart_totals(cart_data):
        sub_total = sum([item['item_total'] for item in cart_data])
        shipping_cost = 1.00
        tax = float(sub_total) * 0.10
        cart_total = float(sub_total) + shipping_cost + tax

        return {
            'sub_total': round(sub_total, 2),
            'tax': round(tax, 2),
            'shipping_cost': shipping_cost,
            'cart_total': round(cart_total, 2)
        }