# Script to cleanup the static page generated by respec to produce a valid WD.

import re

# Remove attributes added by respec.
stripstr = [
	# data-bug-xxx is for the bug-assist.js script..
	' data-bug-product="WebAppsWG" data-bug-component="DOM3 Events" typeof="bibo:Document w3p:WD" about="" property="dcterms:language" content="en" prefix="bibo: http://purl.org/ontology/bibo/ w3p: http://www.w3.org/2001/02pd/rec54#"',
	' property="dcterms:title"',
	' property="dcterms:issued" datatype="xsd:dateTime" content="2013-11-05T08:00:00.000Z"',
 	' property="dcterms:issued" datatype="xsd:dateTime" content="2014-09-25T07:00:00.000Z"',
 	' rel="bibo:editor" inlist=""',
	' typeof="foaf:Person"',
	' property="foaf:name"',
	' content="Gary Kacmarcik"',
	' content="Travis Leithead"',
	' property="dcterms:abstract" datatype=""',
	' typeof="bibo:Chapter" resource="#[A-Za-z0-9_-]+" rel="bibo:Chapter"',
	' aria-label="False"',
	' aria-label="True"',
	' about=""',
	# More bug-assist.js stuff to remove for WD.
	'<script src="bug-assist.js" type="text/javascript"></script>',
	'<form action="http://www.w3.org/Bugs/Public/enter_bug.cgi" target="_blank" style="position: fixed; padding: 5px; top: 1em; right: 2em; font-family: sans-serif; font-size: 0.8em; background-color: rgb\(255, 255, 255\); border: 1px solid rgb\(255, 0, 0\);">Select text and <input type="submit" accesskey="f" value="file a bug" style="display: block;" /><input type="hidden" name="comment" value="" /><input type="hidden" name="product" value="WebAppsWG" /><input type="hidden" name="component" value="DOM3 Events" /></form>',
	# Respec's TOC generator adds these turds (which the validator complains about).
	'<ul class="toc"></ul>',
]

def strip(line):
	for str in stripstr:
		pattern = '^(.*)'
		pattern += str
		pattern += '(.*)$'
		while True:
			m = re.match(pattern, line)
			if not m:
				break
			line = m.group(1) + m.group(2) + '\n'
	return line

# Fixup refs to WebIDL consts by adding the interface name prefix.
widlstr = [
	['Event-', 'NONE"'],
	['Event-', 'CAPTURING_PHASE"'],
	['Event-', 'AT_TARGET"'],
	['Event-', 'BUBBLING_PHASE"'],
	['WheelEvent-', 'DOM_DELTA_PIXEL"'],
	['WheelEvent-', 'DOM_DELTA_LINE"'],
	['WheelEvent-', 'DOM_DELTA_PAGE"'],
	['KeyboardEvent-', 'DOM_KEY_LOCATION_STANDARD"'],
	['KeyboardEvent-', 'DOM_KEY_LOCATION_LEFT"'],
	['KeyboardEvent-', 'DOM_KEY_LOCATION_RIGHT"'],
	['KeyboardEvent-', 'DOM_KEY_LOCATION_NUMPAD"'],
]

def widl(line):
	for str in widlstr:
		pattern = '^(.*href="#)('
		pattern += str[1]
		pattern += '.*)$'
		m = re.match(pattern, line)
		if m:
			line = m.group(1) + 'widl-' + str[0] + m.group(2) + '\n'
	return line

# Cleanup the unwieldy method names by removing the param list.
paramstr = [
	['Event-stopPropagation', '-void'],
	['Event-preventDefault', '-void'],
	['Event-initEvent', '-void-DOMString-eventTypeArg-boolean-bubblesArg-boolean-cancelableArg'],
	['Event-stopImmediatePropagation', '-void'],
	['EventTarget-addEventListener', '-void-DOMString-type-EventListener-listener-boolean-useCapture'],
	['EventTarget-removeEventListener', '-void-DOMString-type-EventListener-listener-boolean-useCapture'],
	['EventTarget-dispatchEvent', '-boolean-Event-event'],
	['EventListener-handleEvent', '-void-Event-event'],
	['DocumentEvent-createEvent', '-Event-DOMString-eventInterface'],
	['MouseEvent-getModifierState', '-boolean-DOMString-keyArg'],
	['KeyboardEvent-getModifierState', '-boolean-DOMString-keyArg'],
	['CustomEvent-initCustomEvent', '-void-DOMString-typeArg-boolean-bubblesArg-boolean-cancelableArg-any-detailArg'],
	['UIEvent-initUIEvent', '-void-DOMString-typeArg-boolean-bubblesArg-boolean-cancelableArg-AbstractView-viewArg-long-detailArg'],
	['FocusEvent-initFocusEvent', '-void-DOMString-typeArg-boolean-bubblesArg-boolean-cancelableArg-AbstractView-viewArg-long-detailArg-EventTarget-relatedTargetArg'],
	['MouseEvent-initMouseEvent', '-void-DOMString-typeArg-boolean-bubblesArg-boolean-cancelableArg-AbstractView-viewArg-long-detailArg-long-screenXArg-long-screenYArg-long-clientXArg-long-clientYArg-boolean-ctrlKeyArg-boolean-altKeyArg-boolean-shiftKeyArg-boolean-metaKeyArg-unsigned-short-buttonArg-EventTarget-relatedTargetArg'],
	['WheelEvent-initWheelEvent', '-void-DOMString-typeArg-boolean-bubblesArg-boolean-cancelableArg-AbstractView-viewArg-long-detailArg-long-screenXArg-long-screenYArg-long-clientXArg-long-clientYArg-unsigned-short-buttonArg-EventTarget-relatedTargetArg-DOMString-modifiersListArg-double-deltaXArg-double-deltaYArg-double-deltaZArg-unsigned-long-deltaMode'],
]

