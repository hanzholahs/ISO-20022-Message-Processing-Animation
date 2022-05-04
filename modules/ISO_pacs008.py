from lxml import etree
from copy import deepcopy
import dicttoxml
import os.path

class ISO_msg:
    def __init__(self, message=None):
        self.message = message
    def create_dict(self):
        if self.message:
            new_dict = {}
            for key in self.message.__dict__:
                if self.message.__dict__[key] is None:
                    continue
                    # new_dict[key] = obj.__dict__[key]
                elif not isinstance(self.message.__dict__[key], (int, float, str)):
                    new_dict[key] = object_to_dict(self.message.__dict__[key])
                else:
                    new_dict[key] = self.message.__dict__[key]
            return new_dict
        return None

class Pacs008:
    def __init__(self,GrpHdr=None, CdtTrfTxInf=None):
        self.GrpHdr      = GrpHdr           # GroupHeader93
        self.CdtTrfTxInf = CdtTrfTxInf      # CreditTransferTransaction39

class GroupHeader93:
    def __init__(self, MsgId, CreDtTm, NbOfTxs, SttlmInf, InstgAgt, InstdAgt):
        self.MsgId      = MsgId
        self.CreDtTm    = CreDtTm
        self.NbOfTxs    = NbOfTxs
        self.SttlmInf   = SttlmInf      # Class: SettlementInstruction7

        self.InstgAgt   = InstgAgt      # Class: BranchAndFinancialInstitutionIdentification6
        self.InstdAgt   = InstdAgt      # Class: BranchAndFinancialInstitutionIdentification6

class CreditTransferTransaction39:
    def __init__(self, PmtId, IntrBkSttlmAmt, ChrgBr, UltmtDbtr, Dbtr, DbtrAcct, DbtrAgt, CdtrAgt, CdtrAcct, Cdtr, UltmtCdtr):
        self.PmtId          = PmtId             # Class: PaymentIdentification7
        self.IntrBkSttlmAmt = IntrBkSttlmAmt    # Amount
        self.ChrgBr         = ChrgBr            # CodeSet: ChargeBearerType1Code
        self.UltmtDbtr      = UltmtDbtr         # Class: PartyIdentification135
        self.Dbtr           = Dbtr              # Class: PartyIdentification135
        self.DbtrAcct       = DbtrAcct          # Class: CashAccount38
        self.DbtrAgt        = DbtrAgt           # Class: BranchAndFinancialInstitutionIdentification6
        self.CdtrAgt        = CdtrAgt           # Class: BranchAndFinancialInstitutionIdentification6
        self.CdtrAcct       = CdtrAcct          # Class: CashAccount38
        self.Cdtr           = Cdtr              # Class: PartyIdentification135
        self.UltmtCdtr      = UltmtCdtr         # Class: PartyIdentification135



class SettlementInstruction7:
    def __init__(self, SttlmMtd, ClrSys, InstgRmbrsmntAgt, InstgRmbrsmntAgtAcct, InstdRmbrsmntAgt, InstdRmbrsmntAgtAcct, ThrdRmbrsmntAgt, ThrdRmbrsmntAgtAcct):
        self.SttlmMtd               = SttlmMtd  # CodeSet: SettlementMethod1Code
        self.ClrSys                 = ClrSys    # Class: ClearingSystemIdentification3Choice

        self.InstgRmbrsmntAgt       = InstgRmbrsmntAgt          # Class: BranchAndFinancialInstitutionIdentification6
        self.InstgRmbrsmntAgtAcct   = InstgRmbrsmntAgtAcct      # Class: CashAccount38
        self.InstdRmbrsmntAgt       = InstdRmbrsmntAgt          # Class: BranchAndFinancialInstitutionIdentification6
        self.InstdRmbrsmntAgtAcct   = InstdRmbrsmntAgtAcct      # Class: CashAccount38
        self.ThrdRmbrsmntAgt        = ThrdRmbrsmntAgt           # Class: BranchAndFinancialInstitutionIdentification6
        self.ThrdRmbrsmntAgtAcct    = ThrdRmbrsmntAgtAcct       # Class: CashAccount38


class PaymentIdentification7:
    def __init__(self, InstrId, EndToEndId, TxId, UETR, ClrSysRef):
        self.InstrId        = InstrId
        self.EndToEndId     = EndToEndId
        self.TxId           = TxId
        self.UETR           = UETR
        self.ClrSysRef      = ClrSysRef


class ClearingSystemIdentification3Choice:
    def __init__(self, Cd):
        self.Cd = Cd        # Codeset: ExternalClearingSystemIdentification1Code


class BranchAndFinancialInstitutionIdentification6:
    def __init__(self, FinInstnId):
        self.FinInstnId = FinInstnId









class PartyIdentification135:
    def __init__(self, Nm, PstlAdr, Id, CtryOfRes, CtctDtls):  
        self.Nm         = Nm
        self.PstlAdr    = PstlAdr   # Class: PostalAddress
        self.Id         = Id        # Class: Party38Choice
        self.CtryOfRes  = CtryOfRes
        self.CtctDtls   = CtctDtls  # Class: ContactDetails

