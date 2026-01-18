import streamlit as st
import pandas as pd
import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="banksight",
    port=3306,
    autocommit=True
)

cursor = conn.cursor()


st.set_page_config(page_title="BankSight Dashboard", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 BankSight Navigation")

menu = st.sidebar.radio(
    "Go to:",
    [
        "🏠Introduction",
        "📊View Tables",
        "🔍Filter Data",
        "✏️ CRUD Operations",
        "💳Credit / Debit Simulation",
        "📈Analytical Insights",
        "👩‍💻About Creator",
    ]
)

# ---------------- MAIN CONTENT ----------------
if menu == "🏠Introduction":
    st.title("🏦 BankSight Transaction Intelligence Dashboard")

    st.subheader("Project Overview")
    st.write("""
    BankSight is a financial analytics system built using **Python, Streamlit, and MySQL**.
    It allows users to explore customer, account, transaction, loan, branches and support tickets,
    perform CRUD operations, simulate deposits/withdrawals, and view analytical insights.
    """)

    st.subheader("Objectives")
    st.markdown("""
    - Understand customer & transaction behavior  
    - Detect anomalies and fraud  
    - Enable CRUD operations  
    - Simulate banking transactions
    """)

# ---------------- VIEW TABLES ----------------
elif menu == "📊View Tables":
    st.header("📊 View Database Tables")

    tables = {
        "Customers": "customers.csv",
        "Accounts": "accounts.csv",
        "Loans": "loans.csv",
        "Transactions": "transactions.csv",
        "Branches": "branches.csv",
        "Support Tickets": "support_tickets.csv"
    }

    selected_table = st.selectbox("Select Table", tables.keys())
    df = pd.read_csv(tables[selected_table])
    st.dataframe(df, use_container_width=True)

#------------------Filter Tbales------------------------

elif menu == "🔍Filter Data":
    st.header("🔍 Filter Data")

    # Select table
    tables = st.selectbox(
        "Select Table to Filter",
        [
            "Customers",
            "Accounts",
            "Loans",
            "Transactions",
            "Branches",
            "Support Tickets"
        ],
        key="table_select"
    )

    # ---------- CUSTOMERS TABLE ----------
    if tables == "Customers":
        df = pd.read_csv("customers.csv")
        filtered_df = df.copy()

        st.subheader("Select columns and values to filter")

        # ---------- Customer ID Filter ----------
        customer_ids = df["customer_id"].astype(str).unique().tolist()
        selected_ids = st.multiselect(
            "Customer ID",
            options=customer_ids,
            key="customer_id_filter"
        )
        if selected_ids:
            filtered_df = filtered_df[
                filtered_df["customer_id"].astype(str).isin(selected_ids)
            ]
    #--------Name filter --------
        customer_name = df["name"].astype(str).unique().tolist()
        selected_ids = st.multiselect(
            "Name",
            options=customer_name,
            key="customer_name_filter"

        )
        # ---------- Gender Filter ----------
        selected_gender = st.multiselect(
            "Gender",
            options=df["gender"].dropna().unique(),
            key="gender_filter"
        )
        if selected_gender:
            filtered_df = filtered_df[
                filtered_df["gender"].isin(selected_gender)
            ]

        # ---------- Age Filter ----------
       # --- Age (User Input - Exact) ---
        age_input = st.number_input(
            "Enter Age",
            min_value=int(df["age"].min()),
            max_value=int(df["age"].max()),
            step=1,
            key="age_input"
)

        filtered_df = filtered_df[filtered_df["age"] == age_input]


        # ---------- City Filter ----------
        selected_city = st.multiselect(
            "City",
            options=df["city"].dropna().unique(),
            key="city_filter"
        )
        if selected_city:
            filtered_df = filtered_df[
                filtered_df["city"].isin(selected_city)
            ]

        # ---------- Account Type Filter ----------
        selected_account_type = st.multiselect(
            "Account Type",
            options=df["account_type"].dropna().unique(),
            key="account_type_filter"
        )
        if selected_account_type:
            filtered_df = filtered_df[
                filtered_df["account_type"].isin(selected_account_type)
            ]

        # ---------- Date Filter ----------
        filtered_df["join_date"] = pd.to_datetime(filtered_df["join_date"])
        min_date = filtered_df["join_date"].min()
        max_date = filtered_df["join_date"].max()
        date_range = st.date_input(
            "Join Date Range",
            value=(min_date, max_date),
            key="date_filter"
        )
        if len(date_range) == 2:
            filtered_df = filtered_df[
                filtered_df["join_date"].between(
                    pd.to_datetime(date_range[0]),
                    pd.to_datetime(date_range[1])
                )
            ]

        # ---------- Display Result ----------
        st.subheader("Filtered Customer Data")
        st.dataframe(filtered_df, use_container_width=True)

        # ---------- Summary ----------
        st.markdown("### 📊 Summary")
        st.write(f"**Total Customers:** {len(filtered_df)}")

    if tables == "Accounts":
        df = pd.read_csv("accounts.csv")
        df["last_updated"] = pd.to_datetime(df["last_updated"])
        filtered_df = df.copy()

        st.subheader("Filter Options")

        # -------- Customer ID --------
        selected_ids = st.multiselect(
            "Customer ID",
            df["customer_id"].astype(str).unique(),
            key="acc_customer_id"
        )

        if selected_ids:
            filtered_df = filtered_df[
                filtered_df["customer_id"].astype(str).isin(selected_ids)
            ]

        # -------- Account Balance --------
        balance_input = st.text_input(
            "Enter Account Balance Range (min,max)",
        placeholder="Eg: 1000.50, 50000.75"
)

        min_balance = float(df["account_balance"].min())
        max_balance = float(df["account_balance"].max())

        if balance_input:
            try:
        # Remove spaces
                clean_input = balance_input.replace(" ", "")

        # If only ONE number entered → exact balance
                if "," not in clean_input:
                    min_val = max_val = float(clean_input)
                else:
                    min_val, max_val = map(float, clean_input.split(","))

        # Validation
                if min_val > max_val:
                    st.warning("Min balance cannot be greater than max balance")
                else:
                    filtered_df = filtered_df.query(
                "account_balance >= @min_val and account_balance <= @max_val"
            )

            except ValueError:
                st.error("Please enter valid numbers like: 1000.50, 50000.75")


        # -------- Last Updated --------
        date_range = st.date_input(
            "Last Updated Date Range",
            (df["last_updated"].min(), df["last_updated"].max()),
            key="acc_date"
        )

        if len(date_range) == 2:
            filtered_df = filtered_df.query(
                "last_updated >= @date_range[0] and last_updated <= @date_range[1]"
            )

        # -------- Display --------
        st.subheader("Filtered Accounts Data")
        st.dataframe(filtered_df, use_container_width=True)

        st.markdown("### 📊 Summary")
        st.metric("Total Accounts", len(filtered_df))
        st.metric(
            "Average Balance",
            f"₹{filtered_df['account_balance'].mean():,.2f}"
        )

    if tables == "Loans":

        df = pd.read_csv("loans.csv")

    # ---- FIX DATE ISSUE HERE ----
        df["Start_Date"] = pd.to_datetime(df["Start_Date"], errors="coerce")
        df["End_Date"] = pd.to_datetime(df["End_Date"], errors="coerce")

        df = df.dropna(subset=["Start_Date", "End_Date"])

        filtered_df = df.copy()

    # --- Customer ID ---
        cust_ids = st.multiselect(
            "Customer ID",
            df["Customer_ID"].astype(str).unique(),
            key="loan_customer"
    )

        if cust_ids:
            filtered_df = filtered_df[
                filtered_df["Customer_ID"].astype(str).isin(cust_ids)
        ]
       #-------Load Id-------
        loan_ids = st.multiselect(
           "Loan ID",
           df["Loan_ID"].astype(str).unique(),
           key="loan_id"
       )
        if loan_ids:
            filtered_df = filtered_df[
                filtered_df["Loan_ID"].astype(str).isin(loan_ids)
            ]

      #---------aCCOUNT iD-----
        account_ids = st.multiselect(
           "Account ID",
           df["Account_ID"].astype(str).unique(),
           key="account_id"
       )
        if account_ids:
            filtered_df = filtered_df[
                filtered_df["Account_ID"].astype(str).isin(account_ids)
            ]

        #--------Branch------
        branch = st.multiselect(
            "Branch",
            df["Branch"].astype(str).unique(),
            key="branch"
        )
        if branch:
            filtered_df = filtered_df[
                filtered_df["Branch"].astype(str).isin(branch)
            ]

        #--------Interest Range--
        interest_rate=st.multiselect(
            "Interest Rate",
            df["Interest_Rate"].astype(str).unique(),
            key="interst rate"
        )
        if interest_rate:
               filtered_df = filtered_df[
                filtered_df["Interest_Rate"].astype(float).isin(interest_rate)
            ] 
    # --- Loan Type ---
        loan_types = st.multiselect(
            "Loan Type",
            df["Loan_Type"].unique(),
            key="loan_type"
    )

        if loan_types:
            filtered_df = filtered_df.query("Loan_Type in @loan_types")

    # --- Loan Status ---
        loan_status = st.multiselect(
            "Loan Status",
            df["Loan_Status"].unique(),
            key="loan_status"
    )

        if loan_status:
            filtered_df = filtered_df.query("Loan_Status in @loan_status")

    # --- Loan Amount ---
        loan_amt = st.number_input(
            "Enter Loan Amount",
            min_value=float(df["Loan_Amount"].min()),
            max_value=float(df["Loan_Amount"].max()),
            step=1000.0,
            key="loan_amount_input"
)

        filtered_df = filtered_df[filtered_df["Loan_Amount"] == loan_amt]

    # --- Date Range (NO ERROR NOW) ---
        date_range = st.date_input(
            "Loan Period",
            (df["Start_Date"].min().date(), df["End_Date"].max().date()),
            key="loan_date"
)

        if isinstance(date_range, tuple) and len(date_range) == 2:
            filtered_df = filtered_df[
                filtered_df["Start_Date"].dt.date.between(date_range[0], date_range[1])
    ]
    # --- Display ---
        st.dataframe(filtered_df, use_container_width=True)

    # --- Download ---
        st.download_button(
            "⬇️ Download Filtered Loans",
            filtered_df.to_csv(index=False),
            "filtered_loans.csv"
    )

    
    if tables == "Transactions":
        df = pd.read_csv("transactions.csv")

# Clean column names
        df.columns = df.columns.str.strip().str.lower()

# Convert date column
        df["txn_time"] = pd.to_datetime(df["txn_time"], errors="coerce")

# ---------------- FILTER WIDGETS ----------------

# Transaction ID
        txn_id = st.text_input("Transaction ID")

# Customer ID
        customer_id = st.text_input("Customer ID")

# Transaction Type
        txn_type = st.multiselect(
        "Transaction Type",
        df["txn_type"].unique()
)

# Status
        status = st.multiselect(
        "Status",
        df["status"].unique()
)

# Amount (typed input – no slider)
        min_amount = st.number_input("Min Amount", min_value=0.0, step=100.0)
        max_amount = st.number_input("Max Amount", min_value=0.0, step=100.0)

# Transaction Date
        start_date = st.date_input(
        "Transaction Date From",
        df["txn_time"].min().date()
)

        end_date = st.date_input(
        "Transaction Date To",
        df["txn_time"].max().date()
)

# ---------------- APPLY FILTERS ----------------

        filtered_df = df.copy()

        if txn_id:
            filtered_df = filtered_df[
            filtered_df["txn_id"].astype(str).str.contains(txn_id, case=False)
    ]

        if customer_id:
            filtered_df = filtered_df[
            filtered_df["customer_id"].astype(str).str.contains(customer_id, case=False)
    ]

        if txn_type:
            filtered_df = filtered_df[filtered_df["txn_type"].isin(txn_type)]

        if status:
            filtered_df = filtered_df[filtered_df["status"].isin(status)]

        if min_amount or max_amount:
            filtered_df = filtered_df[
            (filtered_df["amount"] >= min_amount) &
            (filtered_df["amount"] <= (max_amount if max_amount > 0 else filtered_df["amount"].max()))
    ]

        filtered_df = filtered_df[
        (filtered_df["txn_time"].dt.date >= start_date) &
        (filtered_df["txn_time"].dt.date <= end_date)
]
        st.dataframe(filtered_df)

    
    
    if tables == "Branches":

            df = pd.read_csv("branches.csv")    
        # Convert date column
            df["Opening_Date"] = pd.to_datetime(df["Opening_Date"], errors="coerce")
        # Branch ID
            branch_id_options = ["Choose an option"] + list(df["Branch_ID"].unique())
            branch_id = st.selectbox("Select Branch ID", branch_id_options, index=0)
        # Branch Name
            branch_name_options = ["Choose an option"] + list(df["Branch_Name"].unique())
            branch_name = st.selectbox("Select Branch Name", branch_name_options, index=0)

            city_options = ["Choose an option"] + list(df["City"].unique())
            city = st.selectbox("City", city_options, index=0)

        # Manager Name
            manager_name = st.selectbox(
            "Select Manager Name",
            ["Choose an option"] + list(df["Manager_Name"].unique()),
    index=0
)
        # Performance Rating
            performance_rating = st.multiselect(
            "Performance_Rating",
            sorted(df["Performance_Rating"].unique())
)
        
# Total Employees
            min_emp = st.number_input("Min Employees", min_value=0, step=1)
            max_emp = st.number_input("Max Employees", min_value=0, step=1)

# Branch Revenue (typed input – no slider)
            min_rev = st.number_input("Min Branch_Revenue", min_value=0.0, step=10000.0)
            max_rev = st.number_input("Max Branch_Revenue", min_value=0.0, step=10000.0)

# Opening Date
            start_date = st.date_input(
            "Opening Date From",
            df["Opening_Date"].min().date()
)

            end_date = st.date_input(
            "Opening Date To",
            df["Opening_Date"].max().date()
)

# ---------------- APPLY FILTERS ----------------

            filtered_df = df.copy()

            if branch_id:
               filtered_df = filtered_df[filtered_df["Branch_ID"] == branch_id]


            if branch_name:
                filtered_df = filtered_df[filtered_df["Branch_Name"] == branch_name]


            if city:
                filtered_df = filtered_df[filtered_df["City"] == city]

            if manager_name != "Choose an option":
                filtered_df = filtered_df[
                filtered_df["Manager_Name"] == manager_name
    ]

            if performance_rating:
                filtered_df = filtered_df[
                filtered_df["Performance_Rating"].isin(performance_rating)
    ]

            if min_emp or max_emp:
                filtered_df = filtered_df[
                (filtered_df["Total_Employees"] >= min_emp) &
                (filtered_df["Total_Employees"] <=
                (max_emp if max_emp > 0 else filtered_df["Total_Employees"].max()))
    ]

            if min_rev < max_rev:
                filtered_df = filtered_df[
                    (filtered_df["Branch_Revenue"] >= min_rev) &
                    (filtered_df["Branch_Revenue"] <= max_rev)
    ]


            filtered_df["Opening_Date"] = pd.to_datetime(
                    filtered_df["Opening_Date"], errors="coerce"

)
            if start_date and end_date:
                    filtered_df = filtered_df[
                        (filtered_df["Opening_Date"] >= pd.to_datetime(start_date)) &
                        (filtered_df["Opening_Date"] <= pd.to_datetime(end_date))
    ]
            if filtered_df.empty:
                    st.warning("No data found. Please adjust filters.")
            else:
                    st.dataframe(filtered_df)

    if tables =="Support Tickets":
      
        # Load your support tickets dataframe
            df = pd.read_csv("support_tickets.csv")

            filtered_df = df.copy()

# ---------------- ID FILTERS ----------------
            ticket_id = st.selectbox("Ticket ID",["Choose an option"] + list(df["Ticket_ID"].dropna().unique()),
            index=0
)
            customer_id = st.selectbox("Customer ID",["Choose an option"] + list(df["Customer_ID"].dropna().unique()),
            index = 0
    )
            account_id = st.selectbox("Account ID",["Choose an option"] + list(df["Account_ID"].dropna().unique()),
            index = 0
)
            loan_id  = st.selectbox ("Loan ID", ["Choose an option"] + list(df["Loan_ID"].dropna().unique()),
            index= 0
    )
            branch = st.selectbox("Branch Name",["Choose an option"] + list(filtered_df["Branch_Name"].dropna().unique()),
            index=0
            )    
            issue_category = st.selectbox("Issue Category",["Choose an option"] + list(filtered_df["Issue_Category"].dropna().unique()),
            index=0
            )      
            priority = st.selectbox("Priority",["Choose an option"] + list(filtered_df["Priority"].dropna().unique()),
            index=0
)
            status = st.selectbox("Status",["Choose an option"] + list(filtered_df["Status"].dropna().unique()),
            index=0
)
            channel = st.selectbox("Channel",["Choose an option"] + list(filtered_df["Channel"].dropna().unique()),
            index=0
)
            support_agent = st.selectbox("Support Agent",["Choose an option"] + list(filtered_df["Support_Agent"].dropna().unique()),
            index=0
)

            if ticket_id != "Choose an option":
                filtered_df = filtered_df[
                    filtered_df["Ticket_ID"] == ticket_id
    ]

            if customer_id != "Choose an option":
                filtered_df = filtered_df[
                filtered_df["Customer_ID"]== customer_id
    ]

            if account_id != "Choose an option":
                filtered_df = filtered_df[
                filtered_df["Account_ID"] == account_id
    ]

            if loan_id != "Choose an option":
                filtered_df = filtered_df[
                filtered_df["Loan_ID"]== loan_id
    ]
     
# Apply dropdown filters
            if branch != "Choose an option":
                filtered_df = filtered_df[filtered_df["Branch_Name"] == branch]

            if issue_category != "Choose an option":
                 filtered_df = filtered_df[filtered_df["Issue_Category"] == issue_category]

            if priority != "Choose an option":
                filtered_df = filtered_df[filtered_df["Priority"] == priority]

            if status != "Choose an option":
                filtered_df = filtered_df[filtered_df["Status"] == status]

            if channel != "Choose an option":
                filtered_df = filtered_df[filtered_df["Channel"] == channel]

            if support_agent != "Choose an option":
                filtered_df = filtered_df[filtered_df["Support_Agent"] == support_agent]

# ---------------- DATE FILTERS ----------------
            filtered_df["Date_Opened"] = pd.to_datetime(filtered_df["Date_Opened"], errors="coerce")
            filtered_df["Date_Closed"] = pd.to_datetime(filtered_df["Date_Closed"], errors="coerce")

            col1, col2 = st.columns(2)
            with col1:
                opened_from = st.date_input("Opened Date From")
            with col2:
                opened_to = st.date_input("Opened Date To")

            if opened_from and opened_to:
                filtered_df = filtered_df[
                (filtered_df["Date_Opened"] >= pd.to_datetime(opened_from)) &
                (filtered_df["Date_Opened"] <= pd.to_datetime(opened_to))
    ]

# ---------------- RATING FILTER ----------------
            rating = st.multiselect(
            "Customer Rating",
            sorted(filtered_df["Customer_Rating"].dropna().unique())
)

            if rating:
                filtered_df = filtered_df[
                filtered_df["Customer_Rating"].isin(rating)
    ]

# ---------------- RESULT ----------------
            if filtered_df.empty:
                st.warning("No support tickets found. Adjust filters.")
            else:
                st.dataframe(filtered_df)


            
# ---------------- CRUD ----------------
elif menu == "✏️ CRUD Operations":
    def load_csv(file):
        return pd.read_csv(file)

    def save_csv(df, file):
        df.to_csv(file, index=False)

    st.header("✏️ CRUD Operations")

    table_map = {
        "Customers": "customers.csv",
        "Accounts": "accounts.csv",
        "Loans": "loans.csv",
        "Transactions": "transactions.csv",
        "Branches": "branches.csv",
        "Support Tickets": "support_tickets.csv"
    }

    table = st.selectbox("Select Table", table_map.keys())
    file = table_map[table]

    df = load_csv(file)
    operation = st.radio(
        "Select Operation",
        ["View", "Add", "Update", "Delete"]
    )
    if operation == "View":
        st.subheader(f"📄 View {table}")
        st.dataframe(df, use_container_width=True)

    elif operation == "Add":
        st.subheader(f"➕ Add New Record to {table}")

        new_data = {}

        for col in df.columns:
            new_data[col] = st.text_input(f"Enter {col}")

        if st.button("Add Record"):
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            save_csv(df, file)
            st.success("Record added successfully ✅")

    elif operation == "Update":
        st.subheader(f"✏️ Update Record in {table}")

        id_col = df.columns[0]

        record_id = st.selectbox(
            f"Select {id_col} to update",
            df[id_col].astype(str)
        )

        column = st.selectbox(
            "Select Column to Update",
            df.columns
        )

        new_value = st.text_input("Enter New Value")

        if st.button("Update Record"):
            df.loc[df[id_col].astype(str) == record_id, column] = new_value
            save_csv(df, file)
            st.success("Record updated successfully ✅")

    elif operation == "Delete":
        st.subheader(f"🗑️ Delete Record from {table}")

        id_col = df.columns[0]

        record_id = st.selectbox(
            f"Select {id_col} to delete",
            df[id_col].astype(str)
        )

        if st.button("Delete Record"):
            df = df[df[id_col].astype(str) != record_id]
            save_csv(df, file)
            st.success("Record deleted successfully ❌")

# ---------------- SIMULATION ----------------
elif "Credit / Debit" in menu:

    st.header("💳Credit / Debit Simulation")

    df = pd.read_csv("credit_cards.csv")

    filtered_df = df.copy()

    acc_id = st.multiselect(
           "Enter Account ID",
           df["Account_ID"].astype(str).unique(),
           key="account_id"
       )
    if acc_id:
        filtered_df = filtered_df[
            filtered_df["Account_ID"].astype(str).isin(acc_id)
            ]
        amt = st.number_input("Enter Amount (₹)", min_value=0.0)
        action = st.radio("Action", ["Check Balance", "Deposit", "Withdraw"])

    if st.button("Submit"):
        if acc_id not in df["Account_ID"].astype(str).values:
            st.error("Account not found")
        else:
            i = df[df["Account_ID"].astype(str).isin(acc_id)].index[0]
            bal = df.at[i, "Current_Balance"]

            if action == "Check Balance":
                st.info(f"💰 Current Balance: ₹{bal:.2f}")

            elif action == "Deposit":
                df.at[i, "Current_Balance"] = bal+ amt
                st.success(f"✅ Amount Deposited : ₹{amt:,.2f}. "
                           f"New Balance : ₹{df.at[i, 'Current_Balance']:,.2f}")

            elif action == "Withdraw":
                if amt > bal:
                    st.error("❌ Insufficient Balance")
                else:
                    df.at[i, "Current_Balance"] =bal - amt
                    st.success(f"✅ Amount Withdrawn₹{amt:,.2f}."
                            f"New Balance: ₹{df.at[i, 'Current_Balance']:,.2f}")

            df.to_csv("credit_cards.csv", index=False)




# ---------------- ANALYTICS ----------------

elif menu == "📈Analytical Insights":
    st.header("📈Analytical Insights")
    questions = st.selectbox(
        "Select an Analytical Questions",
        [
            "Q1:How many customers exist per city, and what is their average account balance?",
            "Q2:Which account type (Savings, Current, Loan, etc.) holds the highest total balance?",
            "Q3:Who are the top 10 customers by total account balance across all account types?",
            "Q4:Which customers opened accounts in 2023 with a balance above ₹1,00,000?",
            "Q5:What is the total transaction volume (sum of amounts) by transaction type?",
            "Q6:How many failed transactions occurred for each transaction type?",
            "Q7:What is the total number of transactions per transaction type?",
            "Q8:Which accounts have 5 or more high-value transactions above ₹20,000?",
            "Q9:What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?",
            "Q10:Which customers currently hold more than one active or approved loan?",
            "Q11:Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?",
            "Q12:What is the average loan amount per branch?",
            "Q13:How many customers exist in each age group (e.g., 18–25, 26–35, etc.)?",
            "Q14:Which issue categories have the longest average resolution time?",
            "Q15:Which support agents have resolved the most critical tickets with high customer ratings (≥4)?"
        ]
)
   
    if questions =="Q1:How many customers exist per city, and what is their average account balance?":
             
            query= """
            SELECT 
                c.city,
                COUNT(DISTINCT c.customer_id) AS total_customers,
                AVG(a.account_balance) AS average_balance
            FROM customers c
            LEFT JOIN accounts a
                ON c.customer_id = a.customer_id
            GROUP BY c.city;
        """


    elif questions == "Q2:Which account type (Savings, Current, Loan, etc.) holds the highest total balance?":
            query = """
           SELECT 
                c.account_type,
                SUM(a.account_balance) AS total_balance
            FROM customers c
            JOIN accounts a ON c.customer_id = a.customer_id
            GROUP BY c.account_type
            ORDER BY total_balance DESC
            LIMIT 1;

        """
    elif questions == "Q3:Who are the top 10 customers by total account balance across all account types?":
            query = """
            SELECT 
                c.customer_id,
                c.name,
                SUM(a.account_balance) AS total_balance
            FROM customers c
            JOIN accounts a
                ON c.customer_id = a.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_balance DESC
            LIMIT 10;
            """
    elif questions == "Q4:Which customers opened accounts in 2023 with a balance above ₹1,00,000?":
        
            query = """
            SELECT 
                c.customer_id,
                c.name,
                c.join_date,
                a.account_balance
            FROM accounts a
            JOIN customers c
                ON a.customer_id = c.customer_id
            WHERE YEAR(c.join_date) = 2023
                AND a.account_balance > 100000;
        """
    elif questions == "Q5:What is the total transaction volume (sum of amounts) by transaction type?":
            query = """
            SELECT 
                txn_type,
                SUM(amount) AS total_volume
            FROM transactions
            GROUP BY txn_type;
        """
    elif questions == "Q6:How many failed transactions occurred for each transaction type?":
            query = """ 
            SELECT 
                txn_type,
                COUNT(*) AS failed_count
            FROM transactions
            WHERE status = 'Failed'
            GROUP BY txn_type;
        """
    elif questions == "Q7:What is the total number of transactions per transaction type?":
            query="""
            SELECT 
                txn_type,
                COUNT(*) AS total_transactions
            FROM transactions
            GROUP BY txn_type;

        """
    elif questions == "Q8:Which accounts have 5 or more high-value transactions above ₹20,000?":
            query = """  
            SELECT 
                customer_id,
                COUNT(*) AS high_value_txn
            FROM transactions
            WHERE amount > 20000
            GROUP BY customer_id
            HAVING COUNT(*) >= 5;
            """
    elif questions == "Q9:What is the average loan amount and interest rate by loan type (Personal, Auto, Home, etc.)?":
            query="""
            SELECT 
                Loan_Type,
                AVG(Loan_Amount) AS avg_Loan_Amount,
                AVG(Interest_Rate) AS avg_Interest_Rate
            FROM loans
            GROUP BY Loan_Type;
            """
    elif questions == "Q10:Which customers currently hold more than one active or approved loan?":
            query="""
            SELECT 
                Customer_ID,
                COUNT(*) AS total_loans
            FROM loans
            WHERE Loan_Status IN ('Active', 'Approved')
            GROUP BY Customer_ID
            HAVING COUNT(*) > 1;
        """
    elif questions == "Q11:Who are the top 5 customers with the highest outstanding (non-closed) loan amounts?":
            query = """
            SELECT 
                l.customer_id,
                c.name,
                SUM(l.Loan_Amount) AS total_outstanding_loan
            FROM loans l
            JOIN customers c
                ON c.customer_id = l.Customer_ID
            WHERE l.Loan_Status <> 'Closed'
            GROUP BY l.Customer_ID, c.name
            ORDER BY total_outstanding_loan DESC
            LIMIT 5;
        """
    elif questions =="Q12:What is the average loan amount per branch?":
            query = """
            SELECT
                branch,
                AVG(loan_amount) AS avg_loan_amount
            FROM loans
            GROUP BY branch
            ORDER BY avg_loan_amount DESC;
        
        """
    elif questions == "Q13:How many customers exist in each age group (e.g., 18–25, 26–35, etc.)?":
            query = """
            SELECT
                CASE
                    WHEN age BETWEEN 18 AND 25 THEN '18–25'
                    WHEN age BETWEEN 26 AND 35 THEN '26–35'
                    WHEN age BETWEEN 36 AND 45 THEN '36–45'
                    WHEN age BETWEEN 46 AND 55 THEN '46–55'
                    WHEN age >= 56 THEN '56+'
                    ELSE 'Unknown'
                END AS age_group,
                COUNT(*) AS total_customers
            FROM customers
            GROUP BY age_group
            ORDER BY age_group;
        """
    elif questions == "Q14:Which issue categories have the longest average resolution time?":
            query="""
            SELECT
                issue_category,
                AVG(DATEDIFF(date_closed, date_opened)) AS avg_resolution_days
            FROM support_tickets
            WHERE date_closed IS NOT NULL
                AND date_opened IS NOT NULL
            GROUP BY issue_category
            ORDER BY avg_resolution_days DESC;
         """
    elif questions == "Q15:Which support agents have resolved the most critical tickets with high customer ratings (≥4)?":
            query = """
            SELECT
                support_agent,
                COUNT(*) AS resolved_critical_tickets
            FROM support_tickets
            WHERE priority = 'Critical'
                AND customer_rating >= 4
                AND status IN ('Resolved', 'Closed')
            GROUP BY support_agent
            ORDER BY resolved_critical_tickets DESC;
        """
  
    
    if st.button("▶ Run"):
        try:

            df = pd.read_sql(query, conn)
            if df.empty:
                st.warning("No data returned for this query.")
            else:
                st.success("Query executed successfully ✅")
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error("Error executing query")
            st.exception(e)
# ---------------- ABOUT ----------------
elif menu == "👩‍💻About Creator":
    st.header("👩‍💻About the Creator")

    st.write("**Name: Rihana Shariff**")
    st.write("**Email: shariffrihan@gmail.com**")
    st.write("**Project: 🏦 BankSight: Transaction Intelligence Dashboard**")

    st.markdown(
        """
            This dashboard showcases end-to-end data handling —
        from CSV ingestion and MySQL integration to SQL analytics
        and interactive Streamlit visualizations.
        """
    )

    st.success("Thank you for exploring the BankSight Dashboard 🚀")
