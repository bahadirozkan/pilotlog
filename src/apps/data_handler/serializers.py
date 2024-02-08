from rest_framework import serializers

from .models import Aircraft, Airfield, BaseModel, Flight, Pilot
from .utils import process_json_data


class ImportDataSerializer(serializers.Serializer):
    file = serializers.FileField()
    # Shared class attribute to store processed data
    processed_data = None

    def getGenericSerializer(self, model_arg):
        """
        takes a model argument (model_arg) and returns
        a dynamically created GenericSerializer class
        using the serializers.ModelSerializer
        """
        class GenericSerializer(serializers.ModelSerializer):
            class Meta:
                model = model_arg
                fields = '__all__'

        return GenericSerializer

    def process_data(self, data):
        """
        Process each entry in the JSON data.
        """
        processed_data = []
        for entry in data:
            table = entry.get('table')
            if table:
                model = {
                    'aircraft': Aircraft,
                    'airfield': Airfield,
                    'flight': Flight,
                    'pilot': Pilot,
                }.get(table.lower(), BaseModel)
                processed_data.append((model, entry))
        return processed_data

    def validate(self, attrs):
        """
        Validate that the JSON data contains fields required for each model.
        """
        if not self.processed_data:
            data = process_json_data(attrs['file'])
            if not data:
                raise serializers.ValidationError("Invalid JSON data format")
            self.processed_data = self.process_data(data)

        required_fields = {
            BaseModel: ['guid'],
            Pilot: ['PilotName', 'PilotEMail'],
            Airfield: ['AFName'], # 'City', 'Notes'
            Aircraft: ['Make', 'Model', 'Category', 'Class', 'Complex', 'HighPerf'],
            Flight: ['DateLOCAL', 'Route', 'DepTimeUTC', 'ArrTimeUTC', 'minTOTAL'],
        }

        for model_class, entry in self.processed_data:
            required = required_fields.get(model_class, [])
            missing_fields = [field for field in required if field not in entry.get('meta', {})]
            if missing_fields:
                raise serializers.ValidationError(f"Missing required fields for {model_class.__name__}: {', '.join(missing_fields)}")

        return attrs

    def import_data(self, request, file):
        """
        Dynamically import data to Aircraft, Airfield,
        Pilot or Flight according to the table parameter
        on the imported file
        """
        if not self.processed_data:
            data = process_json_data(file)
            if not data:
                return False, "Invalid JSON data format"
            self.processed_data = self.process_data(data)

        try:
            for model_class, entry in self.processed_data:
                # Create serializer dynamically
                generic_serializer = self.getGenericSerializer(model_class)
                model_serializer = generic_serializer(data=entry)

                if model_serializer.is_valid():
                    model_serializer.save()
                else:
                    return False, model_serializer.errors

            return True, None # Success

        except Exception as e:
            return False, str(e)
