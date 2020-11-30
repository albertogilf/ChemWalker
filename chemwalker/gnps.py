
import pandas as pd
import requests
import io
import xmltodict
import json

class Proteosafe:
    def __init__(self, taskid, workflow):
        """ Builds GNPS node attributes and edge list
        Returns
        -------
        gnps  :  gnps task identification data
        """
        self.taskid = taskid
        self.workflow = workflow

    def description(self):
        return "{} taskid is a {} workflow".format(self.taskid, self.workflow)

    def get_gnps(self):
        """ Sends a request to ProteoSAFe.
        Parameters
        ----------
        taskid : str
           gnps task id
        workflow : str
           gnps workflow type
        Returns
        -------
        gnps : pandas.DataFrame
            node attributes table.
        net : pandas.DataFrame
            edge list
        """
        taskid = self.taskid
        taskid = taskid.split(',')
        workflow = self.workflow
        gdict = {}

        if workflow=='MZmine':
            url_to_attributes = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=clusterinfo_summary/" % (taskid[0])
            url_to_edges = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=networking_pairs_results_file_filtered/" % (taskid[0])
            url_to_features = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=quantification_table/" % (taskid[0])
            url_to_metadata = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=metadata_table/" % (taskid[0])
            self.gnps = pd.read_csv(io.StringIO(requests.get(url_to_attributes).text), sep='\t')
            self.net = pd.read_csv(io.StringIO(requests.get(url_to_edges).text), sep='\t')
            self.feat = pd.read_csv(io.StringIO(requests.get(url_to_features).text))
            self.meta = pd.read_csv(io.StringIO(requests.get(url_to_metadata).text), sep='\t')
            if len(taskid) > 1:
                url_to_attributes = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=clusterinfo_summary/" % (taskid[1])
                url_to_edges = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=networking_pairs_results_file_filtered/" % (taskid[1])
                self.gnps1 = pd.read_csv(io.StringIO(requests.get(url_to_attributes).text, sep='\t'))
                self.net1 = pd.read_csv(io.StringIO(requests.get(url_to_edges).text), sep='\t')
            else:
                self.gnps1 = None
                self.net1 = None
        elif workflow=='V2':
            url_to_attributes = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=clusterinfosummarygroup_attributes_withIDs_withcomponentID/" % (taskid[0])
            url_to_edges = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=networkedges_selfloop/" % (taskid[0])
            self.gnps = pd.read_csv(io.StringIO(requests.get(url_to_attributes).text), sep='\t')
            self.net = pd.read_csv(io.StringIO(requests.get(url_to_edges).text), sep='\t')
            if len(taskid) > 1:
                url_to_attributes = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=clusterinfosummarygroup_attributes_withIDs_withcomponentID/" % (taskid[1])
                url_to_edges = "http://gnps.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=networkedges_selfloop/" % (taskid[1])
                self.gnps1 = pd.read_csv(io.StringIO(requests.get(url_to_attributes).text), sep='\t')
                self.net1 = pd.read_csv(io.StringIO(requests.get(url_to_edges).text), sep='\t')
            else:
                self.gnps1 = None
                self.net1 = None

    def get_nap(self):
        """ Sends a request to ProteoSAFe.
        Parameters
        ----------
        taskid : str
           NAP task id
        Returns
        -------
        gtaskid : str
            GNPS taskid.
        tabgnps : pandas.DataFrame
            node attributes table.
        net : pandas.DataFrame
            edge list
        mlist : pandas.DataFrame
            Structural grouping
        lid : pandas.DataFrame
            MetFrag candidatas
        fusion : pandas.DataFrame
            Fusion scores
        consensus : pandas.DataFrame
            Consensus scores
        """
        taskid = self.taskid
        ndict = {}

        url = 'http://dorresteinappshub.ucsd.edu:5001/NAPviewer/?task=%s' % taskid
        rnap = requests.get(url)
        if rnap.status_code==200:
            base_url = 'http://dorresteinappshub.ucsd.edu:5001/NAPviewer/static/downloads/{0}/{1}'
            url_to_tab = base_url.format(*[taskid, 'tabgnps.tsv'])
            url_to_net = base_url.format(*[taskid, 'net.tsv'])
            url_to_mlist = base_url.format(*[taskid, 'mlist.json'])
            url_to_fusion = base_url.format(*[taskid, 'fusion.json'])
            url_to_lid = base_url.format(*[taskid, 'lid.json'])
            url_to_consensus = base_url.format(*[taskid, 'consensus.json'])
            self.tabgnps = pd.read_csv(io.StringIO(requests.get(url_to_tab).text), sep='\t')
            self.net = pd.read_csv(io.StringIO(requests.get(url_to_net).text), sep='\t')
            self.mlist = json.load(io.StringIO(requests.get(url_to_mlist).text))
            self.fusion = json.load(io.StringIO(requests.get(url_to_fusion).text))
            self.lid = json.load(io.StringIO(requests.get(url_to_lid).text))
            self.consensus = json.load(io.StringIO(requests.get(url_to_consensus).text))
        else:
            print(rnap.text)

        # need parameter file
        target_url = "http://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=params/" % taskid
        r = requests.get(target_url)
        plist = xmltodict.parse(r.text)['parameters']['parameter']
        self.ndb = [x['#text'] for x in plist if x['@name']=='DATABASE'][0]
        self.gtaskid = [x['#text'] for x in plist if x['@name']=='JOBID'][0]

    def get_gnps_taskid(self):
        """ Sends a request to ProteoSAFe.
        Parameters
        ----------
        taskid : str
           NAP task id
        Returns
        -------
        gtaskid : str
            GNPS taskid.
        """
        taskid = self.taskid

        # need parameter file
        target_url = "http://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task=%s&block=main&file=params/" % taskid
        r = requests.get(target_url)
        plist = xmltodict.parse(r.text)['parameters']['parameter']
        self.gtaskid = [x['#text'] for x in plist if x['@name']=='JOBID'][0]