class PostalAddress24:
    def __init__(self, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry):
        self.StrtNm         = StrtNm
        self.BldgNb         = BldgNb
        self.BldgNm         = BldgNm
        self.Flr            = Flr
        self.PstCd          = PstCd
        self.TwnNm          = TwnNm
        self.CtrySubDvsn    = CtrySubDvsn
        self.Ctry           = Ctry


class Party38Choice: 
    def __init__(self, OrgId, PrvtId):
        self.OrgId  = OrgId    # Class: OrganisationIdentification29
        self.PrvtId = PrvtId   # Class: PersonIdentification13

class PersonIdentification13:
    def __init__(self, DtAndPlcOfBirth, Othr):
        self.DtAndPlcOfBirth    = DtAndPlcOfBirth   # Class: DateAndPlaceOfBirth
        self.Othr               = Othr              # Class: GenericIdentification
        
class OrganisationIdentification29:
    def __init__(self, AnyBIC, LEI, Othr):
        self.AnyBIC = AnyBIC
        self.LEI    = LEI
        self.Othr   = Othr                          # Class: GenericIdentification
        
class GenericIdentification1:     # GenericOrganisationIdentification1 OR GenericPersonIdentification1 
    def __init__(self, Id, Issr):
        self.Id     = Id
        self.Issr   = Issr

class DateAndPlaceOfBirth1:
    def __init__(self, BirthDt, PrvcOfBirth, CityOfBirth, CtryOfBirth):
        self.BirthDt     = BirthDt
        self.PrvcOfBirth = PrvcOfBirth
        self.CityOfBirth = CityOfBirth
        self.CtryOfBirth = CtryOfBirth

class Contact4:   
    def __init__(self, PhneNb, MobNb, FaxNb, EmailAdr):
        self.PhneNb     = PhneNb
        self.MobNb      = MobNb
        self.FaxNb      = FaxNb
        self.EmailAdr   = EmailAdr

class CashAccount38:
    def __init__(self, Id, Ccy, Nm):
        self.Id     = Id    # Class: AccountIdentification4Choice
        self.Ccy    = Ccy
        self.Nm     = Nm

class AccountIdentification4Choice:
    def __init__(self, IBAN, Othr):
        self.IBAN   = IBAN
        self.Othr   = Othr  # Class: GenericAccountIdentification1

class GenericAccountIdentification1:
    def __init__(self, Id, Issr):
        self.Id     = Id
        self.Issr   = Issr


class FinancialInstitutionIdentification18:
    def __init__(self, BICFI, ClrSysMmbId, LEI, Nm, PstlAdr):
        self.BICFI          = BICFI
        self.ClrSysMmbId    = ClrSysMmbId   # Class: ClearingSystemMemberIdentification2
        self.LEI            = LEI
        self.Nm             = Nm
        self.PstlAdr        = PstlAdr       # Class: PostalAddress24
    
    def __sql_insert(self, conn, BICFI, ClrSysMmbId, LEI, Nm, PstlAdr):
        c = conn.cursor()
        self.MainID = str(self.sql_find_new_ID(conn))
        MmbId   = ClrSysMmbId.MmbId
        PstlAdr = PstlAdr.MainID
        c.execute(
            "INSERT INTO FinancialInstitutionIdentificationTable VALUES (:MainID, :BICFI, :MmbId, :LEI, :Nm, :PstlAdr)",
            {'MainID':self.MainID, 'BICFI':BICFI, 'MmbId':MmbId, 'LEI':LEI, 'Nm':Nm, 'PstlAdr':PstlAdr}
        )
        conn.commit()
        
    def sql_find_new_ID(self, conn):
        c = conn.cursor()
        c.execute("SELECT MAX(MainID) FROM FinancialInstitutionIdentificationTable")
        lastID = c.fetchone()[0]
        return int(lastID)+1 if lastID else 1

class ClearingSystemMemberIdentification2:
    def __init__(self, MmbId):
        self.MmbId          = MmbId






XML_PACS008 = etree.Element(
    "Document", nsmap={
        "xsi":"http://www.w3.org/2001/XMLSchema-instance" , 
        None: "urn:iso:std:iso:20022:tech:xsd:pacs.008.001.09"
    }
)
SCHEMA_PACS008 = etree.XMLSchema(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../msg/xsd/pacs.008.001.09.xsd"))

def create_msg(msg_root, messageObj, currency="IDR"):
    xml_file = deepcopy(msg_root)
    xml_file.append(etree.Element("FIToFICstmrCdtTrf"))
    data = etree.fromstring(dicttoxml.dicttoxml(object_to_dict(messageObj), attr_type=False))
    for child in data:
        xml_file[0].append(child)
    for child in xml_file.iter("IntrBkSttlmAmt"):
        child.set("Ccy", currency)
    return xml_file

def write_msg(xml, file_path):
    with open(file_path, "w") as xml_file:
        xml_file.write(etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode())
    
def validate_msg(schema, file_path):
    xml_file = etree.parse(file_path)
    return schema.validate(xml_file)
    

def object_to_dict(obj):
    new_dict = {}
    for key in obj.__dict__:
        if obj.__dict__[key] is None or obj.__dict__[key] == '' or key == "MainID":
            continue
        elif not isinstance(obj.__dict__[key], (int, float, str)):
            new_dict[key] = object_to_dict(obj.__dict__[key])
        else:
            new_dict[key] = obj.__dict__[key]
    return new_dict



