import uno
import unohelper

def createInstance( ctx ):
    # NumberText uses a new type, importing it at the top of this file
    # leads to a failure during adding the extension to OOo 
    import org.Numbertext
    return org.Numbertext.NUMBERTEXT( ctx )

# pythonloader looks for a static g_ImplementationHelper variable
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation( \
        createInstance,"org.numbertext",
        ("com.sun.star.sheet.AddIn",),)
