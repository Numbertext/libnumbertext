import uno
import unohelper

def createInstance( ctx ):
    # NumberName uses a new type, importing it at the top of this file
    # leads to a failure during adding the extension to OOo 
    import org.openoffice.comp.addin.sample.python.numbertext
    return org.openoffice.comp.addin.sample.python.numbertext.NumberText( ctx )

# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
	createInstance,"org.openoffice.comp.addin.sample.python.NumberText",
        ("com.sun.star.sheet.AddIn",),)
