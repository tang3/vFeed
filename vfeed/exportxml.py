
from time import gmtime, strftime
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom

from . import vFeed
from . import config


'''
exportxml.py -  Class to export CVE into the vFeed structured XML format


'''

class vFeedXML(object):
    '''
    Produce the vFeed XML format
    The XML file is the flagship feature of the vFeed Concept

    '''
    def __init__(self, cveID):
        
        
        self.cve_url = config.gbVariables['cve_url']
        self.redhat_oval_url = config.gbVariables['redhat_oval_url']
        self.cwe_url = config.gbVariables['cwe_url']
        self.capec_url = config.gbVariables['capec_url']
        self.osvdb_url = config.gbVariables['osvdb_url']
        self.milw0rm_url = config.gbVariables['milw0rm_url']
        self.ms_bulletin_url  = config.gbVariables['ms_bulletin_url']
        self.ms_kb_url  = config.gbVariables['ms_kb_url']
        
        #Invoking the vFeed api with CVE object
        self.cveID = cveID.upper()
        self.vfeed = vFeed(cveID)
        
       # Calling all available methods
        self.cveInfo = self.vfeed.get_cve()
        self.cveRef = self.vfeed.get_refs()
        self.SCIP_id = self.vfeed.get_scip()
        self.CERTVN_id = self.vfeed.get_certvn()
        self.IAVM_id = self.vfeed.get_iavm()
        self.OSVDB_id = self.vfeed.get_osvdb()
        self.CPE_id = self.vfeed.get_cpe()
        self.CWE_id = self.vfeed.get_cwe()
        self.CAPEC_id = self.vfeed.get_capec()
        self.Risk = self.vfeed.get_risk()
        self.cvssScore = self.vfeed.get_cvss()
        self.MS_id = self.vfeed.get_ms()
        self.KB_id = self.vfeed.get_kb()
        self.AIXAPAR_id = self.vfeed.get_aixapar()
        self.REDHAT_id, self.BUGZILLA_id = self.vfeed.get_redhat()
        self.DEBIAN_id = self.vfeed.get_debian()
        self.FEDORA_id = self.vfeed.get_fedora()
        self.SUSE_id = self.vfeed.get_suse()
        self.GENTOO_id = self.vfeed.get_gentoo()
        self.UBUNTU_id = self.vfeed.get_ubuntu()
        self.CISCO_id = self.vfeed.get_cisco()
        self.MANDRIVA_id = self.vfeed.get_mandriva()
        self.VMWARE_id = self.vfeed.get_vmware()
        self.OVAL_id = self.vfeed.get_oval()
        self.NESSUS_id = self.vfeed.get_nessus()
        self.OPENVAS_id = self.vfeed.get_openvas()
        self.EDB_id = self.vfeed.get_edb()
        self.SAINT_id = self.vfeed.get_saint()
        self.MSF_id = self.vfeed.get_msf()
        self.MILWORM_id = self.vfeed.get_milw0rm()
        self.SNORT_id = self.vfeed.get_snort()
        self.SURICATA_id = self.vfeed.get_suricata()        
    
    def export(self):
        '''
            exporting data to the vFeed XML format
            Output : CVE_xxxx_xxx_.xml file
        '''
        # define id
        self.vfeedid = self.cveID.replace('self.cveID', 'vFeed')
        self.vfeedfile = self.cveID.replace('-', '_') + '.xml'
    
        # define generation time
        self.generated_on = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    
        # define the vFeed XML attributes
        self.root = Element('vFeed')
        self.root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        self.root.set('xmlns:meta', "http://www.toolswatch.org/vfeed/")
        self.root.set('xmlns', "http://www.toolswatch.org/vfeed/")
        self.root.set('xsi:schemaLocation', "http://www.toolswatch.org/vfeed/ http://www.toolswatch.org/vfeed/vFeed.xsd")
    
        self.root.append(Comment('#####################################'))
        self.root.append(Comment(config.product['__title__']))
        self.root.append(Comment('Generated by vFeedApi.py'))
    
        self.head = SubElement(self.root, 'release')
        self.project_name = SubElement(self.head, 'name')
        self.project_name.text = 'vFeed XML for %s' % self.cveID
    
        self.project_version = SubElement(self.head, 'version')
        self.project_version.text = config.product['__build__']
    
        self.project_author = SubElement(self.head, 'author')
        self.project_author.text = config.author['__name__']
    
        self.project_url = SubElement(self.head, 'url')
        self.project_url.text = config.author['__website__']
    
        self.date_generated = SubElement(self.head, 'date_generated')
        self.date_generated.text = self.generated_on
    
        # Exporting  Vulnerability Summary
    
        self.root.append(Comment('#####################################'))
        self.root.append(Comment('Entry ID'))
        self.entry_head = SubElement(self.root, 'entry',
                                     {'exported': self.vfeedfile,
                                      'id': self.vfeedid,
                                      })
    
        self.vul_summary_date = SubElement(self.entry_head, 'date',
                                           {'published': self.cveInfo['published'],
                                            'modified': self.cveInfo['modified'],
                                            })
    
        self.vul_summary = SubElement(self.entry_head, 'summary')
        self.vul_summary.text = self.cveInfo['summary']
        self.vul_summary_ref = SubElement(self.entry_head, 'cve_ref')
        self.vul_summary_ref.text = self.cve_url + self.cveID
    
        # Exporting references as they come from NVD XML
    
        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('Official References'))
        self.references_head = SubElement(self.entry_head, 'references')
    
        for i in range(0, len(self.cveRef)):
            self.source_head = SubElement(self.references_head, 'ref',
                                          {'url': self.cveRef[i]['link'],
                                           'source': self.cveRef[i]['id'],
                                           })


        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('vFeed Mapped References'))
        self.mappedrefs_head = SubElement(self.entry_head, 'crossReferences')


        # Exporting extra SCIP ref from Mapping
        
        for i in range(0, len(self.SCIP_id)):
            self.source_head = SubElement(self.mappedrefs_head, 'ref',
                                          {'url': self.SCIP_id[i]['link'],
                                           'id': self.SCIP_id[i]['id'],
                                           'source': "SCIP",
                                           })
 
         # Exporting extra CERT VN ref from Mapping
        
        for i in range(0, len(self.CERTVN_id)):
            self.source_head = SubElement(self.mappedrefs_head, 'ref',
                                          {'url': self.CERTVN_id[i]['link'],
                                           'id': self.CERTVN_id[i]['id'],
                                           'source': "CERT-VN",
                                           })
        
        # Exporting IAVM ref from Mapping

        for i in range(0, len(self.IAVM_id)):
            self.source_head = SubElement(self.mappedrefs_head, 'ref',
                                          {'vmskey': self.IAVM_id[i]['key'],
                                           'id': self.IAVM_id[i]['id'],
                                           'title': self.IAVM_id[i]['title'],
                                           'source': "DISA/IAVM",
                                           })

        # Exporting OSVDB ref from Mapping
        
        for i in range(0, len(self.OSVDB_id)):
            self.source_head = SubElement(self.mappedrefs_head, 'ref',
                                          {
                                           'id': self.OSVDB_id[i]['id'],
                                           'url': self.osvdb_url + self.OSVDB_id[i]['id'],
                                           'source': "OSVDB",
                                           })
            
        # Exporting Targets CPEs ids
    
        if self.CPE_id:
            self.entry_head.append(
                Comment('#####################################'))
            self.entry_head.append(
                Comment('Vulnerable Targets according to CPE'))
            self.vulnerabletargets_head = SubElement(
                self.entry_head, 'vulnerableTargets',
                {'totalCPE': str(len(self.CPE_id)), })
    
            for i in range(0, len(self.CPE_id)):
                self.cpe_head = SubElement(self.vulnerabletargets_head, 'cpe',
                                           {'id': self.CPE_id[i]['id'],
                                            })
    
        # Exporting Risk Scoring
    
        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('Risk Scoring Evaluation'))
        self.riskscoring_head = SubElement(self.entry_head, 'riskScoring')
    
        self.risk_head = SubElement(self.riskscoring_head, 'severityLevel',
                                    {'status': self.Risk['severitylevel'],
                                     })
    
        self.risk_head = SubElement(self.riskscoring_head, 'cvss',
                                    {
                                     'base': self.cvssScore['base'],
                                     'impact': self.cvssScore['impact'],
                                     'exploit': self.cvssScore['exploit'],
                                     })
    
        self.risk_head = SubElement(self.riskscoring_head, 'cvssVector',
                                    {'AV': self.cvssScore['access_vector'],
                                     'AC': self.cvssScore['access_complexity'],
                                     'Au': self.cvssScore['authentication'],
                                     'C': self.cvssScore['confidentiality_impact'],
                                     'I': self.cvssScore['integrity_impact'],
                                     'A': self.cvssScore['availability_impact'],
                                     })
    
        self.risk_head = SubElement(self.riskscoring_head, 'topVulnerable',
                                    {'status': str(self.Risk['topvulnerable']),
                                     })
    
        self.risk_head = SubElement(self.riskscoring_head, 'topAlert',
                                    {'status': str(self.Risk['topAlert']),
                                     })
    
        self.risk_head = SubElement(self.riskscoring_head, 'pciCompliance',
                                    {'status': self.Risk['pciCompliance'],
                                     })
    
    # Exporting Patch Management
    
        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('Patch Management'))
        self.patchmanagement_head = SubElement(
            self.entry_head, 'patchManagement')
    
        ## Exporting Microsoft MS Patches
    
        for i in range(0, len(self.MS_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.MS_id[i]['id'],
                                          'title': self.MS_id[i]['title'],
                                          'source': 'microsoft',
                                          'url' : self.ms_bulletin_url + self.MS_id[i]['id'],
                                          })
    
        ## Exporting Microsoft KB Patches
    
        for i in range(0, len(self.KB_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.KB_id[i]['id'],
                                          'title': self.KB_id[i]['title'],
                                          'source': 'microsoft KB',
                                          'url' : self.ms_kb_url + self.KB_id[i]['id'],
                                          })
    
        ## Exporting IBM AIXAPAR Patches
        for i in range(0, len(self.AIXAPAR_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.AIXAPAR_id[i]['id'],
                                          'source': 'IBM',
                                          })
    
        ## Exporting REDHAT Patches
    
        for i in range(0, len(self.REDHAT_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.REDHAT_id[i]['id'],
                                          'title': self.REDHAT_id[i]['title'],
                                          'source': 'REDHAT',
                                          })
    
        for i in range(0, len(self.BUGZILLA_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'date_issue': self.BUGZILLA_id[i]['date_issue'],
                                          'id': self.BUGZILLA_id[i]['id'],
                                          'title': self.BUGZILLA_id[i]['title'],
                                          'source': 'BUGZILLA',
                                          })
    
        ## Exporting SUSE Patches
        for i in range(0, len(self.SUSE_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.SUSE_id[i]['id'],
                                          'source': 'SUSE',
                                          })
    
        ## Exporting DEBIAN Patches
    
        for i in range(0, len(self.DEBIAN_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.DEBIAN_id[i]['id'],
                                          'source': 'DEBIAN',
                                          })
    
        ## Exporting MANDRIVA Patches
    
        for i in range(0, len(self.MANDRIVA_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.MANDRIVA_id[i]['id'],
                                          'source': 'MANDRIVA',
                                          })

        ## Exporting VMWARE Patches
    
        for i in range(0, len(self.VMWARE_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.VMWARE_id[i]['id'],
                                          'source': 'VMWARE',
                                          })


        ## Exporting CISCO Patches
    
        for i in range(0, len(self.CISCO_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.CISCO_id[i]['id'],
                                          'source': 'CISCO',
                                          })

        ## Exporting UBUNTU Patches
    
        for i in range(0, len(self.UBUNTU_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.UBUNTU_id[i]['id'],
                                          'source': 'UBUNTU',
                                          })
            
        ## Exporting GENTOO Patches
    
        for i in range(0, len(self.GENTOO_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.GENTOO_id[i]['id'],
                                          'source': 'GENTOO',
                                          })    
        
        ## Exporting FEDORA Patches
    
        for i in range(0, len(self.FEDORA_id)):
            self.patch_head = SubElement(self.patchmanagement_head, 'patch',
                                         {'id': self.FEDORA_id[i]['id'],
                                          'source': 'FEDORA',
                                          })  



        # Attack and Weaknesses Patterns
        
        if self.CWE_id:
    
            self.entry_head.append(
                Comment('#####################################'))
            self.entry_head.append(Comment('Attack and Weaknesses Categories. Useful when performing classification of threats'))
            self.attackclassification_head = SubElement(
                self.entry_head, 'attackPattern')
    
            for i in range(0, len(self.CWE_id)):
                self.cwe_id_url = self.CWE_id[i]['id'].split("CWE-")
                self.attackPattern_head = SubElement(
                    self.attackclassification_head, 'cwe',
                    {'standard': 'CWE - Common Weakness Enumeration',
                                                    'id': self.CWE_id[i]['id'],
                                                    'title': self.CWE_id[i]['title'],
                                                    'url' : self.cwe_url+self.cwe_id_url[1]
                     })
    
    
            for i in range(len(self.CWE_id), len(self.CAPEC_id) + len(self.CWE_id)):
                self.attackPattern_head = SubElement(
                    self.attackclassification_head, 'capec',
                    {'standard': 'CAPEC - Common Attack Pattern Enumeration and Classification',
                                                    'relatedCWE': self.CAPEC_id[i]['cwe'],
                                                    'id': self.CAPEC_id[i]['id'],
                                                    'url' : self.capec_url + self.CAPEC_id[i]['id']
                     })
    
    
        # Exporting Assessment, security tests and exploitation
        
        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('Assessment and security Tests. The IDs and source could be leveraged to test the vulnerability'))
        self.securitytest_head = SubElement(self.entry_head, 'assessment')
    
        ## Exporting OVAL ids
        for i in range(0, len(self.OVAL_id)):
            self.ovalChecks_head = SubElement(self.securitytest_head, 'check',
                                              {'type': 'Local Security Testing',
                                               'id': self.OVAL_id[i]['id'],
                                               'utility': "OVAL Interpreter",
                                               'file': self.OVAL_id[i]['file'],
                                               })
    
        for i in range(0, len(self.REDHAT_id)):
            self.ovalChecks_head = SubElement(self.securitytest_head, 'check',
                                              {'type': 'Local Security Testing',
                                               'id': self.REDHAT_id[i]['oval'],
                                               'utility': "OVAL Interpreter",
                                               'file': self.redhat_oval_url + self.REDHAT_id[i]['oval'].split('oval:com.redhat.rhsa:def:')[1] + '.xml',
                                               })
    
        ## Exporting Nessus attributes
        for i in range(0, len(self.NESSUS_id)):
            self.nessusChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Remote Security Testing',
                 'id': self.NESSUS_id[i]['id'],
                 'name': self.NESSUS_id[i]['name'],
                 'family': self.NESSUS_id[i]['family'],
                 'file': self.NESSUS_id[i]['file'],
                 'utility': "Nessus Vulnerability Scanner",
                 })
     
        ## Exporting OpenVAS attributes
        for i in range(0, len(self.OPENVAS_id)):
            self.openvasChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Remote Security Testing',
                 'id': self.OPENVAS_id[i]['id'],
                 'name': self.OPENVAS_id[i]['name'],
                 'family': self.OPENVAS_id[i]['family'],
                 'file': self.OPENVAS_id[i]['file'],
                 'utility': "OpenVAS Vulnerability Scanner",
                 })           
            
        ## Exporting EDB ids
        for i in range(0, len(self.EDB_id)):
            self.exploitChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Exploitation',
                 'utility': "exploit-db",
                 'id': self.EDB_id[i]['id'],
                 'file': self.EDB_id[i]['file'],
                 })
    
        ## Exporting Milw0rm ids 
        for i in range(0, len(self.MILWORM_id)):
            self.exploitChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Exploitation',
                 'utility': "milw0rm",
                 'id': self.MILWORM_id[i]['id'],
                 'file': self.milw0rm_url + self.MILWORM_id[i]['id'],
                 })


        ## Exporting SAINT ids
        for i in range(0, len(self.SAINT_id)):
            self.exploitChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Exploitation',
                 'utility': "saintExploit",
                 'id': self.SAINT_id[i]['id'],
                 'title': self.SAINT_id[i]['title'],
                 'file': self.SAINT_id[i]['file'],
                 })
    
        ## Exporting MSF - Metasploit ids
        for i in range(0, len(self.MSF_id)):
            self.exploitChecks_head = SubElement(
                self.securitytest_head, 'check',
                {'type': 'Exploitation',
                 'utility': "Metasploit",
                 'id': self.MSF_id[i]['id'],
                 'title': self.MSF_id[i]['title'],
                 'script': self.MSF_id[i]['file'],
                 })


        # Exporting Defense rules
        
        self.entry_head.append(
            Comment('#####################################'))
        self.entry_head.append(Comment('Defense and IDS rules. The IDs and source could be leveraged to deploy effective rules'))
        self.defense_head = SubElement(self.entry_head, 'defense')
    
            ## Exporting Snort Rules
        for i in range(0, len(self.SNORT_id)):
            self.idsRules_head = SubElement(
                self.defense_head, 'rule',
                {'type': 'Defense',
                 'utility': "Snort",
                 'id': self.SNORT_id[i]['id'],
                 'signature': self.SNORT_id[i]['signature'],
                 'classtype': self.SNORT_id[i]['classtype'],
                 })
 
             ## Exporting Suricata Rules
        for i in range(0, len(self.SURICATA_id)):
            self.idsRules_head = SubElement(
                self.defense_head, 'rule',
                {'type': 'Defense',
                 'utility': "Suricata",
                 'id': self.SURICATA_id[i]['id'],
                 'signature': self.SURICATA_id[i]['signature'],
                 'classtype': self.SURICATA_id[i]['classtype'],
                 })
  
 
                    
        self.xmlfile = open(self.vfeedfile, 'w+')
        print '[info] vFeed xml file %s exported for %s' % (self.vfeedfile, self.cveID)
        print >> self.xmlfile, self.prettify(self.root)
    
    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        This function found on internet.
        So thanks to its author whenever he is.
        """
        rough_string = ElementTree.tostring(elem, 'UTF-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
