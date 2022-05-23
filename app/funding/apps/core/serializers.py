from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.fields import empty


class CoreSerializer(Serializer):
    def get_validators(self):
        """
        Determine the set of validators to use when instantiating serializer.
        """
        # If the validators have been declared explicitly then use that.
        validators = getattr(getattr(self, 'Meta', None), 'validators', None)
        if validators is not None:
            return list(validators)

        # Otherwise use the default set of validators.
        return (
            self.get_unique_together_validators() +
            self.get_unique_for_date_validators()
        )
