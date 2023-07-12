import calendar
from datetime import date
from dateutil.relativedelta import relativedelta

class Anno:
    FESTIVOS = { 2023:
                        {   1 :  [9],       
                            2 :  [],
                            3 :  [20],
                            4 :  [6, 7],
                            5 :  [1, 22],
                            6 :  [12, 19],
                            7 :  [3, 20],
                            8 :  [7, 21],
                            9 :  [],
                            10 : [16],
                            11 : [6, 13],
                            12 : [8, 25],
                        },
                  2024: {   1 :  [8],
                            2 :  [],
                            3 :  [],
                            4 :  [],
                            5 :  [],
                            6 :  [],
                            7 :  [20],
                            8 :  [7],
                            9 :  [],
                            10 : [],
                            11 : [],
                            12 : [8, 25],
                        },
                }
    
    def __init__(self, anno):
        self._anno = anno

    # devuelve la lista de los dias laborables del año
    def listaDiasLaborables(self):
        listaDiasNum = []
        calendario = calendar.Calendar()
        for mes in range(1,13):
            tuplas = calendario.itermonthdays2(self._anno, mes)
            for (dia, ind) in tuplas:
                listaDiasNum.append([mes, dia, ind])

        listaDepurada = list(filter(lambda x: x[2] not in [5,6] and x[1]!= 0, listaDiasNum)) # se elminan los sabados y domingos y se crea la lista de dias. tambien elimina los ceros de relleno en listaDiasMes
        listaFechas = list(map(lambda d: date(self._anno, d[0], d[1]), listaDepurada))
        return list(filter(lambda f: f not in self.listaFestivos(), listaFechas))

    def listaFestivos(self):
        festivos = []
        for mes in Anno.FESTIVOS[self._anno]:
            for dia in Anno.FESTIVOS[self._anno][mes]:
                festivos.append(date(self._anno, mes, dia))
        return festivos

    
if __name__ == "__main__":
    y = Anno(2023)
    for dia in y.listaDiasLaborables():
        print(dia)