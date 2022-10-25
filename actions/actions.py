from turtle import home
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import regex
import re
import requests
L = ["home", "house", "land", "appartment", "car", "vehicle", "bike", "motorcycle"]
class ValidateSimpleLoanForm(FormValidationAction):
    """Custom form action to fill all slots required to find specific type
    of healthcare facilities in a certain city or zip code."""

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "validate_simple_loan_form"

    def validate_amount1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `amount` value."""

        if not slot_value:
            dispatcher.utter_message("you didn't enter any amount")
            return {"amount1": None}
        else:
            slot_value = slot_value.lower()
            L = slot_value.split(" ") 
            if len(L) > 1:
                if L[1] == "dollars":
                    L[0] = str(int(L[0]) * 1.01)
                    L[1] = "euros"
                slot_value = " ".join(L)
            else:
                if slot_value.count("$") == 1:
                    slot_value = str(int(slot_value[:-1])*1.01) + " euros"    
                elif slot_value.count("£") == 1:
                    slot_value = slot_value[:-1] + " euros"
            dispatcher.utter_message(text=f"OK! You want to get {slot_value}.")
            return {"amount1": slot_value}

    def validate_purpose(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `duration` value."""

        if slot_value.lower() not in L:
            dispatcher.utter_message("you didn't enter any account_number")
            return {"purpose": None}
        else:
            if L.index(slot_value) < L.index("car"):
                slot_value = "home"
            else:
                slot_value = "car"
            dispatcher.utter_message(text=f"OK! You want to get a {slot_value} loan.")
            return {"purpose": slot_value}

    def validate_loan_term(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `duration` value."""

        if not slot_value:
            dispatcher.utter_message("you didn't enter any account_number")
            return {"loan_term": None}
        else:
            L = tracker.latest_message.get("text").split(" ")
            if "years" in L: 
                if "months" in L:
                    if L.index("years") < L.index("months"):
                        slot_value = " ".join(L[L.index("years")-1:L.index("months")+1])
                    else:
                        slot_value = " ".join(L[L.index("months")-1:L.index("years")+1])
                else:
                    slot_value = " ".join(L[L.index("years")-1:L.index("years")+1])
            elif "months" in L:
                slot_value = " ".join(L[L.index("months")-1:L.index("months")+1])
            else:
                slot_value = None
            
            dispatcher.utter_message(text=f"OK! You want to get a loan for {slot_value}.")
            return {"loan_term": slot_value}
        

class ValidateSimpleBalanceForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "validate_simple_balance_form"

    def validate_account_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `amount` value."""

        #if not slot_value:
           # dispatcher.utter_message("you didn't enter any account_number")
           # return {"account_number": None}
        #else:
        ch99 = tracker.latest_message.get("text")
        pattern1 = "\d+"
        digit99 = re.findall(pattern1,ch99)
        digit99 = [i for i in digit99 if len(i)==10]
        if len(digit99)!= 1:
            slot_value = None
            return {"account_number": None}
        else:
            slot_value = digit99[0]
            dispatcher.utter_message(text=f"OK! this is your account number {slot_value}.")
            result=requests.post('http://127.0.0.1:5000/check_balance', json = {"an": slot_value})
            dispatcher.utter_message(text=f"OK! this is your solde: {result.text}.")
            return {"account_number": slot_value}
        

class ValidateSimpleTransactionForm(FormValidationAction):

    def name(self) -> Text:
        """Unique identifier of the form"""

        return "validate_simple_transaction_form"

    def validate_amount(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `amount` value."""

        if not slot_value:
            dispatcher.utter_message("you didn't enter any account_number")
            return {"amount": None}
        else:
            slot_value = slot_value.lower()
            L = slot_value.split(" ") 
            if len(L) > 1:
                if L[1] == "dollars":
                    L[0] = str(int(L[0]) * 1.01)
                    L[1] = "euros"
                slot_value = " ".join(L)
            else:
                if slot_value.count("$") == 1:
                    slot_value = str(int(slot_value[:-1])*1.01) + " euros"    
                else:
                    slot_value = slot_value[:-1] + " euros"
                    dispatcher.utter_message(text=f"OK! this is the amount of money you want to send: {slot_value}.")  
            return {"amount": slot_value}


    def validate_account_number1(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `amount` value."""

        if not slot_value:
            dispatcher.utter_message("you didn't enter any account_number")
            return {"amount": None}
        else:
            ch = tracker.latest_message.get("text")
            l1 = ch.split(" ")
            pattern1 = "\d+"
            digit = re.findall(pattern1,ch)
            digit = [i for i in digit if len(i)==10]
            l2 = [i for i, x in enumerate(l1) if x == "to"]  #indexes of "to"
            if len(digit) == 1:
                if "from" in l1:
                    if len(l2) != 0:
                        b = l2[-1]
                        c = l1.index("from")
                        if b > c:  # from 9bal to, i want to send money from my account to this account 1147855236
                            if l1.index(digit[0]) < b :
                                departure = digit[0]
                                destination = None
                            else:
                                departure = None
                                destination = digit[0]
                        else:  # to 9bal from, i want to send to this account from my account 1223654789
                            if l1.index(digit[0]) < c :  #i want to send to 1223654789 from my account
                                departure = None
                                destination = digit[0]
                            else:                         # i want to send to my friend from my account 1123547896
                                departure = digit[0]
                                destination = None
                    else:  #ma famech to
                        departure = digit[0]
                        destination = None
                
                else: #from mehich mawjouda
                    if "to" in l1:
                
                        l22 = [i for i, x in enumerate(l1) if x == "to"]
                        z = l22[-1]
                        if z < l1.index(digit[0]):
                            destination = digit[0]   #fel account number 2 wel 3aks fel account number 1 ******************************
                            departure = None
                        else:
                            destination = None   
                            departure = digit[0]
                    else:
                        destination = None    
                        departure = digit[0]




                    
            elif len(digit) ==2:
                if "from" in l1:
                    if len(l2) != 0:
                        d = l2[-1]  #to
                        e = l1.index("from")
                        if d > e:
                            destination = digit[1]
                            departure = digit[0]
                        else:
                            departure = digit[1]
                            destination = digit[0]
                    else: #mafamech to, send 1236547897, from my account 1123654789, a9reb wa7da lel from
                        l7 = l1[l1.index("from"):]  #mel from lel e5er
                        ch7 = " ".join(l7)
                        digit7 = re.findall(pattern1, ch7)
                        digit7 = [i for i in digit7 if len(i)==10]
                        departure = digit7[0]
                        destination = [i for i in digit if i != departure][0]
                else:  #ma famech from
                    if "my" in l1:
                        l8 = l1[l1.index("my"):]
                        ch8 = " ".join(l8)
                        digit8 = re.findall(pattern1, ch8)
                        digit8 = [i for i in digit8 if len(i)==10]
                        departure = digit8[0]
                        destination = [i for i in digit if i != departure][0]
            else:
                departure = None
                destination = None
            l10 = [departure] + [destination]
   





            slot_value = l10[0]
            dispatcher.utter_message(text=f"OK! this is your account number: {slot_value}.")
            return {"account_number1": slot_value}
    def validate_account_number2(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `amount` value."""

        if not slot_value:
            dispatcher.utter_message("you didn't enter any account_number")
            return {"amount": None}
        else:
            ch = tracker.latest_message.get("text")
            l1 = ch.split(" ")
            pattern1 = "\d+"
            digit = re.findall(pattern1,ch)
            digit = [i for i in digit if len(i)==10]
            l2 = [i for i, x in enumerate(l1) if x == "to"]  #indexes of "to"
            if len(digit) == 1:
                if "from" in l1:
                    if len(l2) != 0:
                        b = l2[-1]
                        c = l1.index("from")
                        if b > c:  # from 9bal to, i want to send money from my account to this account 1147855236
                            if l1.index(digit[0]) < b :
                                departure = digit[0]
                                destination = None
                            else:
                                departure = None
                                destination = digit[0]
                        else:  # to 9bal from, i want to send to this account from my account 1223654789
                            if l1.index(digit[0]) < c :  #i want to send to 1223654789 from my account
                                departure = None
                                destination = digit[0]
                            else:                         # i want to send to my friend from my account 1123547896
                                departure = digit[0]
                                destination = None
                    else:  #ma famech to
                        departure = digit[0]
                        destination = None
                
                else: #from mehich mawjouda
                    if "to" in l1:
                
                        l22 = [i for i, x in enumerate(l1) if x == "to"]
                        z = l22[-1]
                        if z < l1.index(digit[0]):
                            destination = digit[0]   #fel account number 2 wel 3aks fel account number 1 ******************************
                            departure = None
                        else:
                            destination = None   #fel account number 2 wel 3aks fel account number 1 ******************************
                            departure = digit[0]
                    else:
                        destination = digit[0]   #fel account number 2 wel 3aks fel account number 1 ******************************
                        departure = None

            elif len(digit) ==2:
                if "from" in l1:
                    if len(l2) != 0:
                        d = l2[-1]  #to
                        e = l1.index("from")
                        if d > e:
                            destination = digit[1]
                            departure = digit[0]
                        else:
                            departure = digit[1]
                            destination = digit[0]
                    else: #mafamech to, send 1236547897, from my account 1123654789, a9reb wa7da lel from
                        l7 = l1[l1.index("from"):]  #mel from lel e5er
                        ch7 = " ".join(l7)
                        digit7 = re.findall(pattern1, ch7)
                        digit7 = [i for i in digit7 if len(i)==10]
                        departure = digit7[0]
                        destination = [i for i in digit if i != departure][0]
                else:  #ma famech from
                    if "my" in l1:
                        l8 = l1[l1.index("my"):]
                        ch8 = " ".join(l8)
                        digit8 = re.findall(pattern1, ch8)
                        digit8 = [i for i in digit8 if len(i)==10]
                        departure = digit8[0]
                        destination = [i for i in digit if i != departure][0]
            else:
                departure = None
                destination = None
            l10 = [departure] + [destination]
   
            slot_value = l10[1]
            dispatcher.utter_message(text=f"OK! this is your receiver account number: {slot_value}.")
            return {"account_number2": slot_value}

class ActionVerify(Action):
    def name(self) -> Text:
        return "action_verify"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #az = tracker.events.get("text")
        for event in tracker.events:
            if event.get("event") == "bot":
                #print("bot",event.get("text"))
                msg = event.get("text")
        #dispatcher.utter_message(text=msg)
        pattern0 = "\d+"
        digit9 = re.findall(pattern0,msg)
        digit9[-1] = digit9[-1] +" " + msg.split(" ")[-1] 
        ccch = " ".join(digit9)
        #dispatcher.utter_message(text=ccch)
        result=requests.post('http://127.0.0.1:5000/credit_transfer', json = {"from_an": digit9[1], "to_an": digit9[0], "montant": digit9[2]})
        dispatcher.utter_message(text=f"OK! {result.text}.")
        return []

class ActionLoan(Action):
    def name(self) -> Text:
        return "action_loan"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #az = tracker.events.get("text")
        for event in tracker.events:
            if event.get("event") == "bot":
                #print("bot",event.get("text"))
                msg = event.get("text")
        #dispatcher.utter_message(text=msg)
        #you want to get a {purpose} loan of {amount1} for {loan_term}
        L = msg.split(" ")
        a = " ".join(L[L.index("of")+1: L.index("of")+3])
        b = " ".join(L[L.index("for")+1:])
        ab = " ".join(L[L.index("a")+1])
        #ll = [a] + [b] 
        result=requests.post('http://127.0.0.1:5000/credit', json = {"montant": a, "duration": b, "purpose": ab})
        dispatcher.utter_message(text=f"OK! {result.text}.")
        return []
        

    