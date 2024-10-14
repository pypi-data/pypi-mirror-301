import math
import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta,date
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.DatePicker import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.PunchCard.CalcTimePad import *

import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *

class RosterUi:
	def __init__(self):
		fieldname='Menu'
		mode='Roster'
		h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
		menutext=f'''
{Fore.cyan}'ap','ad person','add person','add personnel','ad personnl' {Fore.light_red}-{Fore.orange_red_1} add a person to Roster table, checking to ensure that name is not duplicated before adding{Style.reset}
{Fore.cyan}'ad','ad dpt','add department','add dpt','addpt' {Fore.light_red}-{Fore.orange_red_1} add a department to tables{Style.reset}
{Fore.cyan}'ars','ad roster shift','add roster shift','adrstrshft' {Fore.light_red}-{Fore.orange_red_1} using Roster and Departments tables, update the RosterShift table with available shift data{Style.reset}
{Fore.cyan}'lurs','dat a phat llama to be puckin tday','lookup rostershift','whos working','twirk it bitch','work dat pole','trex wrote this','donkeys eating it','why trexes always angry','their arms are too short','to either [fli/jer]ck it' {Fore.light_red}-{Fore.orange_red_1} search the RosterShift for who's working today and print as list{Style.reset}
{Fore.cyan}'search','s','still a virgin','dont worry itll be over soon','whats in that corn field?','children!' {Fore.light_red}-{Fore.orange_red_1} search for a person/date/department and print as a list{Style.reset}
		'''
		while True:
			try:
				cmd=Prompt.__init2__(self,func=FormBuilderMkText,ptext=f"{h}Do what?",helpText=menutext,data="string")
				if cmd in [None,]:
					return
				elif cmd.lower() in ['d',]:
					print(menutext)
				elif cmd.lower() in ['ap','ad person','add person','add personnel','ad personnl']:
					pass
				elif cmd.lower() in ['ad','ad dpt','add department','add dpt','addpt']:
					pass
				elif cmd.lower() in ['ars','ad roster shift','add roster shift','adrstrshft']:
					pass
				elif cmd.lower() in ['lurs','dat a phat llama to be puckin tday','lookup rostershift','whos working','twirk it bitch','work dat pole','trex wrote this','donkeys eating it','why trexes always angry','their arms are too short','to either [fli/jer]ck it']:
					pass
				elif cmd.lower() in ['search','s','still a virgin','dont worry itll be over soon','whats in that corn field?','children!']:
					pass
				else:
					print(menutext)
			except Exception as e:
				print(e)