if __name__ != "__main__":
    from modules.custom_functions import get_now_datetime
    from modules.ISO_pacs008 import *


class Entities:
    def __init__(self):
        self.set_default_entities_dict()
        self.__party1 = self.set_Prvt(*self.__party1_default.values())
        self.__party2 = self.set_Org(*self.__party2_default.values())
        self.__bank1 = self.set_Bank(*self.__bank1_default.values())
        self.__bank2 = self.set_Bank(*self.__bank2_default.values())
        self.__msg = self.set_Msg(*self.__msg_default.values())

        self.centralNode = CentralNode()
        self.bank1 = Bank(self.__bank1["MmbId"], self.__bank1["Nm"], self.centralNode)
        self.bank2 = Bank(self.__bank2["MmbId"], self.__bank2["Nm"], self.centralNode)
        self.party1 = Account(self.__party1["Id"], self.__bank1["MmbId"], self.__party1["Nm"], balance=2525000., agent=self.bank1)
        self.party2 = Account(self.__party2["Id"], self.__bank2["MmbId"], self.__party2["Nm"], balance=3250000., agent=self.bank2)

    def set_entity_value(self, role, val):
        if role == "party1":
            self.__party1 = self.set_Prvt(*val)
            self.party1.name  = self.__party1["Nm"]
        elif role == "party2":
            self.__party2 = self.set_Org(*val)
            self.party2.name  = self.__party2["Nm"]
        elif role == "bank1":
            self.__bank1 = self.set_Bank(*val)
            self.bank1.name  = self.__bank1["Nm"]
        elif role == "bank2":
            self.__bank2 = self.set_Bank(*val)
            self.bank2.name  = self.__bank2["Nm"]
        elif role == "msg":
            self.__msg = self.set_Msg(*val)
        else:
            print("No such entity")

    def get_entity_default_values(self, role):
        if   role == "party1"   : return self.__party1_default.values()
        elif role == "party2"   : return self.__party2_default.values()
        elif role == "bank1"    : return self.__bank1_default.values()
        elif role == "bank2"    : return self.__bank2_default.values()
        elif role == "msg"      : return self.__msg_default.values()
        else: print("No such entity")
    
    def get_entity_values(self, role):
        if   role == "party1"   : return self.__party1.values()
        elif role == "party2"   : return self.__party2.values()
        elif role == "bank1"    : return self.__bank1.values()
        elif role == "bank2"    : return self.__bank2.values()
        elif role == "msg"      : return self.__msg.values()
        else: print("No such entity")

    def get_entity_default_dict(self, role):
        if   role == "party1"   : return self.__party1_default
        elif role == "party2"   : return self.__party2_default
        elif role == "bank1"    : return self.__bank1_default
        elif role == "bank2"    : return self.__bank2_default
        elif role == "msg"      : return self.__msg_default
        else: print("No such entity")
    
    def get_entity_dict(self, role):
        if   role == "party1"   : return self.__party1
        elif role == "party2"   : return self.__party2
        elif role == "bank1"    : return self.__bank1
        elif role == "bank2"    : return self.__bank2
        elif role == "msg"      : return self.__msg
        else: print("No such entity")
    
    def set_Prvt(
        self, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry, 
        BirthDt, PrvcOfBirth, CityOfBirth, CtryOfBirth, Id, Issr, CtryOfRes, PhneNb, MobNb, 
        FaxNb, EmailAdr
    ):
        return { "Nm":Nm, "StrtNm":StrtNm, "BldgNb":BldgNb, "BldgNm":BldgNm, "Flr":Flr, "PstCd":PstCd, 
            "TwnNm":TwnNm, "CtrySubDvsn":CtrySubDvsn, "Ctry":Ctry, "BirthDt":BirthDt, "PrvcOfBirth":PrvcOfBirth, 
            "CityOfBirth":CityOfBirth, "CtryOfBirth":CtryOfBirth, "Id":Id, "Issr":Issr, "CtryOfRes":CtryOfRes, 
            "PhneNb":PhneNb, "MobNb":MobNb, "FaxNb":FaxNb, "EmailAdr":EmailAdr,
        }
    def set_Org(
        self, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry, AnyBIC, LEI, Id, Issr, 
        CtryOfRes, PhneNb, MobNb, FaxNb, EmailAdr
    ):
        return {
            "Nm":Nm, "StrtNm":StrtNm, "BldgNb":BldgNb, "BldgNm":BldgNm, "Flr":Flr, "PstCd":PstCd, "TwnNm":TwnNm, 
            "CtrySubDvsn":CtrySubDvsn, "Ctry":Ctry, "AnyBIC":AnyBIC, "LEI":LEI, "Id":Id, "Issr":Issr, 
            "CtryOfRes":CtryOfRes, "PhneNb":PhneNb, "MobNb":MobNb, "FaxNb":FaxNb, "EmailAdr":EmailAdr
        }
    def set_Msg(
        self, MsgId, NbOfTxs, InstrId, EndToEndId, TxId, UETR, ClrSysRef, IntrBkSttlmAmt, ChrgBr
    ):
        return {
            "MsgId":MsgId, "NbOfTxs":NbOfTxs, "InstrId":InstrId, "EndToEndId":EndToEndId, "TxId":TxId, 
            "UETR":UETR, "ClrSysRef":ClrSysRef, "IntrBkSttlmAmt":IntrBkSttlmAmt, "ChrgBr":ChrgBr
        }
    def set_Bank(
        self, BICFI, MmbId, LEI, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry
    ):
        return {
            "BICFI":BICFI, "MmbId":MmbId, "LEI":LEI, "Nm":Nm, "StrtNm":StrtNm, "BldgNb":BldgNb, "BldgNm":BldgNm, 
            "Flr":Flr, "PstCd":PstCd, "TwnNm":TwnNm, "CtrySubDvsn":CtrySubDvsn, "Ctry":Ctry
        }

    def getISO_Prvt(
        self, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry, 
        BirthDt, PrvcOfBirth, CityOfBirth, CtryOfBirth, Id, Issr, CtryOfRes, PhneNb, MobNb, 
        FaxNb, EmailAdr
    ):
        return PartyIdentification135(
            Nm=Nm, 
            PstlAdr=PostalAddress24(
                StrtNm=StrtNm, BldgNb=BldgNb, BldgNm=BldgNm, Flr=Flr, PstCd=PstCd, TwnNm=TwnNm, 
                CtrySubDvsn=CtrySubDvsn, Ctry=Ctry
            ), 
            Id = Party38Choice(
                OrgId="", 
                PrvtId = PersonIdentification13(
                    DtAndPlcOfBirth = DateAndPlaceOfBirth1(
                        BirthDt=BirthDt, PrvcOfBirth=PrvcOfBirth, CityOfBirth=CityOfBirth, CtryOfBirth=CtryOfBirth
                    ), 
                    Othr = GenericIdentification1(
                        Id=Id, Issr=Issr
                    ))), 
            CtryOfRes=CtryOfRes, 
            CtctDtls   = Contact4(
                PhneNb=PhneNb, MobNb=MobNb, FaxNb=FaxNb, EmailAdr=EmailAdr
            )
        )       
    def getISO_Org(
        self, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry, AnyBIC, LEI, Id, Issr, 
        CtryOfRes, PhneNb, MobNb, FaxNb, EmailAdr
    ):
        return PartyIdentification135(
            Nm=Nm,
            PstlAdr = PostalAddress24(
                StrtNm=StrtNm, BldgNb=BldgNb, BldgNm=BldgNm, Flr=Flr, PstCd=PstCd, 
                TwnNm=TwnNm, CtrySubDvsn=CtrySubDvsn, Ctry=Ctry
            ), 
            Id = Party38Choice(
                OrgId  = OrganisationIdentification29(
                    AnyBIC=AnyBIC, LEI=LEI, 
                    Othr = GenericIdentification1(
                        Id=Id, Issr=Issr
                    )), 
                PrvtId=""), 
            CtryOfRes=CtryOfRes, 
            CtctDtls   = Contact4(
                PhneNb=PhneNb, MobNb=MobNb, FaxNb=FaxNb, EmailAdr=EmailAdr
            )
        )
    def getISO_Bank(
        self, BICFI, MmbId, LEI, Nm, StrtNm, BldgNb, BldgNm, Flr, PstCd, TwnNm, CtrySubDvsn, Ctry
    ):
        return FinancialInstitutionIdentification18(
            BICFI=BICFI, 
            ClrSysMmbId = ClearingSystemMemberIdentification2(MmbId=MmbId), 
            LEI=LEI,
            Nm=Nm, 
            PstlAdr = PostalAddress24(
                StrtNm=StrtNm, BldgNb=BldgNb, BldgNm=BldgNm, Flr=Flr, PstCd=PstCd, 
                TwnNm=TwnNm, CtrySubDvsn=CtrySubDvsn, Ctry=Ctry
            ), 
        )
    def getISO_Msg(
        self, MsgId, NbOfTxs, InstrId, EndToEndId, TxId, UETR, ClrSysRef, IntrBkSttlmAmt, ChrgBr
    ):
        return Pacs008(
            GrpHdr = GroupHeader93(
                MsgId   = MsgId,
                CreDtTm = get_now_datetime(), 
                NbOfTxs = NbOfTxs,
                SttlmInf= SettlementInstruction7(
                    SttlmMtd    = "CLRG", 
                    ClrSys      = ClearingSystemIdentification3Choice(
                        Cd    = "RTG"
                    ), 
                    InstgRmbrsmntAgt        = "", 
                    InstgRmbrsmntAgtAcct    = "", 
                    InstdRmbrsmntAgt        = "", 
                    InstdRmbrsmntAgtAcct    = "", 
                    ThrdRmbrsmntAgt         = "", 
                    ThrdRmbrsmntAgtAcct     = ""
                ), 
                InstgAgt = "", 
                InstdAgt = ""
            ),
            CdtTrfTxInf = CreditTransferTransaction39(
                PmtId       = PaymentIdentification7(
                    InstrId     = InstrId,
                    EndToEndId  = EndToEndId,
                    TxId        = TxId,
                    UETR        = UETR,
                    ClrSysRef   = ClrSysRef
                ),
                IntrBkSttlmAmt= IntrBkSttlmAmt,
                ChrgBr      = ChrgBr,
                UltmtDbtr   = "", 
                Dbtr        = self.getISO_Prvt(*self.__party1.values()), 
                DbtrAcct    = "", 
                DbtrAgt     = BranchAndFinancialInstitutionIdentification6(self.getISO_Bank(*self.__bank1.values())), 
                CdtrAgt     = BranchAndFinancialInstitutionIdentification6(self.getISO_Bank(*self.__bank2.values())), 
                CdtrAcct    = "", 
                Cdtr        = self.getISO_Org(*self.__party2.values()),
                UltmtCdtr   = ""
            )
        )        
    def set_default_entities_dict(self):
        self.__party1_default = PARTY1_DEFAULT
        self.__party2_default = PARTY2_DEFAULT
        self.__bank1_default  = BANK1_DEFAULT
        self.__bank2_default  = BANK2_DEFAULT
        self.__msg_default    = MSG_DEFAULT


