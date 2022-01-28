import ast, statistics
from db_service import DbService
from scipy.spatial import distance

class KNNClassifier():

    def __init__(self, k, probe, threshold):
        self.k = k
        self.threshold = threshold
        self.probe = probe
        self.db = DbService('database.gait')
        self.gallery_angles = []
        self.gallery_dists = []
        self.gallery_lengths = []
        self.probe_angles = []
        self.probe_dists = []
        self.probe_lengths = []
    
    def classify(self):
        self.prepare_gallery()
        self.prepare_probe()
        distances = []
        for i in range(0, len(self.gallery_angles)):
            label = self.gallery_angles[i][0]
            gal_angles = []
            gal_dists = []
            gal_lengths = []
            for j in range(0, len(self.gallery_angles[i][1])):
                gal_angles += self.gallery_angles[i][1][j]
            for j in range(0, len(self.gallery_dists[i][1])):
                gal_dists += self.gallery_dists[i][1][j]
            for j in range(0, len(self.gallery_lengths[i][1])):
                gal_lengths += self.gallery_lengths[i][1][j]
            d1 = distance.euclidean(self.probe_angles, gal_angles)
            d2 = distance.euclidean(self.probe_dists, gal_dists)
            d3 = distance.euclidean(self.probe_lengths, gal_lengths)
            distances.append(((d1+d2+d3)/3, label))
        distances.sort()
        if distances[0][0] > self.threshold:
            return 5 #id_funcioanrio desconhecido
        lbls = []
        for rank in distances[0:self.k]:
            lbls.append(rank[1])
        return statistics.mode(lbls)

    def prepare_probe(self):
        angles = ast.literal_eval(self.probe)['angles']
        for j in range(0, len(angles)):
                self.probe_angles += angles[j]
        dists = ast.literal_eval(self.probe)['distances']
        for j in range(0, len(dists)):
                self.probe_dists += dists[j]
        lengths = ast.literal_eval(self.probe)['lengths']
        for j in range(0, len(lengths)):
                self.probe_lengths += lengths[j]
    
    def prepare_gallery(self):
        galley_templates = self.get_templates()
        for temp in galley_templates:
            self.gallery_angles.append(self.get_descriptor('angles', temp))
            self.gallery_dists.append(self.get_descriptor('distances', temp))
            self.gallery_lengths.append(self.get_descriptor('lengths', temp))

    def get_templates(self):
        query = """SELECT id_funcionario, descritor 
                    FROM templates"""
        _, result = self.db.execute_query(query)
        return result
    
    def get_descriptor(self, key, template):
        temp = ast.literal_eval(template[1])
        return (template[0], temp[key])    
