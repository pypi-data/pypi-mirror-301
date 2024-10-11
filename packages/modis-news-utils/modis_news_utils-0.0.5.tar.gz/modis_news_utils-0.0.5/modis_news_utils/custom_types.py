from typing import Union

UtilName = str
UtilMethodName = str
URL = str
HTML = str
AttributeName = str
Text = str
XPath = str
Probability = float
ParamName = str
LanguageCode = str

UtilsInfo = dict[UtilName, dict[ParamName, Union[URL, list[UtilMethodName]]]]
AvailableMethods = dict[UtilName, list[UtilMethodName]]

NewsAttributeNode = dict[ParamName, Union[Text, XPath, Probability]]
NewsAttributes = dict[AttributeName, list[NewsAttributeNode]]

SectionItemAttributeNode = dict[ParamName, Union[Text, XPath]]
SectionItemAttribute = list[SectionItemAttributeNode]
SectionItem = dict[ParamName, Union[XPath, SectionItemAttribute]]
