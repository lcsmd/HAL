# Document

# XML

|  [![Top](top.gif)](titlepage.htm)  [![Previous](previous.gif)](without.htm)
[![Next](next.gif)](qmbasic.htm)  
---|---  
  The XML keyword causes the query processor to produce output in XML format.     Format   XML {ELEMENTS} {WITH.DTD | DTD.ONLY} {WITH.SCHEMA | SCHEMA.ONLY}   where   | ELEMENTS| produces a report in which each field or value is output as a separate XML element.  
---|---  
  


WITH.DTD| includes the Document Type Definition in the output.  
---|---  
  


DTD.ONLY| produces a report containing only the Document Type Definition.  
---|---  
  


WITH.SCHEMA| includes the schema in the output.  
---|---  
  


SCHEMA.ONLY| produces a report containing only the schema.  
---|---  
  




An XML mode report command may not include breakpoints or arithmetic field
qualifiers. Use of the PAN, DET.SUP, HEADING or FOOTING options will be
ignored.



The tag name applied to top level (record) items is the file name.  For
associated multivalue items, the association name is used as the tag. For non-
associated multivalued items, the tag is the name of the item with a _MV
suffix.





Example



The following example is based on QM's demonstration sales database as created
using the [SETUP.DEMO](setup_demo.htm) command but without creating any of the
additional items developed from material in the Teach Yourself OpenQM training
package.



LIST SALES XML

<?xml version="1.0" encoding="UTF-8"?>

<ROOT>

<SALES SALE = "12140" DATE = "14 Oct 07" CUST = "1056">

 <LINE ITEM = "003" QTY = "1" PRICE = "1.70"/>

 <LINE ITEM = "122" QTY = "3" PRICE = "44.50"/>

 <LINE ITEM = "234" QTY = "2" PRICE = "26.00"/>

 <LINE ITEM = "121" QTY = "6" PRICE = "38.00"/>

</SALES>

<SALES SALE = "12347" DATE = "07 Feb 08" CUST = "1087">

 <LINE ITEM = "004" QTY = "1" PRICE = "1.70"/>

 <LINE ITEM = "131" QTY = "3" PRICE = "6.98"/>

 <LINE ITEM = "232" QTY = "1" PRICE = "19.85"/>

 <LINE ITEM = "055" QTY = "1" PRICE = "2.87"/>

 <LINE ITEM = "021" QTY = "6" PRICE = "0.25"/>

</SALES>

</ROOT>

etc



With the ELEMENTS keyword, the first record from this example becomes

<?xml version="1.0" encoding="UTF-8"?>

<ROOT>

<SALES>

<SALE>12140</SALE>

<DATE>14 Oct 07</DATE>

<CUST>1056</CUST>

 <LINE>

   <ITEM>003</ITEM>

   <QTY>1</QTY>

   <PRICE>1.70</PRICE>

 </LINE>

 <LINE>

   <ITEM>122</ITEM>

   <QTY>3</QTY>

   <PRICE>44.50</PRICE>

 </LINE>

 <LINE>

   <ITEM>234</ITEM>

   <QTY>2</QTY>

   <PRICE>26.00</PRICE>

 </LINE>

 <LINE>

   <ITEM>121</ITEM>

   <QTY>6</QTY>

   <PRICE>38.00</PRICE>

 </LINE>

</SALES>

</ROOT>

