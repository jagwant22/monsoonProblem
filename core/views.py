from django.shortcuts import render, HttpResponse
import json
from django.http import JsonResponse
from django.views import View
import pandas as pd
import os
import monsoonApp.settings as settings
from tabula import read_pdf, convert_into
from .models import PdfUploadModel
import re
def home(request):
	return render(request, 'index.html', context = {})

class FileUploadClass(View):
	
	def get(self,request):
		path = request.GET['path']
		media_path = PdfUploadModel.objects.get(pk = path).return_csv
		
		if os.path.exists(media_path):
			with open(media_path, 'r') as fh:
				response = HttpResponse(fh.read())
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(media_path)
				return response
		else:
			return HttpResponse("404: Not Found")

	def post(self,request):
		return_data = dict()
		try:
			if request.method == 'POST':
				data = request.POST
				query_data = dict()
				query_data["query"] = data["queryVar"]
				query_data["year"] = data["forYear"]

				file = request.FILES["pdf_file"]

				upload_object =PdfUploadModel(
						file_name = "pdf-data",
						file = file, 
						query_name = query_data["query"],
						query_year = query_data["year"]
					)

				upload_object.save()
				file_name = upload_object.file.name
				cleaned_data = cleanData(upload_object.file.url)
				query_result = runQueryOnData(query_data, cleaned_data)
				final_data = mergeFrames(cleaned_data)
				csv_location = generateCsvFromDataFrame(final_data , file_name)
				upload_object.return_csv = csv_location
				upload_object.save()
				return_data['query'] = query_data['query']
				return_data['query_result'] = query_result
				return_data['csv_id'] = upload_object.pk
				return_data['status'] = 200
			
		except Exception as e:
			return_data['status'] = 500
			return_data['result'] = 'FAILURE'
			return_data['reason'] = str(e)
		
		return JsonResponse(return_data)


def runQueryOnData(query,data_frames):
	
	return_result = []
	for table in data_frames :
		ans = searchTable(table, query)
		if ans is not False:
			return_result.append(searchTable(table, query))

	return return_result
	


def searchTable(table, query):

	cols = table.columns
	year = str(query['year'])
	
	to_return = dict()
	try:
		
		select_row = table.loc[(table[cols[0]] == query['query'])]
		
		if year != '':	
			to_return = select_row[str(year)]
		else :
			to_return = select_row

		return to_return.to_json(orient='records')

	except Exception as E:
		return False

def generateCsvFromDataFrame(frame, name):
	# Generate Csv file 
	# Remove any rows where all values are NaN
	frame.dropna(axis=1, how='all')
	try:
		name = name.split(".")[0]
	except:
		pass
	location = name+'.csv'
	frame.to_csv(location)
	return location

def mergeFrames(frames):
	return pd.concat([frames[0], frames[1]], axis=1)

def renameTableCols(table):
	# Handling unnamed and . in column names
	cols = table.columns

	for col in cols :
		if re.match(r"Unnamed\b", col ) :
			table.rename(columns = {col : ""}, inplace=True)
		if col.split("."):
			table.rename(columns = {col:col.split(".")[0]}, inplace=True)

	return table

def cleanData(dataFile):
	# Split the dataframe to handle merged column
	# Store all columns of second table in separate dataframe
	# Merge while generating csv
	# Read Pdf as Dataframe
	
	original_dataframe = read_pdf(dataFile)
	# Split dataframe into two separate dataframes
	table1 = original_dataframe.iloc[:,:3]
	table2 = original_dataframe.iloc[:,3:]
	table1 = renameTableCols(table1)
	table2 = renameTableCols(table2)

	# clean column 3
	column3 = table1.iloc[:,2]
	column3_name = table1.columns[2]
	column3_newName = column3_name.split(" ",1)[0]
	table2_col_name = column3_name.split(" ", 1)[1]

	split_1 = []
	split_2 = []
	for row in column3:
		try:
			split_1.append(row.split(" ",1)[0])
		except:
			split_1.append("")
		try:
			split_2.append(row.split(" ",1)[1])
		except:
			split_2.append("")


	table2.insert(0, table2_col_name, split_2)
	
	table1.rename(columns={table1.columns[2]: table1.columns[2].split(" ",1)[0]},inplace=True)
	
	c = pd.Series()
	for index, row in enumerate(table1.iloc[:,2]):
		try:
			split_ans = row.split(" ",1)[0]
			c.set_value(index, float(split_ans))
		except:
			c.set_value(index, "")

	table1.iloc[:,2] = c

	
	# Return List of Dataframes
	tables = []
	tables.append(table1)

	tables.append(table2)
	return tables