class CentralNode:
    def __init__(self):
        self.banks = []
    def add_bank(self, bank):
        self.banks.append(bank)
    def process_transaction(self, creditorAgent, creditor, debtor, debtorAgent, amount, msg):
        try:
            # if not self.validate_pacs008(msg_path, SCHEMA_PACS008):
            #     raise Exception
            if not creditorAgent.validate_transaction(creditor, amount):
                raise Exception
            if not debtorAgent.validate_transaction(debtor, amount, send_money=False):
                raise Exception
        except Exception:
            print("WARNING: Error while validating transaction")
            return None

        msg.create_transaction_message()
        creditorAgent.send_money(creditor, amount)
        debtorAgent.receive_money(debtor, amount)
        print("Transaction success")

class Bank:
    def __init__(self, bankMainID, bankName, centralNode=None):
        self.bankMainID = bankMainID
        self.name       = bankName
        self.totalBalance   = 0
        self.accounts       = []
        
        if centralNode:
            centralNode.add_bank(self)
    
    def add_account(self, account):
        self.accounts.append(account)
        self.calculate_totalBalance()
    
    def send_money(self, account, amount):
        account.balance -= amount
        self.calculate_totalBalance()
        return True
    
    def receive_money(self, account, amount):
        account.balance += amount
        self.calculate_totalBalance()
        return True
    
    def validate_transaction(self, account, amount, send_money=True):
        if account not in self.accounts:
            print("Account not found")
            return False
        elif account.balance < amount and send_money:
            print("Insufficient fund")
            return False
        else:
            return True

    def calculate_totalBalance(self):
        balance = 0
        for account in self.accounts:
            balance += account.balance
        self.totalBalance = balance

