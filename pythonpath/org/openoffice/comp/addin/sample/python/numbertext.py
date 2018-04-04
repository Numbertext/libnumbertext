import uno
import unohelper
import Soros
from org.openoffice.addin.sample import XNumberText
from com.sun.star.sheet import XAddIn
from com.sun.star.lang import XLocalizable, XServiceName, Locale

import re

from string import split

# constant
MINUS = "[-\u2212]"  # ASCII hyphen/minus or Unicode minus sign

# loaded patterns
patterns = {}

class NumberText( unohelper.Base, XNumberText, XAddIn, XServiceName ):

	def __init__(self, ctx):
		sLocaleData = "com.sun.star.i18n.LocaleData"
		self.LocaleData = ctx.ServiceManager.createInstance(sLocaleData)
		sProvider = "com.sun.star.configuration.ConfigurationProvider"
		sAccess   = "com.sun.star.configuration.ConfigurationAccess"
		aConfigProvider = ctx.ServiceManager.createInstance(sProvider)
		prop = uno.createUnoStruct('com.sun.star.beans.PropertyValue')
		prop.Name = "nodepath"
		prop.Value = "/org.openoffice.Setup/L10N"
		self.aSettings = aConfigProvider.createInstanceWithArguments(sAccess,(prop,))
		self.uilocale = self.aSettings.getByName("ooLocale")
		self.titles = __import__("numbertext_titles").titles
		self.locales = __import__("numbertext_locales").__doc__.strip().split("\n")
		self.decplaces = __import__("numbertextplaces").decplaces
		self.locale = Locale("en", "US", "")

	# XLocalizable method implementations
	def setLocale( self, locale ):
		self.locale = locale

	def getLocale( self ):
		return self.locale

	# XServiceName method implementations
	def getServiceName(self):
		return "org.openoffice.addin.sample.python.numbertext.NumberText"

	def queryLocale(self, prop, loc):
		if loc != None:
			a = split(loc, "-")
			if len(a) == 1:
				return Locale(a[0], "", "")
			if len(a) == 2:
				return Locale(a[0], a[1], "")
			else:
				return Locale(a[0], a[1], a[2])
		locale = prop.getPropertyValue("CharLocaleAsian")
		if locale != None and locale.Language != "zxx":
			return locale
		locale = prop.getPropertyValue("CharLocaleComplex")
		if locale != None and locale.Language != "zxx":
				return locale
		locale = prop.getPropertyValue("CharLocale")
		if locale != None and locale.Language != "zxx":
			return locale
		return Locale("en", "US", "")

	# set module name for importing locale data
	def getModule(self, Language, Country, Variant):
		global patterns
		if Country == "":
		    module = Language
		if Variant == "":
		    module = Language + "_" + Country
		else:
		    module = Language + "_" + Country + "_" + Variant
		if not module in self.locales:
			module = Language
			if not module in self.locales:
				module = "en"
		if not module in patterns:
			try:
				d = __import__("numbertext_" + module)
			except:
				return "Error: missing language data"
			patterns[module] = Soros.compile(d.__doc__)
		return module

	def getCurrency(self, locale):
		allcurr = self.LocaleData.getAllCurrencies(locale)
		if allcurr != None:
			struct = uno.createUnoStruct("com.sun.star.i18n.Currency")
			for struct in allcurr:
				if struct.Default:
					return struct
		return None

	# XNumberText method implementations
	def moneytext(self, prop, num, curr, loc):
		global patterns
		num = num.strip()
		if not re.compile(MINUS + "?[0-9][0-9]*([.,][0-9][0-9]*)?$").match(num):
			return num
		locale = self.queryLocale(prop, loc)
		mod = self.getModule(locale.Language, locale.Country, locale.Variant)
		decimalplaces = 2;
		outcurr = ""
		if curr == None:
			currency = self.getCurrency(locale)
			decimalplaces = currency.DecimalPlaces
			outcurr = currency.ID + " "
		elif curr in self.decplaces:
			decimalplaces = self.decplaces[curr]
			outcurr = curr + " "
		if num.rfind(".") > -1 or num.rfind(",") > -1:
			num = round(float(num.replace(",",".")), decimalplaces)
			if decimalplaces == 0:
				num = str(int(num))
			else:
				# add missing 0(s) for decimalplaces digit
				num = str(num)
				dig = len(num[num.rfind(".")+1:])
				num = num + "".zfill(decimalplaces - dig)
		return get_numbertext(outcurr + num, patterns[mod])

	def numbertext(self, prop, num, loc):
		global patterns
		num = num.strip()
		if not re.compile(MINUS + "?[0-9][0-9]*([.,][0-9][0-9]*)?$").match(num):
			return num	
		if num.rfind(".") > -1 or num.rfind(",") > -1:
			num = str(round(float(num.replace(",",".")), 2))
			dig = num[num.rfind(".")+1:]
			num = num + "".zfill(2 - len(dig))
		# query document language
		loc = self.queryLocale(prop, loc)
		mod = self.getModule(loc.Language, loc.Country, loc.Variant)
		return get_numbertext(num, patterns[mod])

	def getTitle(self, par, loc):
		try:
			return self.titles[par + "-" + loc.Language + "_" + loc.Country]
		except:
			try:
				return self.titles[par + "-" + loc.Language]
			except:
				return self.titles[par + "-en"]

	# XAddIn method implementations
	def getProgrammaticFuntionName(self, aDisplayName):
		return aDisplayName

	def getDisplayFunctionName(self, aProgrammaticName):
		return aProgrammaticName

	def getFunctionDescription(self, aProgrammaticName):
		return self.getTitle("Desc-", self.uilocale)
		return self.getTitle("Desc-" + aProgrammaticName, self.uilocale)

	def getDisplayArgumentName(self, aProgrammaticFunctionName, nArgument):
		return self.getTitle("Arg" + str(nArgument), self.uilocale)
		return self.getTitle("Arg" + str(nArgument) + "-" + aProgrammaticFunctionName, self.uilocale)

	def getArgumentDescription(self, aProgrammaticFunctionName, nArgument):
		return self.getTitle("Arg" + str(nArgument) + "Desc", self.uilocale)
		return self.getTitle("Arg" + str(nArgument) + "Desc-" + aProgrammaticFunctionName, self.uilocale)

	def getProgrammaticCategoryName(self, aProgrammaticFunctionName):
	        return "Add-In"

	def getDisplayCategoryName(self, aProgrammaticFunctionName):
		return "Add-In"

def get_numbertext(num, conv):
	try:
		n = conv.run(num)
	except:
		return "Conversion error"	
	if n == "":
		return num
	return n
