from flask_restx import Namespace, Resource, fields

api = Namespace("dogs", description="Dogs related operations")

dog = api.model(
    "Dog",
    {
        "id": fields.String(required=True, description="The dog identifier"),
        "name": fields.String(required=True, description="The dog name"),
    },
)

post_dog = api.model(
    "Dog",
    {
        "name": fields.String(required=True, description="The dog name"),
    },
)

DOGS = [
    {"id": "medor", "name": "Medor"},
]


@api.route("/")
class DogList(Resource):
    @api.doc("list_dogs")
    @api.marshal_list_with(dog)
    def get(self):
        """List all dogs"""
        return DOGS

    @api.doc("create_dog")
    @api.expect(dog)
    @api.marshal_list_with(dog)
    def post(self):
        """Create a dog name with an identifier"""
        DOGS.append(api.payload)
        return DOGS


@api.route("/<id>")
@api.param("id", "The dog identifier")
@api.response(404, "Dog not found")
class Dog(Resource):
    @api.doc("get_dog")
    @api.marshal_with(dog)
    def get(self, id):
        """Fetch a dog given its identifier"""
        for dog in DOGS:
            if dog["id"] == id:
                return dog
        api.abort(404)

    @api.doc("update_dog")
    @api.expect(post_dog)
    @api.marshal_with(dog)
    def patch(self, id):
        """Modify a dog's name given its identifier"""
        for dog in DOGS:
            if dog["id"] == id:
                dog["name"] = api.payload["name"]
                return dog

        api.abort(404)

    @api.doc('delete_dog')
    @api.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a dog given its identifier'''
        DOGS = filter(lambda x: x['id'] == id, DOGS)
        return DOGS
