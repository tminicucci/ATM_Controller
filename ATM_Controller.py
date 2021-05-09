import math

class ATMController():
	def __init__(self, MaxWithdrawal, CashReserves):
		self.CardNumber = None
		self.MaxWithdrawal = MaxWithdrawal
		self.CashReserves = CashReserves

	def ReadCard(self):
		#Scan magnetic strip
		self.CardNumber = input()

	def IsValidAccount(self):
		self.CardNumber
		CardValid = True				#Confirm with host that card number is connected to an account
		if(CardValid):
			return True
		else: return False

	def AccessAccount(self, Pin):
		ValidPin = True					#Query host to verify the given pin with the customer's bank
		if(ValidPin):
			return True
		else:
			print("Invalid Pin")
			return False

	def ViewBalance(self):
		#Select Checking or Savings
		#Query the host to fetch the current account balance and display to screen
		pass

	def RequestWithdrawal(self):
		#Select Checking or Savings
		Amount = int(input())
		CurrentLimit = min(self.MaxWithdrawal, self.CashReserves)
		if(Amount > CurrentLimit):
			Amount = CurrentLimit
		WithdrawalAccepted = True		   		    #Query host to have bank approve the withdrawal amount requested on this account  
		if(WithdrawalAccepted):						#Host will debit the bank and dispense an equal amount of cash to the customer at the ATM
			self.DispenseCash(Amount)
			self.CashReserves -= Amount
		else:
			print("Insufficient Funds")

	def InitiateDeposit(self):
		#Select Checking or Savings
		print("Enter Cash or Checks Below")
		IsDonePressed = False
		CashDeposit = 0
		CheckDeposit= 0
		DepositedAmount = 0
		while(True):
			Scan = ("Check", 500)					#A function connected to the scanner can return a tuple (type, amount) where type is bill or check. Complete scanning each bill or check entered before continuing to next loop
			if(Scan == None):
				print("Check could not be scanned")
			if(Scan[0] == "Bill"):
				CashDeposit += Scan[1]
			else: CheckDeposit += Scan[1]
			DepositedAmount += CashDeposit + CheckDeposit	
			print("Done")												#This would instead be a button on-screen
			IsDonePressed = True if(input() == "Yes") else False		#For testing purposes only
			if(IsDonePressed):											#Monitors the status of UI so the customer may complete the deposit after the last bill has been scanned
				break
		self.CashReserves += CashDeposit
		#Query host to add DepositedAmount from the host account to customer's bank account

	def DispenseCash(self, Amount):
		Payable = Amount
		Denominations = [20, 10, 5, 1]
		CashToDispense = []						#Array to hold how many of each bill must be dispensed to meet the withdrawal request. We assume there are enough of each bill to meet the request
		for Bill in Denominations:
			if(Payable >= Bill):
				Bill_Count = math.floor(Payable/Bill)
				Payable -= Bill * Bill_Count
				CashToDispense.append(Bill_Count)

	def GenerateReceipt(self, SelectedOption):
		#Include date, time, transaction performed
		#Include available account balance and total account balance
		pass


	def BeginService(self):
		while(True):
			print("Select an option")
			SelectedOption = input()
			if(SelectedOption == "View Balance"):
				self.ViewBalance()
			elif(SelectedOption == "Withdrawal"):
				self.RequestWithdrawal()
			elif(SelectedOption == "Deposit"):
				self.InitiateDeposit()
			self.GenerateReceipt(SelectedOption)
			print("Would you like to perform another transaction?")
			if(input() == "No"):      
				break			

ATM_Active = True					 #ATM is operational, each time it's out of operation we assume the CashReserves are replenished 
while(ATM_Active):
	ATM = ATMController(1000, 10000)
	print("Insert Card")
	ATM.ReadCard()
	if(ATM.IsValidAccount()):
		print("Enter 4 digit pin")
		AccessGranted = ATM.AccessAccount(input())
		if(not AccessGranted):
			continue                #Customer must rescan their card. Attempts may be counted at this point to restrict further attempts for security 
		ATM.CardNumber = None       #Once Account is verified, ATM removes customer's card number from memory, ready for the next customer
		ATM.BeginService()
	else:
		print("Account not found. Please visit your local bank")
