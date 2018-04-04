import uno
import unohelper
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
		self.locales = __import__("numbertext_locales").locales
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
				return Locale(a, "", "")
			else:
				return Locale(a[0], a[1], "")
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
	def getModule(self, Language, Country):
		global patterns
		module = Language + "_" + Country
		if not module in self.locales:
			module = Language
			if not module in self.locales:
				module = "en"
		if not module in patterns:
			try:
				d = __import__("numbertext_" + module)
			except:
				return "Error: missing language data"
			for i in d.dic:
				i += [ i[0][0] ==  "^", i[0][-1] == "$" ]
				if i[0][-1] != "$":
					i[0] += "$"
				i[0] = re.compile(i[0])
				if len(i) == 4:
					print "BE", i[1]
					i[1] = re.sub("\$([0-9])", r"$(\\\1)", i[1])
					print i[1]
			patterns[module] = d.dic
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
		mod = self.getModule(locale.Language, locale.Country)
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
		mod = self.getModule(loc.Language, loc.Country)
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
		n = convert_numbertext(num, True, True, conv)
	except:
		return "Conversion error"	
	if n == "":
		return num
	return n

def convert_numbertext(num, begin, end, conv):
	# strip leading zeros
	num = num.lstrip("0")
	if num == "":
		num = "0"
	# search the first matching pattern
	for i in conv:
		if len(i) == 4:
			if (begin == False and i[2]) or (end == False and i[3]):
				continue
		m = i[0].match(num)
		if (not m):
			continue
		# missing replacement
		if len(i) != 4:
			return m.group(0)
		sp = split(m.expand(i[1]), "$(")
		res = ""
		cut = 0
		lbegin = begin
		lend = False
		for j in range(0, len(sp)):
			if j == 0 and len(sp[j]) == 0:
				continue
			if j>0:
				parpos = sp[j].find(")")
				cut = parpos + 1
				if j == len(sp) - 1 and len(sp[j]) == cut:
					lend = end
				if sp[j][parpos+1:parpos+2] == "|":
					lend = True
					cut = cut + 1
				res = res + convert_numbertext(sp[j][0:parpos], lbegin, lend, conv)
			if j < len(sp) - 1 and sp[j][-1:] == "|":
				res = res + sp[j][cut:-1]
				lbegin = True
			else:
				res = res + sp[j][cut:]
				lbegin = False
		return res.strip()
	return ""
