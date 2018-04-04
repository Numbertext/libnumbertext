import uno
import unohelper
import re

from org.numbertext import XNumberText
from com.sun.star.lang import Locale

from org.Numbertext import Soros
from org.Numbertext.locales import locales
from org.Numbertext.places import places

from string import split

# constant
MINUS = "[-\u2212]"  # ASCII hyphen/minus or Unicode minus sign

langname = {}
# loaded patterns
patterns = {}


class NUMBERTEXT( unohelper.Base, XNumberText):

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
		self.locale = Locale("en", "US", "")
		for i in locales:
		    langname[i.split("_")[0]] = i

	def queryLocale(self, prop, loc):
		if loc != None:
			a = split(loc, "-")
			if len(a) == 1:
				return Locale(a[0], "", "")
			if len(a) == 2:
				return Locale(a[0], a[1], "")
			else:
				return Locale(a[0], a[1], a[2])
#		locale = prop.getPropertyValue("CharLocaleAsian")
#		if locale != None and locale.Language != "zxx":
#			return locale
#		locale = prop.getPropertyValue("CharLocaleComplex")
#		if locale != None and locale.Language != "zxx":
#				return locale
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
		    if not module in locales:
			module = Language + "_" + Country
		if not module in locales:
			module = Language
			if not module in locales:
			    try:
				module = langname[Language]
			    except:
				module = "en_US"
		if not module in patterns:
			try:
				d = __import__("numbertext_" + module)
			except:
				return "Error: missing language data (" + module + ")"
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
		# query document language
		locale = self.queryLocale(prop, loc)
		mod = self.getModule(locale.Language, locale.Country, locale.Variant)
		decimalplaces = 2;
		if curr == None:
			currency = self.getCurrency(locale)
			decimalplaces = currency.DecimalPlaces
			outcurr = currency.ID + " "
		else:
			outcurr = curr + " "
			if curr in places:
				decimalplaces = places[curr]
		if num.rfind(".") > -1 or num.rfind(",") > -1:
			num = float(num.replace(",","."))
			if (type(decimalplaces) == type(0.1)):
				pl = 10**decimalplaces;
				num = str(round(num * pl) / pl)
			else:
				num = str(round(num, decimalplaces))
		return get_numbertext(outcurr + num, patterns[mod])

	def numbertext(self, prop, num, loc):
		global patterns
		# query document language
		loc = self.queryLocale(prop, loc)
		mod = self.getModule(loc.Language, loc.Country, loc.Variant)
		return get_numbertext(num.strip(), patterns[mod])

def get_numbertext(num, conv):
	try:
		n = conv.run(num)
	except:
		return "Conversion error"
	if n == "":
		return num
	return n
