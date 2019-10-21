class Screen:

    def __init__(self):
        i =0
        
    def displayMessage(self,message):
        print(message)
        return

    def displayDollarAmount(self,amount):
        print (amount)
        return


class CashDispenser:
    _count =0

    def __init__(self):
        i =0
        
    def __init__(self,amount):
        self.count = 500

    def dispenseCash(self,amount):
        self.count -= int (amount/20)

    def isSufficientCashAvailable(self,amount):
        billsRequired = int (amount/20)
        if self.count>= billsRequired:
            return 1
        else:
            return 0


class Account:
    accountNumber = 0
    pin = 0
    availableBalance = 0.0
    totalBalance = 0.0

    def __init__(self,theAccountNumber,thePin,theAvailableBalance,theTotalBalance):
        self.accountNumber = theAccountNumber
        self.pin = thePin
        self.availableBalance = theAvailableBalance
        self.totalBalance = theTotalBalance

    def validatePin(self,userPin):
        if userPin == self.pin:
            return 1
        else:
            return 0

    def getAvailableBalance(self):
        return self.availableBalance

    def getTotalBalance(self):
        return self.totalBalance

    def credit(self,amount):
        self.availableBalance += amount
        self.totalBalance+= amount

    def debit(self,amount):
        self.availableBalance -= amount
        self.totalBalance -= amount

    def getAccountNumber(self):
        return self.accountNumber



class BankDatabase:
    accounts = []

    def __init__(self):
        
        a = Account(12345,54321,1000.0,1200.0)
        self.accounts.append(a)
        b = Account(98765,56789,200.0,200.0)
        self.accounts.append(b)

    def getAccount(self,accountNumber):
        i = 0
        while(i<len(self.accounts)):
            if(self.accounts[i].getAccountNumber()== accountNumber):
               return self.accounts[i]
            i +=1
        
        return 0
    def authenticateUser(self,userAccountNumber , userPin):

        userAccount = self.getAccount(userAccountNumber)
        if userAccount!=0:
            return userAccount.validatePin(userPin)
        else:
            return 0

    def getAvailableBalance(self,userAccountNumber):
        return self.getAccount(userAccountNumber).getAvailableBalance()

    def getTotalBalance( self,userAccountNumber ):
        return self.getAccount( userAccountNumber ).getTotalBalance()

    def credit( self,userAccountNumber,amount ):
        self.getAccount( userAccountNumber ).credit( amount )

    def debit( self, userAccountNumber, amount ):
        self.getAccount( userAccountNumber ).debit( amount )


class Transaction:
    
    accountNumber = 0
    screen = Screen() 
    bankDatabase = BankDatabase()
        
    #def __init__(self , userAccountNumber):
        #self.accountNumber = userAccountNumber

    def getAccountNumber(self):
        return self.accountNumber

    def getScreen(self):
        return self.screen

    def getBankDatabase(self):
        return self.bankDatabase

    def execute(self):
        i=0
    

class BalanceInquiry(Transaction):
    #accountNumber = 0
    def __init__(self,userAccountNumber,atmScreen,atmBankDatabase):
        #super(userAccountNumber)
        self.accountNumber = userAccountNumber
        self.bankDatabase = atmBankDatabase
        self.screen = atmScreen
        
    #def getAccountNumber(self):
       # return self.accountNumber
    
    def execute(self):
        self.bankDatabase = self.getBankDatabase();
        self.screen = self.getScreen();

        availableBalance = self.bankDatabase.getAvailableBalance( self.getAccountNumber() )

        totalBalance = self.bankDatabase.getTotalBalance( self.getAccountNumber() )

        self.screen.displayMessage( "\nBalance Information:" )
        self.screen.displayMessage( " - Available balance: " )
        self.screen.displayDollarAmount( availableBalance )
        self.screen.displayMessage( "\n - Total balance: " )
        self.screen.displayDollarAmount( totalBalance )
        self.screen.displayMessage( "" )



