#Question 2 
#Which account type (Savings, Current, Loan, etc.) holds the highest total balance?
SELECT customers.account_type,
SUM(account_balances.account_balance)AS total_balance  #calculates the total balance for that account type by adding all customers’ balances together.
FROM customers #The main table is customers because it contains the account_type column.
				#We will join this table with account_balances to get the balances.
JOIN account_balances #You are joining customers with account_balances, 
						#but the condition is comparing customers.customer_id to itself.
ON customers.customer_id=customers.customer_id
GROUP BY customers.account_type 	#Groups all rows by account_type.
ORDER by total_balance DESC			#Sorts the results in descending order of total balance.
										#The account type with the largest total balance appears first.
LIMIT 1;  #Only returns the top row, i.e., the account type with the highest total balance.

