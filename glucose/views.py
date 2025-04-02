import csv
import io
from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, parser_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .filters import GlucoseFilter
from .models import Glucose
from .serializers import GlucoseSerializer

REQUIRED_COLUMNS = [
    "Seriennummer",
    "Gerätezeitstempel",
    "Aufzeichnungstyp",
    "Glukosewert-Verlauf mg/dL",
    "Glukose-Scan mg/dL",
]


class GlucosePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Glucose.objects.all()
    serializer_class = GlucoseSerializer
    pagination_class = GlucosePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GlucoseFilter
    ordering_fields = ["timestamp"]

    @action(detail=False, methods=["POST"], name="Populate Glucose Data")
    def populate(self, request):
        """
        Endpoint to pre-populate glucose data in the database via a POST request.
        The request body should contain an array of glucose records.
        """
        serializer = GlucoseSerializer(data=request.data, many=True)
        if serializer.is_valid():
            Glucose.objects.bulk_create(
                [Glucose(**item) for item in serializer.validated_data]
            )
            return Response(
                {"message": "Data successfully populated!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def find_header_row(reader):
    """Finds the correct header row and returns the column mapping."""
    for row in reader:
        if row and row[0].strip() == "Gerät":  # First column should be "Gerät"
            headers = row[1:]
            if all(col in headers for col in REQUIRED_COLUMNS):
                return headers, {col: i + 1 for i, col in enumerate(headers)}
            break
    return None, None


def parse_glucose_data(reader, header_mapping):
    """Parses CSV rows into Glucose model instances."""
    glucose_objects = []

    for row in reader:
        try:
            glucose = Glucose(
                user_id=row[header_mapping["Seriennummer"]].strip(),
                timestamp=datetime.strptime(
                    row[header_mapping["Gerätezeitstempel"]].strip(), "%d-%m-%Y %H:%M"
                ),
                record_type=int(row[header_mapping["Aufzeichnungstyp"]].strip()),
                glucose_value_trend=(
                    int(row[header_mapping["Glukosewert-Verlauf mg/dL"]].strip())
                    if row[header_mapping["Glukosewert-Verlauf mg/dL"]].strip()
                    else None
                ),
                glucose_scan=(
                    int(row[header_mapping["Glukose-Scan mg/dL"]].strip())
                    if row[header_mapping["Glukose-Scan mg/dL"]].strip()
                    else None
                ),
            )
            glucose_objects.append(glucose)
        except Exception as e:
            return f"Invalid data format: {e}"

    return glucose_objects


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_glucose_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file provided"}, status=400)

    decoded_file = file.read().decode("utf-8-sig")
    io_string = io.StringIO(decoded_file)
    reader = csv.reader(io_string)

    headers, header_mapping = find_header_row(reader)
    if not headers:
        return Response({"error": "Invalid or missing header row"}, status=400)

    glucose_objects = parse_glucose_data(reader, header_mapping)
    if isinstance(glucose_objects, str):  # If there's an error message
        return Response({"error": glucose_objects}, status=400)

    Glucose.objects.bulk_create(glucose_objects)
    return Response({"message": "CSV data uploaded successfully!"}, status=201)


# @api_view(["POST"])
# def populate_glucose_data(request):
#     """
#     Endpoint to pre-populate glucose data in the database via a POST request.
#     The request body should contain an array of glucose records.
#     """
#     serializer = GlucoseSerializer(data=request.data, many=True)
#     if serializer.is_valid():
#         Glucose.objects.bulk_create([Glucose(**item) for item in request.data])
#         return Response({"message": "Data successfully populated!"}, status=status.HTTP_201_CREATED)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
