def serializer_client(staff_object):
    return {
        "name": staff_object.name,
        "email": staff_object.email
    }