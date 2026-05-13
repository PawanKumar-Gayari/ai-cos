class BaseRepository:

    model = None

    @classmethod
    def get_by_id(cls, obj_id):
        return cls.model.objects.filter(id=obj_id).first()

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)