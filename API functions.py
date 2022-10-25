from flask import Flask, request
app = Flask(__name__)

comptes={"1234567890":1025,
         "4587715678":200}


@app.route("/check_balance", methods=["POST"])
def test1():
    #comptes={"1234567890":1000,
         #"4587715678":200}
    input = request.get_json(force=True) # {"an":"1512486359"}
    '''
    if input["an"] in list(comptes.keys()):
        #return str(comptes[input["an"]])
        return comptes[input["an"]]
        #return( list(comptes.keys()))
    else:
        #return( list(comptes.keys()))

        return comptes[input["an"]]
    '''
    if input["an"] in list(comptes.keys()):
        return str(comptes[input["an"]]) + " euros"
    else:
        #return str(type(input["an"]))
        return "This account number is not found in our database"

@app.route("/credit_transfer", methods=["POST"])
def test2():
    input = request.get_json(force=True) # input = {"from_an": "9487789655","to_an":"1078965484","montant":"1215 euros"} #
    if input["from_an"] in list(comptes.keys()):
        #montant=input['montant']
        montant=int(input['montant'].split(" ")[0])
        solde=comptes[input["from_an"]]
        if montant<=solde:
            if input["to_an"] in list(comptes.keys()):   
                comptes[input["from_an"]]=comptes[input["from_an"]]-montant
                comptes[input["to_an"]]=comptes[input["to_an"]]+montant
                return "The transaction is done."
            else:
                return "The reciever not found."
        else:
            return "You don't have enough money to send."
    else:
        return "The account number of the sender don't exists in the database."

@app.route("/credit", methods=["POST"])
def test3():
    input = request.get_json(force=True) # {"montant":"74120 dollars", "duration":"12 months", "purpose": "car"}
    #monthly payement PMT = PVi(1+i)^n/(1+i)^n-1     PV: amount of money, n:duration in months, i:interest
    L = input["duration"].split(" ")
    if "months" in L:
        if "years" in L:
            number_of_months = int(L[L.index("months")-1]) + int(L[L.index("years")-1])*12
        elif "year" in L:
            number_of_months = int(L[L.index("months")-1]) + 12
        #months only
        else:
            number_of_months = int(L[L.index("months")-1])
    
    elif "year" in L:
        number_of_months = 12
    else:
        number_of_months = int(L[L.index("years")-1])*12
    if input["purpose"] == "car":
        monthly_payement = "11"
    else:
        #monthly_payement = int(input["montant"].split(" ")[0])*(0.07/12)*((1+(0.07/12))**number_of_months)/(((1+(0.07/12))**number_of_months)-1)
        monthly_payement = "12"
    return "this is your monthly payment:" + str(monthly_payement)




    


app.run()