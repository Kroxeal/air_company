def add_sum_by_status(service_class: str, price: float):
    try:
        if service_class == 'business':
            return price + 55
        elif service_class == 'standart':
            return price + 30
        elif service_class == 'economy':
            return price + 15
    except Exception as e:
        print(f"Unexpected status {e}")
        raise
