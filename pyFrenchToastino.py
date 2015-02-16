import serial
import time
import openanything
import xml.etree.ElementTree as ETree

useragent = 'pyFrenchToastArduino/1.0'
xml_source = 'http://www.universalhub.com/toast.xml'
server_response = { 'etag' : None, 'lastmodified' : None, 'data': None }


def processXML(xml):
  tree = ETree.fromstring(xml)
  status = tree.find('status')

  if status != None:
    #print status.text
    # return first character, uppercase
    return status.text[:1].upper()
  # default case: return error code
  return 'X'


def retrieveXML():
  global xml_source
  global server_response
  # Check for updates to XML.  If HTTP 200 is recieved, process the response
  latest_server_response = openanything.fetch(xml_source, server_response['etag'],
    server_response['lastmodified'], useragent)
  #print(latest_server_response)

  # Handle (most common) case, where the XML is unchanged
  if latest_server_response['status'] == 304:
    # We continure to return the last valid data, since nothing has changed
    #print('XML Unchanged')
    return server_response['data']

  # Handle normal response
  if latest_server_response['status'] in {200, 302}:
    # Store this as a the current, valid, updated response
    server_response = latest_server_response
    #print(server_response['data'])
    return server_response['data']

  # if this is a permenant redirect, also update the URI for future calls
  if latest_server_response['status'] == 301:
    xml_source = params['url']
    server_response = latest_server_response
    return server_response['data']
  
  # If we got some sort of other response
  return None

# Init Serial Port
ser = serial.Serial('COM7', 9600, timeout=15)


# Loop forever
while 1:
  try:
    current_xml = retrieveXML()
    response_code =  processXML(current_xml)
    print "Sending to Arduino: " + response_code
    # Write to arduino on serial port
    ser.write(response_code)


    # Wait for response (max of serial timeout value), and print any reply we get from the arduino
    serial_reply = ser.readline() 
    print "Recieved from Arduino: " + serial_reply.decode('ascii')

    # Sleep for 15 minutes (then start over)
    time.sleep(60 * 5)
  except Exception as e:
    print "Exception: " + e
    time.sleep(60)



