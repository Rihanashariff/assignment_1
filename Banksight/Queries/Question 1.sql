#Question 1
#How many customers exist per city, and what is their average account balance?
SELECT customers.city,
COUNT(customers.customer_id)AS   #Counts the number of customer records in each city.
TOTAL_CUSTOMERS,  #Result
AVG(account_balances.account_balance)AS AVERAGE_BALANCES  #Calculates the average account balance for customers in each city.
FROM customers
LEFT JOIN account_balances
ON customers.customer_id=account_balances.customer_id
group by customers.city;  #Groups all rows city-wise. 