def query_serializer(query):
    if query == None:
        return None
    else:
        query_list = []
        for q in query:
            q['balance'] = str(q['balance'])
            query_list.append(q)
        dict = {'wallet_data': query_list}
        return dict