class Withdrawal(Transaction):
    #accountNumber = 0
    amount = 0
    cashDispenser = CashDispenser(0)

    def __init__(self,userAccountNumber,atmScreen,atmBankDatabase,atmCashDispenser):
        #__bases__(userAccountNumber)
        self.accountNumber = userAccountNumber
        self.cashDispenser = atmCashDispenser
        self.bankDatabase = atmBankDatabase
        self.screen = atmScreen
        
        
    #def getAccountNumber(self):
        #return self.accountNumber
    def execute(self):
        cashDispensed = 1
        availableBalance = 0.0
        self.bankDatabase = self.getBankDatabase()
        while cashDispensed:
            self.amount = self.displayMenuOfAmounts()
            if self.amount != 6:
                availableBalance = self.bankDatabase.getAvailableBalance(self.getAccountNumber())
                if self.amount <= availableBalance:
                    if self.cashDispenser.isSufficientCashAvailable(self.amount):
                        self.bankDatabase.debit(self.getAccountNumber(),self.amount)
                        self.cashDispenser.dispenseCash(self.amount)
                        cashDispensed = 0
                        print('\nYour Cash has been dispensed . Please take your cash now .')
                    else:
                        print("\nInsufficient cash available in the ATM . ","\n\nPlease choose a smaller amount.")
                else:
                    print("\nInsuffucient funds in your account.","\n\nPlease choose a smaller amount.")
            else:
                print("\nCanceling transaction...")
                cashDispensed = 0
                
                   
    def displayMenuOfAmounts(self):
        userChoice = 0
        amounts = [0,100,500,1000,2000,5000]
        while userChoice==0:
            print("\nWithdrawal Menu: ")
            print("1 - 100\n2 - 500\n3 - 1000\n4 - 2000\n5 - 5000\n6 - Cancel transaction")
            print("\nChoose a withdrawal amount: ")
            i = int(input())
            if i<6 :
                userChoice = amounts[i]
            elif i!=6:
                print ("\nInvalid selection. Try again. ")
            elif i==6:
                return i
                
        return userChoice


class DepositSlot:
    def isEnvelopeReceived():
        return 0

    
class Deposit(Transaction):
    amount= 0.0
    #accountNumber = 0
    depositSlot = DepositSlot()

    def __init__(self,userAccountNumber,atmScreen,atmBankDatabase,atmDepositSlot):
        #super(userAccountNumber)
        self.accountNumber = userAccountNumber
        self.depositSlot = atmDepositSlot
        self.bankDatabase = atmBankDatabase
        self.screen = atmScreen
        
    #def getAccountNumber(self):
       # return self.accountNumber
    
    def execute(self):
        self.bankDatabase = self.getBankDatabase()
        self.screen = self.getScreen()
        self.amount = self.promptForDepositAmount()
        if self.amount!= 0:
            print("\nPlease insert a deposit envelope containing ")
            self.screen.displayDollarAmount(self.amount)
            print(".")
            self.bankDatabase.credit(self.getAccountNumber(),self.amount)
        else:
            print("\nCenceling trnsaction...")

    def promptForDepositAmount(self):
        print("\nPlease enter a deposit amount in taka (or 0 to cencel: ")
        amount = int (input())
        return amount


class ATM:
    userAuthenticated = 0
    currentAccountNumber = 0
    screen = Screen()
    cashDispenser = CashDispenser(500)
    bankDatabase = BankDatabase()
    depositSlot = DepositSlot()
   
    
    def authenticateUser(self):
        print("\nPlease enter your acccount number")
        accountNumber = int(input())
        print("\nEnter your PIN: ")
        pin = int (input())
        self.userAuthenticated = self.bankDatabase.authenticateUser(accountNumber,pin)
        if self.userAuthenticated:
            self.currentAccountNumber = accountNumber
            return 1
        else:
            print("\nInvalid account number or PIN. Please try again.")
            return 0
    
    def performTransaction(self):
       # currentTransaction 
        exited = 0
        while exited==0 :
            menuSelection = self.displayMainMenu()
            if menuSelection <=3:
                currentTransaction = self.createTransaction(menuSelection)
                currentTransaction.execute()
            elif menuSelection ==4:
                exited = 1
                print("\nExiting the system...")
            else:
                print("\nYou did not enter a valid selection. Try again.")
    
    def displayMainMenu(self):
        print("\nMain menu: ")
        print("1 - View my balance")
        print("2 - Withdraw cash\n3 - Deposit funds")
        print("4 - Exit\n")
        print("Enter a choice: ")
        a = int(input())
        return a
    
    def createTransaction(self,ty):

        if ty ==1 :
            return  BalanceInquiry(self.currentAccountNumber,self.screen,self.bankDatabase)
        elif ty==2:
            return  Withdrawal(self.currentAccountNumber,self.screen,self.bankDatabase,self.cashDispenser)
        elif ty==3:
            return  Deposit(self.currentAccountNumber,self.screen,self.bankDatabase,self.cashDispenser)

    
    def run(self):
        
        while(1==1):
            while(self.userAuthenticated==0):
                print("\nWelcome!")
                self.userAuthenticated = self.authenticateUser()
            self.performTransaction()
            self.userAuthenticated = 0
            self.currentAccountNumber = 0
            print("\nThank you! Goodbye!")

theATM = ATM()
theATM.run()
                  
