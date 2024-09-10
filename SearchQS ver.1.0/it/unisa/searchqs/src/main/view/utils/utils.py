def get_attributes_from_list_of_request(request, keys, keys_list):
    if (keys is None or not isinstance(keys, list)) and (keys_list is None or not isinstance(keys_list, list)):
        return None
    attributes = {}
    if keys is not None:
        for key in keys:
            if request.method == "POST":
                attributes[key] = request.form.get(key)
            elif request.method == "GET":
                attributes[key] = request.args.get(key)
            else:
                raise Exception("errore, richiesta request non valida.")
    if keys_list is not None:
        for key_list in keys_list:
            if request.method == "POST":
                attributes[key_list] = request.form.getlist(key_list)
            elif request.method == "GET":
                attributes[key_list] = request.args.getlist(key_list)
            else:
                raise Exception("errore, richiesta request non valida.")
    print(attributes)
    return attributes

def get_attribute_request_file(request, key):
    return request.files[key]








