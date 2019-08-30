from django.core.signing import Signer
from rest_framework import mixins, viewsets


class CreateRetrieveViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    # A viewset that only provides create and single-retrieval functionality
    pass


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class IDSigner():

    def sign_id(self, value):
        signer = Signer()
        signed_id = signer.sign(value)
        thread_id = signed_id.split(':', 1)[1]
        return thread_id
