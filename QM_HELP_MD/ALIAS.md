# Document

# ALIAS

|  [![Top](top.gif)](titlepage.htm)
[![Previous](previous.gif)](admin_user.htm)
[![Next](next.gif)](analyse_file.htm)  
---|---  
  The ALIAS command creates a temporary alias for a command.     Format   | ALIAS command  target| Create an alias  
---|---  
  
ALIAS command| Remove an alias  
---|---  
  
ALIAS| List all defined aliases  
---|---  
  


where



command| is the alias name.  
---|---  
  


target| is the command to which the alias applies. If this contains spaces, it
must be quoted.  
---|---  
  




The ALIAS command creates an alternative name by which a command can be
referenced such that command becomes a synonym for target. It provides a
simple mechanism by which standard commands can be linked to alternative VOC
entries as a means of providing improved compatibility with other multivalue
database products. For example, the [COPY](copy.htm) command could be linked
to the Pick style variant named [COPYP](copyp.htm) by executing

ALIAS COPY COPYP

This change affects only the current process and does not modify the VOC.
Typically, ALIAS commands would be executed from the
[LOGIN](command_scripts.htm) paragraph. To maintain system security, LOGIN
cannot itself be aliased.



The second form of the ALIAS command removes a previously defined alias for
command.



The third form lists all currently defined aliases.

