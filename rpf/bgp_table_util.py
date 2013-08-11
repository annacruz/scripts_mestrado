#!/usr/env python
import re

class Util:

  def convert_to_dict(self, info, host):
    ## TODO:
    ##   Test with another BGP table with network like xxx.xx.xx.x/16  => Maybe some little adjust in regexp
    """ Gets bgp table and parse to a dictionary  """

    keys = ["Type", "Network", "Next_Hop", "Metric", "LocPrf", "Weight", "Path"] # These keys are used only to mount the final dictionary
    crude = ''.join(info)
    lines = crude.split('\n\n')[1].split('\n')
    header = lines.pop(0) # Removing the useless header
    header = header.replace('Next Hop', 'Next_Hop') # Go Horse!

    header = re.split(r' [a-zA-Z]', header) # Spliting the header selecting the first string after a space
    header[0] = header[0][0:-1] # First column only lose one char so remove another one here
    output = []
    regex = []

    # Creating the regexp to break the BGP table from header column size
    for column in header:
      if column == header[-1]:
        regex.append("(.+)")
        break
      regex.append("(.{%s})" %str(len(column)+2))

    regex = ''.join(regex) # As regex must be an string, convert the array.

    # From the regex break the line into pieces and then create the final dict
    for line in lines:
      values = re.findall(regex, line)
      values = [x.strip() for x in values[0]]
      output.append(dict(zip(keys, values)))

    # If no network is inputed, then the network is the previous value
    for index in range(len(output)):
      if output[index].get('Network') == '':
        output[index]['Network'] = output[index-1]['Network']
      output[index]['Router_Host'] = host

    return output

  def getting_interface(self, route_information):
    """ Gets the show ip route information and return a dict with network and interface """
    clear_result = filter(lambda x: 'eth' in x,route_information) # This line filter the position in route_information that contains eth information to be returned
    interface = clear_result[0].split('eth')[1]

    return interface
