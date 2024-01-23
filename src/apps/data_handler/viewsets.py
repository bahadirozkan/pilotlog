import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Aircraft, Airfield, BaseModel, Flight, Pilot
from .serializers import ImportDataSerializer, getGenericSerializer


def import_view(request):
    """view for importing the json file"""
    return render(request, 'import_data.html')

@method_decorator(csrf_exempt, name='dispatch')
class ImportDataView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Serializer is initiated from the imported
        file as a json file. If valid saved as the
        base model
        """
        serializer = ImportDataSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            return self.import_data(request, file)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data, model_arg):
        """
        A function that creates model objects
        that are dynamically read from the imported
        file
        """
        # Select only specific fields from the meta dictionary
        selected_fields = self.get_selected_fields(validated_data, model_arg)
        return model_arg.objects.create(**selected_fields)

    def get_selected_fields(self, meta_fields, model):
        """
        Returns the fields of the model that is sent
        """
        model_fields = set([field.name for field in model._meta.fields])
        selected_fields = {key: meta_fields[key] for key in meta_fields
                           if key in model_fields}
        return selected_fields

    def import_data(self, request, file):
        """
        Dynamically import data to Aircraft, Airfield,
        Pilot or Flight according to the table parameter
        on the imported file
        """
        try:
            data = JSONParser().parse(file)
            for entry in data:
                # Add meta dict to the row
                entry.update(entry['meta'])
                # Dynamically get the model from each row
                table = entry['table']
                if table == 'aircraft':
                    model = Aircraft
                elif table == 'airfield':
                    model = Airfield
                elif table == 'flight':
                    model = Flight
                elif table == 'pilot':
                    model = Pilot
                else:
                    model = BaseModel
                # Get the Dynamic Serializer according to the model
                generic_serializer = getGenericSerializer(model)
                # Feed the data to the serializer
                model_serializer = generic_serializer(data={**entry})
                # if valid save, else throw error
                if model_serializer.is_valid():
                    model_serializer.save()
                else:
                    return Response(model_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Imported data successfully."},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error importing data. {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExportDataView(APIView):
    def get(self, request, *args, **kwargs):
        """Exports the data to a .csv file"""
        # Create the HttpResponse object with CSV header.
        response = HttpResponse(content_type='text/csv')
        file_name = "export - logbook_template.csv"
        response['Content-Disposition'] = f"attachment; filename={file_name}"

        # Create a CSV writer using the HttpResponse object as the "file"
        csv_writer = csv.writer(response)
        # Write the title of the Logbook on the first line
        csv_writer.writerow(['ForeFlight Logbook Import'])
        csv_writer.writerow(['Aircraft Table'])

        # Aircraft and Flight table titles and fields that will be exported
        header_title = ['AircraftID', 'Make', 'Model', 'Category',
                        'Class', 'Complex', 'HighPerf']
        header_row = ['guid', 'Make', 'Model', 'Category', 'Class',
                      'Complex', 'HighPerf']
        csv_writer.writerow(header_title)

        # Query all models and write the data to the CSV file
        for aircraft in Aircraft.objects.all():
            csv_writer.writerow([getattr(aircraft, field)
                                 for field in header_row[0:7]])

        csv_writer.writerow(['Flights Table'])
        footer_title = ['Date', 'AircraftID', 'Route', 'TimeOut',
                        'TimeIn', 'TotalTime', 'Approach1', 'Approach2',
                        'Approach3', 'Person1', 'Person2']
        csv_writer.writerow(footer_title)

        # Merges Flight, Airfield and Pilot data on Flight, key = "guid"
        # Can be commented out after first run, if the data is persistent.
        # It modifies the flight model
        Flight.objects.merge_pilot_airfield_data()

        for flight_instance in Flight.objects.all():
            guid = flight_instance.guid
            date_local = flight_instance.DateLOCAL
            route = flight_instance.Route
            dep_time_utc = flight_instance.DepTimeUTC
            arr_time_utc = flight_instance.ArrTimeUTC
            min_total = flight_instance.minTOTAL

            # Access related data
            airfield_data = flight_instance.airfield_data
            pilot_data = flight_instance.pilot_data

            # Access fields from airfield_data
            if airfield_data:
                af_name = airfield_data.AFName
                city = airfield_data.City
                notes = airfield_data.Notes
            else:
                af_name = city = notes = None

            # Access fields from pilot_data
            if pilot_data:
                pilot_name = pilot_data.PilotName
                pilot_email = pilot_data.PilotEMail
            else:
                pilot_name = pilot_email = None

            csv_writer.writerow([date_local, guid, route, dep_time_utc,
                                 arr_time_utc, min_total, af_name, city,
                                 notes, pilot_name, pilot_email])

        return response
