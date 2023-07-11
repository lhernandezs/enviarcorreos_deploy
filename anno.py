import calendar
import datetime
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

    # devuelve la lista de los dias laborables del mes
    def listaDiasLaborables(self):
        lista = []
        calendario = calendar.Calendar()
        for mes in range(1,13):
            tuplas = calendario.itermonthdays2(2023, mes)
            for (dia, ind) in tuplas:
                lista.append([mes, dia, ind])

        for item in lista:
            print(item)
        # listaDiasMes = [x for x in calendario.itermonthdays2(2023, self._mes)] # se crean las tuplas (dia mes, dia semana)
        # listaTuplasMes = list(filter(lambda x: x[1] not in [5,6] and x[0]!= 0, listaDiasMes)) # se elminan los sabados y domingos y se crea la lista de dias. tambien elimina los ceros de relleno en listaDiasMes
        # return list(filter(lambda x: x not in Mes.FESTIVOS[self._mes], [x[0] for x in listaTuplasMes])) # retorna la lista de dias laborables del mes eliminando los festivos

    # devuelve la fecha del ultimo dia del mes
    def ultimoDia(self):
        return datetime.date(2023, self._mes, 1) + relativedelta(day=31)
    
if __name__ == "__main__":
    y = Anno(2023)
    y.listaDiasLaborables()