from ..takeoff_test import TakeOffTest
import re

class AristaBGPConnTest(TakeOffTest):

  def test(self):

   # res = connection_object.cli('show bgp summary')
    with open('BGP.txt','r') as foo:
      res = foo.read()

    # Program for checking the status of the BGP neighbor from the "show ip bgp summary" command.
    # Note: Enter the correct number of BGP neighbors. Entering more number than acual produces random result.
    #  pfile_r=pfile.read()
    #  pfile_l=pfile_r.split()
    #  index_version=pfile_l.index("State/PfxRcd")
    #  iteration=int(raw_input("Enter the number of neighbours"))
    neighbor_line_re = re.compile('(^\d+\.\d+\.\d+\.\d+).*')

    neighbor_lines = []
    #for line in res['results'][0].split('\n'):
    for line in res.split('\n'):
      if neighbor_line_re.match(line):
        neighbor_lines.append(line)

    for neighbor in neighbor_lines:
      neighbor_line_split = neighbor.split()
      #print "DEBUG: %s" % neighbor_line_split
      neighbor_ip = neighbor_line_split[0]
      neighbor_state = neighbor_line_split[-1]
      # Then test the neighbor
      self.nei_fun(neighbor_ip, neighbor_state)

    if len(self.error) == 0:
      self._handle_success()


  def nei_fun(self, nei_addr, nei_state):
    #print nei, nei_name
    #print type(nei), type(nei_name)
    #print "DEBUG: %s %s" % (nei_addr, nei_state)

    if nei_state.isdigit():
      self.output.append("Peer %s is up, %s prefixes" % (nei_addr, nei_state))
    else:
      self.error.append('Peer %s not up, in state %s' % (nei_addr, nei_state))

    # except ValueError as e:
    # print "BGP peering with", nei_name, "is Down"

    # for neighbor in range(iteration):
    #  nei=pfile_l[index_version+10*neighbor]
    #  temp=index_version+10*neighbor
    #  nei_name=pfile_l[temp+1]
    #  #print nei, temp, nei_name
    #  #print type(nei), type(temp), type(nei_name)
    #  nei_fun(nei, nei_name)
