import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PerformanceCriteria:
    def __init__(self, url_data: str):
        self.data = pd.read_csv(url_data)
        self.classe, self.score = self.data[self.data.columns[0]], self.data[self.data.columns[1]]
        self.ppv, self.pnv = self.ppv_pnv()
        self.seuil = self.generate_seuil()
        self.fp, self.tp = self.fp_tp()
        self.Tfp, self.Ttp = self.Tfp_Ttp()
        self.fn = self.calculate_fn()
        self.fnr, self.fpr = self.fnr_fpr()
        self.rapel, self.precision = self.coordonne()

    def ppv_pnv(self):
        p = len(self.classe[self.classe == 1])
        return self.score[:p].to_numpy(), self.score[p:].to_numpy()

    def generate_seuil(self, val=10):
        return np.linspace(self.score.min() - 0.01, self.score.max() + 0.01, val)

    def get_seuil(self):
        return self.seuil

    def fp_tp(self):
        fp = [(i, len(self.pnv[self.pnv > i])) for i in self.seuil]
        tp = [(i, len(self.ppv[self.ppv > i])) for i in self.seuil]
        return fp, tp

    def Tfp_Ttp(self):
        tfp = [k[1] / len(self.pnv) for k in self.fp]
        ttp = [k[1] / len(self.ppv) for k in self.tp]
        return tfp, ttp

    def calculate_fn(self):
        return [(k[0], len(self.ppv) - k[1]) for k in self.tp]

    def coordonne(self):
        rp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.tp, self.fn)]
        pp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.tp, self.fp) if (k[1] + m[1]) > 0]
        coordonne = [(k[1], m[1]) for k, m in zip(pp, rp)]
        return [i[0] for i in coordonne], [i[1] for i in coordonne]

    def fnr_fpr(self):
        return [k[1] / len(self.ppv) for k in self.fn], [k[1] / len(self.pnv) for k in self.fp]

    def dipoldDET(self,title="hold DET"):
        plt.plot(self.seuil,self.fnr,label="FNR",c="b")
        plt.plot(self.seuil,self.fpr,label="FPR",c="orange")
        plt.xlabel("Seuil")
        plt.title(title)
        plt.legend()

    def dispDET(self,label="DET",c="orange",title="Courbe DET"):
        plt.plot(self.fnr,self.fpr,label=label,c=c)
        plt.xlabel("FNR")
        plt.ylabel("FPR")
        plt.title(title)
        plt.legend()

    def dispPR(self,label="P-R",c="brown",title="Courbe Rappel-Precision"):
        plt.plot(self.rapel,self.precision,label=label,c=c)
        plt.xlabel("Rappel")
        plt.ylabel("Precision")
        plt.title(title)
        plt.legend()

    def dispROC(self,label="ROC",c="b",title="Courbe ROC"):
        plt.plot(self.Tfp,self.Ttp,label=label,c=c)
        plt.title(title)
        plt.xlabel("TFP")
        plt.ylabel("TTP")
        plt.legend()
        

    def displaygraphe(self,taille=(18,10),save=False,name="criteres_performance"):
        plt.figure(figsize=taille)
        plt.subplot(2,3,1)
        self.dispROC()
        plt.subplot(2,3,2)
        self.dispPR()
        plt.subplot(2,3,3)
        self.dispDET()
        plt.subplot(2,3,4)
        self.dipoldDET()
        if save:
            plt.savefig(name+".png")
        plt.show()