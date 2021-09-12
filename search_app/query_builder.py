# Separated mongo query builder for better testability.
def build_mongo_query(search_term):
    return {
                'headline': {
                    '$regex': search_term,
                    '$options' :'i' # case-insensitive
                }
            }