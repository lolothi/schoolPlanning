from enum import IntEnum
from datetime import datetime, date
from dateutil.easter import easter, EASTER_WESTERN
from dateutil.relativedelta import relativedelta
import json
from collections import namedtuple
import serpy

class Jour(IntEnum):
    LUNDI = 1
    MARDI= 2
    MERCREDI = 3
    JEUDI = 4
    VENDREDI = 5
    SAMEDI = 6
    DIMANCHE = 7

class Mois(IntEnum):
    
    JANVIER   = 1
    FEVRIER   = 2
    MARS      = 3
    AVRIL     = 4
    MAI       = 5
    JUIN      = 6
    JUILLET   = 7
    AOUT      = 8
    SEPTEMBRE = 9
    OCTOBRE   = 10
    NOVEMBRE  = 11
    DECEMBRE  = 12
            
class JoursFeries(object):
    
    def __init__(self, annee: int = datetime.now().year):
        self.current_year = int(annee)
            
    @property
    def current_year(self) -> int:
        return self._annee

    @current_year.setter
    def current_year(self, value: int) -> None:
        self._annee = value
    
    @property
    def JOUR_DE_L_AN(self) -> date:
        return date(self.current_year, Mois.JANVIER, 1)
    
    @property
    def PAQUES(self) -> date:
        return easter(self.current_year, method=EASTER_WESTERN)
    
    @property
    def LUNDI_DE_PAQUES(self) -> date:
        return self.PAQUES + relativedelta(days=1)
    
    @property
    def FETE_DU_TRAVAIL(self) -> date:
        return date(self.current_year, Mois.MAI, 1)
    
    @property
    def VICTOIRE_1945(self) -> date:
        return date(self.current_year, Mois.MAI, 8)
    
    @property
    def ASCENSION(self) -> date:
        return self.PAQUES + relativedelta(days=39)
    
    @property
    def PENTECOTE(self) -> date:
        return self.PAQUES + relativedelta(days=49)
    
    @property
    def LUNDI_DE_PENTECOTE(self) -> date:
        return self.PENTECOTE + relativedelta(days=1)
    
    @property
    def FETE_NATIONALE(self) -> date:
        return date(self.current_year, Mois.JUILLET, 14)
    
    @property
    def ASSOMPTION(self) -> date:
        return date(self.current_year, Mois.AOUT, 15)
    
    @property
    def TOUSSAINT(self) -> date:
        return date(self.current_year, Mois.NOVEMBRE, 1)
    
    @property
    def ARMISTICE_1918(self) -> date:
        return date(self.current_year, Mois.NOVEMBRE, 11)
    
    @property
    def NOEL(self) -> date:
        return date(self.current_year, Mois.DECEMBRE, 25)
    
    @property
    def proprietes(self) -> list:
        return list(self.dumps().keys())
    
    def to_list(self) -> list:
        return [getattr(self, x) for x in self.dumps().keys()]
    
    def __str__(self) -> str:
        return '\n'.join([f'{x:<20s}: {getattr(self, x)}' for x in self.dumps().keys()])
    
    def __repr__(self) ->str:
        return json.dumps(self.dumps(), indent=4, ensure_ascii=False)
        
    def dumps(self) -> dict:
        return JoursFeriesSerialize(self).data
    
    def to_namedtuple(self) -> namedtuple:
        return namedtuple('JourFeries', self.dumps().keys())(**self.dumps())
    
class JoursFeriesSerialize(serpy.Serializer):
    
    JOUR_DE_L_AN       = serpy.StrField()
    PAQUES             = serpy.StrField()
    LUNDI_DE_PAQUES    = serpy.StrField()
    FETE_DU_TRAVAIL    = serpy.StrField()
    VICTOIRE_1945      = serpy.StrField()
    ASCENSION          = serpy.StrField()
    PENTECOTE          = serpy.StrField()
    LUNDI_DE_PENTECOTE = serpy.StrField()
    FETE_NATIONALE     = serpy.StrField()
    ASSOMPTION         = serpy.StrField()
    TOUSSAINT          = serpy.StrField()
    ARMISTICE_1918     = serpy.StrField()
    NOEL               = serpy.StrField()