class Account:
    def __init__(self, partyMainID, bankMainID, name, balance=0, agent=None):
        self.partyMainID = partyMainID
        self.bankMainID  = bankMainID
        self.name        = name
        self.balance     = balance
        if agent:
            agent.add_account(self)




# Set default parameters

PARTY1_DEFAULT = {
    "Nm":"Bambang Soetardjo",
    "StrtNm":"Kebun Sawit St.",
    "BldgNb":"19A",
    "BldgNm":'',
    "Flr":'',
    "PstCd":"13254",
    "TwnNm":"Jakarta Selatan",
    "CtrySubDvsn":"DKI Jakarta",
    "Ctry":"ID",
    "BirthDt":"1980-12-02",
    "PrvcOfBirth":"DKI Jakarta",
    "CityOfBirth":"Jakarta Selatan",
    "CtryOfBirth":"ID",
    "Id":"3180320212800021", 
    "Issr":"Dukcapil",
    "CtryOfRes":"ID",        
    "PhneNb":"", 
    "MobNb":"+62-81831412",
    "FaxNb":"",
    "EmailAdr":"Bambangsoe@goodmail.com"
}

PARTY2_DEFAULT = {
    "Nm":"PT Rembulan Sejati", 
    "StrtNm":"Cokelat Pagi St.",
    "BldgNb":"100AB",
    "BldgNm":"Menara Indah Tower",
    "Flr":"21",
    "PstCd":"13254",
    "TwnNm":"Jakarta Selatan",
    "CtrySubDvsn":"DKI Jakarta",
    "Ctry":"ID",
    "AnyBIC":"ARTHIDJA",
    "LEI":"",
    "Id":"114242526437",
    "Issr":"OSS",
    "CtryOfRes":"ID",
    "PhneNb":"+62-21214238",
    "MobNb":"",
    "FaxNb":"+62-21214238",
    "EmailAdr":"Contact@rembulansejati.com"
}

