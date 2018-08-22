
def arraypermute(collection, key):

    '''
    Returns all combinations of collection and key
    '''

    return [ str(i) + str(j) for i in collection for j in key ]


class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'arraypermute': arraypermute
       }
