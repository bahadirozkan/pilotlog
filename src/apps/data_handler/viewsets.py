import csv

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Aircraft, Flight
from .serializers import ImportDataSerializer


def import_view(request):
    """view for importing the json file"""
    return render(request, 'import_data.html')


@method_decorator(csrf_exempt, name='dispatch')
class ImportDataView(APIView):
    """View for import. Inherits APIView from DRF"""
    def post(self, request, *args, **kwargs):
        """
        Serializer is initiated from the imported
        file as a json file. If valid saved as the
        base model
        """
        serializer = ImportDataSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            success, error = serializer.import_data(request, file)
            if success:
                return Response({"message": "Imported data successfully."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Error importing data. {error}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ExportDataView(APIView):
    """View for export. Outputs a csv file"""
    def get(self, request, *args, **kwargs):
        """Exports the data to a .csv file"""
        response = HttpResponse(content_type='text/csv')
        file_name = "export - logbook_template.csv"
        response['Content-Disposition'] = f"attachment; filename={file_name}"

        # initiate a csv file for exporting results
        csv_writer = csv.writer(response)
        # Write the title
        csv_writer.writerow(['ForeFlight Logbook Import'])
        csv_writer.writerow(['Aircraft Table'])

        header_title = ['AircraftID', 'Make', 'Model', 'Category',
                        'Class', 'Complex', 'HighPerf']
        header_row = ['guid', 'Make', 'Model', 'Category', 'Class',
                      'Complex', 'HighPerf']
        csv_writer.writerow(header_title)

        for aircraft in Aircraft.objects.all():
            csv_writer.writerow([getattr(aircraft, field)
                                 for field in header_row[0:7]])

        csv_writer.writerow(['Flights Table'])
        footer_title = ['Date', 'AircraftID', 'Route', 'TimeOut',
                        'TimeIn', 'TotalTime', 'Approach1', 'Approach2',
                        'Approach3', 'Person1', 'Person2']
        csv_writer.writerow(footer_title)

        # Modify Flight data. Merges flight with airfield and pilot
        Flight.objects.merge_pilot_airfield_data()

        # get the merged data items
        for flight_instance in Flight.objects.all():
            guid = flight_instance.guid
            date_local = flight_instance.DateLOCAL
            route = flight_instance.Route
            dep_time_utc = flight_instance.DepTimeUTC
            arr_time_utc = flight_instance.ArrTimeUTC
            min_total = flight_instance.minTOTAL

            airfield_data = flight_instance.airfield_data
            pilot_data = flight_instance.pilot_data

            if airfield_data:
                af_name = airfield_data.AFName
                city = airfield_data.City
                notes = airfield_data.Notes
            else:
                af_name = city = notes = None

            if pilot_data:
                pilot_name = pilot_data.PilotName
                pilot_email = pilot_data.PilotEMail
            else:
                pilot_name = pilot_email = None

            csv_writer.writerow([date_local, guid, route, dep_time_utc,
                                 arr_time_utc, min_total, af_name, city,
                                 notes, pilot_name, pilot_email])

        return response