BANK1_DEFAULT = {
    "BICFI":"BMBRIDJA",
    "MmbId":"BMBR-1231412", 
    "LEI":"",
    "Nm":"Bank Mandiri Bersama", 
    "StrtNm":"Cokelat Panas St.",
    "BldgNb":"12",
    "BldgNm":"Kantor Pusat BMB",
    "Flr":"1",
    "PstCd":"13254", 
    "TwnNm":"Jakarta Selatan",
    "CtrySubDvsn":"DKI Jakarta",
    "Ctry":"ID"
}

BANK2_DEFAULT = {
    "BICFI":"BBSJIDJA", 
    "MmbId":"BBSJ-4293810",
    "LEI":"", 
    "Nm":"Bank Bumi Selatan Jaya",
    "StrtNm":"Jakarta Raya St.",
    "BldgNb":"31",
    "BldgNm":"Kantor Bumi Selatan Jaya",
    "Flr":"1",
    "PstCd":"15623",
    "TwnNm":"Jakarta Barat",
    "CtrySubDvsn":"DKI Jakarta",
    "Ctry":"ID"
}

MSG_DEFAULT = {
    "MsgId":"1122334455",
    "NbOfTxs":"1",
    "InstrId":"",
    "EndToEndId":"11232-ASA-1",
    "TxId":"",
    "UETR":"",
    "ClrSysRef":"",
    "IntrBkSttlmAmt":"20000000",
    "ChrgBr":"CRED"
}
