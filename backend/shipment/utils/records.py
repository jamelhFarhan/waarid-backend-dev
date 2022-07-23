from users.models import CustomUser, Company, Address


def create_contact(data):
    email = data.get('email')
    user, user_created = CustomUser.objects.get_or_create(email=email)
    if user_created:
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        phone_number = data.get('address').get('phone_number')
        address = Address.objects.create(phone_number=phone_number)
        user.address = address
        user.save()
    company_data = data.get('company')
    company_name = company_data.get('name')
    company, company_created = Company.objects.get_or_create(name=company_name,
                                                             owner=user)
    if company_created:
        address_data = {}
        address = company_data.get('address')
        address_data['country'] = address.get('country')
        address_data['city'] = address.get('city')
        address_data['street'] = address.get('street')
        address_data['house'] = address.get('house')
        address_data['postal_code'] = address.get('postal_code')
        company_address = Address(**address_data)
        company_address.save()
        company.address = company_address
        company.save()
    return user
