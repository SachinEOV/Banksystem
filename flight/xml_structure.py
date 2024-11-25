EXPECTED_XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<fareRequest da="true">
  <vcrs>
    <vcr>BA</vcr>
  </vcrs>
  <fareTypes xmlns="http://ypsilon.net/shared"/>
  <tourOps/>
  <flights>
    <flight depApt="JFK" dstApt="LAX" depDate="2024-12-01"/>
    <flight depApt="LAX" dstApt="JFK" depDate="2024-12-10"/>
  </flights>
  <paxes>
    <pax surname="Doe" firstname="John" dob="1985-05-15" gender="M"/>
    <pax surname="Smith" firstname="Jane" dob="1990-07-20" gender="F"/>
  </paxes>
  <paxTypes/>
  <options>
    <limit>20</limit>
    <offset>0</offset>
    <waitOnList>
      <waitOn>ALL</waitOn>
    </waitOnList>
  </options>
  <coses>
    <cos>E</cos>
  </coses>
</fareRequest>
"""
