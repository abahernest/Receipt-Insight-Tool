import json
from rest_framework.response import Response
from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser

# serializers
from .serializer import DelimeterSerializer, DocumentSerializer, BlockSerializer,NewDocumentSerializer
# models
from .models import Delimeter, Document, Block
# Core
from .core import GetSubstrings

class ReceiptView (APIView):
    parser_classes = [FormParser, MultiPartParser]

    POSSIBLE_RETURN_STRINGS=["\r\n","\r","\n"]

    def get (self,request, format=None):
        try:
            documents = Document.objects.order_by("-created_at").all()
            output=[]
            for document in documents:
                serialized_document = DocumentSerializer(document).data
                blocks = document.block_set.all()
                serialized_document["blocks"] = BlockSerializer(blocks, many=True).data
                output.append(serialized_document)
            
            """My decision to Fetch all Block Objects while traversing the Document object
              is an attempt to optimize the database operation.
              Using  Document.objects.prefetch_related("block_set").all() will achieve same result
              but the operation wont be scalable. More info here
              https://www.geeksforgeeks.org/prefetch_related-and-select_related-functions-in-django/
              """
            return Response({
                "status":200,
                "data": output,
                "message": "success"
            })

        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 500,
                    'message': "Internal Server Error",
                    "error": e.args
                },
                status=500)

    def post (self, request, format=None):
        try:
            data = NewDocumentSerializer(data=request.data)

            with transaction.atomic():
                ## fetch list of delimeters
                delimeterObjects = Delimeter.objects.all()
                delimeters = DelimeterSerializer(delimeterObjects, many=True)

                [delimeters, smallest_delimiter, longest_delimiter] = self.process_delimiters(
                    delimeters.data)

                if data.is_valid():
                    file_obj = self.request.data.get('file')
                    row = 0
                    blocksArray=[]

                    document = Document.objects.create(name=file_obj.name)


                    with file_obj.open(file_obj) as file:
                        while True:
                            line = file.readline()
                            if not line:
                                break
                            
                            line = self.process_word(line)

                            blocks = GetSubstrings(line, delimeters, smallest_delimiter, longest_delimiter)
                            
                            for col_indices in blocks:
                                if col_indices[0] <= col_indices[1]:
                                    blocksArray.append(Block(
                                        begin_row=row,
                                        begin_column=col_indices[0],
                                        end_row=row,
                                        document=document,
                                        end_column=col_indices[1],
                                    ))

                            row +=1
                    
                    blocks = Block.objects.bulk_create(blocksArray)
                    serialized_blocks = BlockSerializer(blocks,many=True)
                    return Response({
                        "status": 200,
                        "data": serialized_blocks.data,
                        "message": "success"
                    })
                else:
                    print(data.errors)
                    return Response({
                        "status": 400,
                        "message": "failure",
                        "error": data.errors
                    }, status=400)
        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 500,
                    'message': "Internal Server Error",
                    "error": e.args
                },
                status=500)

    ## Helper Method
    def find_axes(self, word: str) -> (map):
        """
        Find the Non-space Starting and Ending Indices a word or phrase in a string
        
        Params:
        word (str): - The string which contains spaces, newline and words

        Returns:
        (dict[str,int]): - Dictionary object with keys "start" and "end" which represents the starting and ending index
        """
        output={"start":0,"end":0}
        
        ## find index of first non-space character
        for index, char in enumerate(word):
            if not char.isspace():
                output["start"] = index
                break
        
        ## find index of last non-space character

        # sliding window of length 1. since newline characters are multiple of 1
        end_index=len(word)-1
        while True:
            # increase end_index if current word in window isnt a newline character
            if word[end_index:] not in self.POSSIBLE_RETURN_STRINGS:
                if not word[end_index].isspace():
                    break
            end_index-=1

        output["end"] = end_index     
        return output
    
    ## Helper Method
    def contains_delimeter(self, word: str, delimeters: list[dict[str,int|str]]) -> bool:
        """
        Checks if a String contains any item from a list of characters
        
        Params:
        word (str): - The string which should be traversed
        delimeters (list[dict[str, int|Non]]): - The array that contains a dictionary of characters and their count
        
        Returns:
        (bool): - Boolean value denoting the word contains a delimiter or not
        """
        for delimeter in delimeters:

            value = json.loads(delimeter["value"])
            count = delimeter["count"]
            if value*count in word.strip():
                return True

        if word in self.POSSIBLE_RETURN_STRINGS:
            return True
        else:
            return False

    def process_word(self, word: str) -> str:
        """
        Performs cleanup on word
        
        Params:
        word (str) - The string which should be processed
        
        Returns:
        (str) - Processed word
        """

        return str(word).split("'")[1] ## line is initially returned as \b'word'

    def process_delimiters(self, delimiters :list[dict[str,int|str]]) -> list[set[str] | int]:
        """"
        Convert the delimiter object to a set of strings for faster lookup

        Params:
        delimiters (list[dict[str,int|str]]): An array of delimeter objects

        Returns:
        set[str]: A set of strings
        int: Length of the shortest delimiter
        int: length of the longest delimiter
        """
        delimiterSet= set()
        for item in delimiters:
            delimiterSet.add(json.loads(item["value"]) * item["count"])

        shortest_delim = len(min(delimiterSet, key=len))
        longest_delim = len(max(delimiterSet, key=len))
        return [delimiterSet, shortest_delim, longest_delim]

class DelimeterView (APIView):

    def get(self,request):
        try:
            delimeter_object = Delimeter.objects.all()
            serialized_delimeter = DelimeterSerializer(delimeter_object, many=True)
            return Response({
                "status":200,
                "data": serialized_delimeter.data,
                "message": "success"
            })

        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 500,
                    'message': "Internal Server Error",
                    "error": e.args
                },
                status=500)

    def post(self,request, format=None):
        try:
            request.data["value"] = json.dumps(request.data["value"])
            req_data = DelimeterSerializer(data = request.data)
            if req_data.is_valid():
                
                ## Check if Value already exists
                delimeter_count = Delimeter.objects.filter(value=req_data.data["value"]).count()
                if delimeter_count >= 1:
                    return Response(
                        {
                            "status": 400,
                            'message': "Value already exist"
                        },
                        status=400)

                delimeter = Delimeter.objects.create(**req_data.data)
                serialized_delimeter = DelimeterSerializer(delimeter)            
            
                return Response({
                    "status":200,
                    "data": serialized_delimeter.data,
                    "message": "success"
                })
            else:
                print(req_data.errors)
                return Response({
                    "status": 400,
                    "message": "failure",
                    "error": req_data.errors
                })
        except Exception as e:
            print(e)
            return Response(
                {
                    "status": 500,
                    'message': "Internal Server Error",
                    "error": e.args
                },
                status=500)