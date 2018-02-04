from django.db import models
import json

class PdfUploadModel(models.Model):
	file_name = models.CharField(max_length=150, blank=False, null=False)
	file = models.FileField(upload_to='files')
	return_csv = models.TextField()
	query_name = models.CharField(max_length = 150, blank=True, null=True)
	query_year = models.CharField(max_length = 10, blank=True, null=True)
	

	def serializer(self):
		returnDict = dict()
		returnDict["file_name"] = self.file_name
		returnDict["csv"] = self.return_csv

		return json.dumps(returnDict)