def params(line):
	for str in paramstr:
		pattern = '^(.*#widl-'
		pattern += str[0]
		pattern += ")"
		pattern += str[1]
		pattern += '(.*)$'
		m = re.match(pattern, line)
		if m:
			line = m.group(1) + m.group(2) + '\n'
	return line

# Re-add the reference links which are mysteriously removed.
refstr = [
	['ref-BCP-47', 'BCP-47'],
	['references-charmod', 'CharMod'],
	['references-DOMCore', 'DOM3 Core'],
	['references-DOM2Events', 'DOM2 Events'],
	['references-ECMAScript', 'ECMAScript'],
	['references-HTML5', 'HTML5'],
	['references-Java', 'Java'],
	['RFC2119', 'RFC2119'],
	['references-UnicodeNormalization', 'UAX #15'],
	['references-UIEvents', 'UIEvents'],
	['references-Unicode', 'Unicode'],
	['references-WebIDL', 'WEB IDL'],
	['references-Namespaces10', 'XML Namespaces 1.0'],
	['ref-ARIA', 'ARIA'],
	['ref-xforms', 'XFORMS'],
	['references-CSS2', 'CSS2.1'],
	['references-DASE', 'DASE'],
	['references-DOMLS', 'DOM3 Load and Save'],
	['references-DOMRange', 'DOM2 Range'],
	['references-DOM4', 'DOM4'],
	['references-DWW95', 'DWW95'],
	['references-HTML40', 'HTML 4.01'],
	['references-HTMLEd', 'HTML Editing'],
	['references-ISO-9995-2-3', 'ISO9995-2/3'],
	['references-ISO-9995-8', 'ISO9995-8'],
	['references-KeyEvent', 'KeyEvent for Java'],
	['references-Keys', 'Keys enumeration for .Net'],
	['references-KeyProps', 'KeyProps'],
	['references-OCAP', 'OCAP'],
	['references-pcre', 'PCRE'],
	['ref-rfc20', 'RFC20'],
	#['ref-US-ASCII', 'US-<acronym title="American Standard Code for Information Interchange">ASCII</acronym>'],
	['references-UAAG2', 'UAAG 2.0'],
	['references-WEB4CE', 'WEB4CE'],
	['ref-WIN1252', 'WIN1252'],
	['references-XML', 'XML 1.0'],
]

def refs(line):
	for str in refstr:
		pattern = '^(.*<dt><strong>\[)'
		pattern += str[1]
		pattern += '(\].*)$'
		m = re.match(pattern, line)
		if m:
			line = m.group(1) + '<a id="' + str[0] + '">' + str[1] + '</a>' + m.group(2) + '\n'
	return line

# Don't use acronym inside reference name.
replacestr = [
	['\[US-<acronym title="American Standard Code for Information Interchange">ASCII</acronym>\]', '[US-ASCII]'],
	['id="idl-def-KeyboardEventInit">partial dictionary', 'id="idl-def-KeyboardEventInit-extra">partial dictionary'],
	['<dl class="methods"><dt id="widl-CustomEvent-initCustomEvent"><code>initCustomEvent</code>', '<dl class="methods"><dt id="widl-CustomEvent-initCustomEvent-extra"><code>initCustomEvent</code>'],
]

def replace(line):
	for str in replacestr:
		pattern = '^(.*)'
		pattern += str[0]
		pattern += '(.*)$'
		m = re.match(pattern, line)
		if m:
			line = m.group(1) + str[1] + m.group(2) + '\n'
	return line

def process(fout, index, line):
	line = strip(line)
	line = widl(line)
	line = params(line)
	line = refs(line)
	line = replace(line)
	fout.write(line)

# Overview.xhtml is the static file exported by respec.
with open('Overview.xhtml', 'r') as fin:
	with open('WD-DOM3-Events.html', 'w') as fout:
		index = 0
		for line in fin:
			process(fout, index, line)
			index += 1
