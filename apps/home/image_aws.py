import boto3
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponse

from apps.home.models import UploadData

ACCESS_KEY = 'AKIAR2VWMLJ2F5NMCWEF'
SECRET_KEY = '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'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def upload_image(request):
    objs = UploadData.objects.filter(name_of_identity ='').exclude(picture1='')
    #print(objs)
    for item in objs:
        imagename = str(item.picture1).replace("photos/","")
        pdfname = str(item.picture2).replace("photos/","")
        print(imagename)
        print(pdfname)
        ab = upload_to_aws(item.picture1.path, 'face-aml-target-image-collection', imagename)
        ab1 = upload_to_aws(item.picture2.path, 'face-aml-target-image-collection', pdfname)
        if ab:
            id = item.id
            exdata = UploadData.objects.get(id=id)
            exdata.name_of_identity = '2'

            exdata.save()
    return HttpResponse()