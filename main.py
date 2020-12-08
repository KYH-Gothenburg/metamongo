

from db.model import Customer, Api, ApiDB


def main():
    """
        POST /skapa_api/5/

        {
            user_id: 5,
            api_id: 3,
            endpoint_id: 45,
            method: 'GET',
            structure: {
                name: 'string',
                age: 'int'
            }
        }

    :return:
    """

    # api_db = ApiDB(
    #     {
    #     'api_user': 3,
    #     'data':
    #         [
    #             {
    #                 'users-name': 'Kalle',
    #                 'users-age': 45
    #             },
    #             {
    #                 'users-name': 'Lisa',
    #                 'users-age': 34
    #             }
    #         ]
    #     }
    # )
    #
    # api_db.save()
    #
    # api = Api({
    #         'user_id': 5,
    #         'api_id': 3,
    #         'endpoint_id': 45,
    #         'method': 'GET',
    #         'structure': {
    #             'name': 'users-name',
    #             'age': 'users-age'
    #         }
    #     })
    # api.save()

    api = Api.find(user_id=5, api_id=3, endpoint_id=45, method='GET').first_or_none()
    if api is not None:
        structure = api.structure
        all_data = ApiDB.find(api_user=3)

        keys = list(structure.values())

        found = []
        for document in all_data:
            for data in document.data:
                if all(elem in data for elem in keys):
                    found.append(data)

        result = []
        for item in found:
            result_dict = {}
            for k, v in structure.items():
                result_dict[k] = item[v]
            result.append(result_dict)

        print()
        data = ApiDB.query({'user-name': {'$exists': True}, 'user-age': {'$exists': True}})
        #data = ApiDB.query(', '.join(f'{{{v}: {{$exists: true}}}}' for v in structure.values()))
        print()

if __name__ == '__main__':
    main()
