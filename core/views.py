from django.shortcuts import render, HttpResponse
import json
from django.views import View
from tabula import read_pdf, convert_into

def home(request):
	return render(request, 'index.html', context = {})

class FileUploadClass(View):
	def get(self,request):
		pass

	def post(self,request):
		pass


def cleanData(dataFile):
	# Split the dataframe to handle merged column
	# Store all columns of second table in separate dataframe
	# Merge while generating csv
	# Read Pdf as Dataframe
	
	original_dataframe = read_pdf('BalSheet.pdf')
	# Split dataframe into two separate dataframes
	table1 = original_dataframe.iloc[:,:3]
	table2 = original_dataframe.iloc[:,3:]
	
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
			split_1_header
		except:
			split_1.append("")
		try:
			split_2.append(row.split(" ",1)[1])
		except:
			split_2.append("NaN")


	table2.insert(0, table2_col_name, split_2)
	print("Renaming Table 1")
	table1.rename(columns={table1.columns[2]: table1.columns[2].split(" ",1)[0]},inplace=True)
	print("Post Rename")
	print(table1.columns)

	tables = []
	tables.append(table1)
	tables.append(table2)
	return tables


