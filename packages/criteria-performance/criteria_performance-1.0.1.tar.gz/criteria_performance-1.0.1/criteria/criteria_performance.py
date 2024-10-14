import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PerformanceCriteria:
    def __init__(self, url_data: str, val=20):
        self.__val = val
        self.__data = pd.read_csv(url_data)
        self.__classe, self.__score = self.__data[self.__data.columns[0]], self.__data[self.__data.columns[1]]
        self.__ppv, self.__pnv = self.ppv_pnv()
        self.__seuil = self.generate_seuil()
        self.__fp, self.__tp = self.fp_tp()
        self.__Tfp, self.__Ttp = self.Tfp_Ttp()
        self.__fn = self.calculate_fn()
        self.__fnr, self.__fpr = self.fnr_fpr()
        self.__rappel, self.__precision = self.coordonne()
        

    def ppv_pnv(self):
        p = len(self.__classe[self.__classe == 1])
        return self.__score[:p].to_numpy(), self.__score[p:].to_numpy()

    def get_ppv(self):
        return self.__ppv

    def get_pnv(self):
        return self.__pnv

    def generate_seuil(self):
        return np.linspace(self.__score.min() - 0.01, self.__score.max() + 0.01, self.__val)

    def get_seuil(self):
        return self.__seuil

    def fp_tp(self):
        fp = [(i, len(self.__pnv[self.__pnv > i])) for i in self.__seuil]
        tp = [(i, len(self.__ppv[self.__ppv > i])) for i in self.__seuil]
        return fp, tp

    def get_fp(self):
        return self.__fp

    def get_tp(self):
        return self.__tp

    def Tfp_Ttp(self):
        tfp = [k[1] / len(self.__pnv) for k in self.__fp]
        ttp = [k[1] / len(self.__ppv) for k in self.__tp]
        return tfp, ttp

    def get_tfp(self):
        return self.__Tfp

    def get_ttp(self):
        return self.__Ttp

    def calculate_fn(self):
        return [(k[0], len(self.__ppv) - k[1]) for k in self.__tp]

    def get_fn(self):
        return self.__fn

    def coordonne(self):
        rp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.__tp, self.__fn)]
        pp = [(k[0], k[1] / (k[1] + m[1])) for k, m in zip(self.__tp, self.__fp) if (k[1] + m[1]) > 0]
        coordonne = [(k[1], m[1]) for k, m in zip(pp, rp)]
        return [i[0] for i in coordonne], [i[1] for i in coordonne]

    def get_rappel(self):
        return self.__rappel

    def get_precision(self):
        return self.__precision

    def fnr_fpr(self):
        return [k[1] / len(self.__ppv) for k in self.__fn], [k[1] / len(self.__pnv) for k in self.__fp]

    def get_fnr(self):
        return self.__fnr

    def get_fpr(self):
        return self.__fpr

    def dispOldDET(self, title="Old DET", xl="Seuil", point=False, c1="b", c2="orange", cp="red", grid=False,save=False,name="courbe_hold-DET"):
        plt.plot(self.__seuil, self.__fnr, label="FNR", c=c1)
        plt.plot(self.__seuil, self.__fpr, label="FPR", c=c2)
        if point:
            x_intersect, y_intersect = self.infos()
            plt.scatter(x_intersect, y_intersect, color=cp, zorder=5, label=f"Intersection ({x_intersect:.2f}, {y_intersect:.2f})")
        plt.xlabel(xl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispDET(self, label="DET", xl="FNR", yl="FPR", c="orange", title="Courbe DET", grid=False,save=False,name="courbe_DET"):
        plt.plot(self.__fnr, self.__fpr, label=label, c=c)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispPR(self, label="P-R", xl="Rappel", yl="Précision", c="brown", title="Courbe Rappel-Précision", grid=False,save=False,name="courbe_P-R"):
        plt.plot(self.__rappel, self.__precision, label=label, c=c)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.title(title)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def dispROC(self, label="ROC", xl="TFP", yl="TTP", c="b", title="Courbe ROC", grid=False, save=False,name="courbe_ROC"):
        plt.plot(self.__Tfp, self.__Ttp, label=label, c=c)
        plt.title(title)
        plt.xlabel(xl)
        plt.ylabel(yl)
        plt.legend()
        if grid:
            plt.grid()
        if save:
            plt.savefig(name + ".png")

    def displaygraphe(self, taille=(18, 10), save=False, name="criteres_performance",point=False,cp="red"):
        plt.figure(figsize=taille)
        plt.subplot(2, 3, 1)
        self.dispROC()
        plt.subplot(2, 3, 2)
        self.dispPR()
        plt.subplot(2, 3, 3)
        self.dispDET()
        plt.subplot(2, 3, 4)
        self.dispOldDET()
        if point:
            x_intersect, y_intersect = self.infos()
            plt.scatter(x_intersect, y_intersect, color=cp, zorder=5, label=f"Intersection ({x_intersect:.2f}, {y_intersect:.2f})")
        plt.legend()
        if save:
            plt.savefig(name + ".png")

    def show(self):
        plt.show()

    def infos(self):
        diff = np.array(self.__fnr) - np.array(self.__fpr)
        sign_changes = np.where(np.diff(np.sign(diff)))[0]
        if len(sign_changes) > 0:
            for index in sign_changes:
                x_intersect = np.interp(0, diff[index:index + 2], self.__seuil[index:index + 2])
                y_intersect = np.interp(x_intersect, self.__seuil, self.__fnr)
                return x_intersect, y_intersect
        return None, None
    
    def __str__(self) -> str:
        info = (
            f"Informations sur les Criteres de Performances\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Total valeur seuil: {self.__val}\n\n"
            f"Valeurs Seuil: {self.__seuil.tolist()}\n\n"
            f"Classes: {self.__classe.tolist()}\n\n"
            f"Scores: {self.__score.tolist()}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"PPV (Positive Predictive Value): {self.__ppv.tolist()}\n\n"
            f"PNV (Negative Predictive Value): {self.__pnv.tolist()}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Faux Positifs (FP): {self.__fp}\n\n"
            f"Vrais Positifs (TP): {self.__tp}\n\n"
            f"Total Faux Positifs (TFP): {self.__Tfp}\n\n"
            f"Total Vrais Positifs (TTP): {self.__Ttp}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Faux Négatifs (FN): {self.__fn}\n\n"
            f"False Negative Rate (FNR): {self.__fnr}\n\n"
            f"False Positive Rate (FPR): {self.__fpr}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Rappel: {self.__rappel}\n\n"
            f"Précision: {self.__precision}\n"
            f"------------------------------------------------------------------------------------------\n"
            f"Point egale Erreur:{self.infos()}"
        )
        return info
