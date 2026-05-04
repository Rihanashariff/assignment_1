#Question 3
# Who are the top 10 customers by total account balance across all account types?

select customers.customer_id,customers.name,
SUM(account_balances.account_balance) AS total_balance #Adds up all account balances belonging to the same customer.
FROM customers
JOIN account_balances  #Joins customers with account_balances.
ON customers.customer_id=account_balances.customer_id
group by customers.customer_id,customers.name  #Groups all rows per customer.
ORDER BY total_balance DESC  #Sorts the results by total_balance.#DESC means highest balance first.
LIMIT 10;




