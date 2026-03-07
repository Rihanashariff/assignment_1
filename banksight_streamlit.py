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


if menu == "🏠Introduction":
    st.title("🏦 BankSight Transaction Intelligence Dashboard")
    st.subheader("Project Overview")
    st.write("""
    BankSight – Transaction  Intelligence  Dashboard is an interactive 
    banking analytics application designed to monitor, analyze, and manage customer
    transactions in real time.   It integrates multiple  banking datasets   to provide
    insights into customer behavior,account activity, loan performance, and operational
    efficiency through dynamic dashboards and SQL-driven analysis,account activity, loan
    performance, and operational efficiency through dynamic dashboard.""")

    st.subheader("Objectives")
    st.markdown("""
    - Understand customer & transaction behavior 
    - To provide a centralized view of banking data 
    - To enable data filtering and CRUD operations  
    - Simulate basic banking transactions
    - To generate analytical insights using SQL queries""")

    st.subheader("Technologies Used ")
    st.write("""
             1.Python 
             2.Pandas
             3.SQL 
             4.Streamlit """)

# ---------------- VIEW TABLES ----------------
elif menu == "📊View Tables":
    st.header("📊 View Database Tables")

    tables = {
        "Customers": "customers.csv",
        "Accounts": "accounts.csv",
        "Loans": "loans.csv",
        "Transactions": "transactions.csv",
        "Branches": "branches.csv",
        "Support Tickets": "support_tickets.csv",
        "Credit Cards" : "credit_cards.csv"
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
            "Support Tickets",
            "Credit Cards"
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
   
        age_input = st.text_input("Enter Age :")

        if age_input:  
            try:
                age_input = int(age_input)
                filtered_df = filtered_df[filtered_df["age"] == age_input]
            except ValueError:
                st.error("Please enter a valid number for age.")

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
    

        filtered_df["join_date"] = pd.to_datetime(
            filtered_df["join_date"], errors="coerce"
)

            # Remove NaT before getting min/max
        valid_dates = filtered_df["join_date"].dropna()

        if not valid_dates.empty:

            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            date_range = st.date_input(
                "Join Date Range",
                value=(min_date, max_date),
                key="date_filter"
    )

            if isinstance(date_range, tuple) and len(date_range) == 2:
                filtered_df = filtered_df[
                    filtered_df["join_date"].dt.date.between(
                        date_range[0],
                        date_range[1]
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
       
                clean_input = balance_input.replace(" ", "")

       
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
                min_value=0.0,
                step=1000.0
)

        if loan_amt:
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
    
        txn_id = st.multiselect(
             "Transaction ID",
             df["txn_id"].unique()
    )

# Customer ID
        customer_id = st.multiselect(
             "Customer ID",
             df["customer_id"].unique()
    )

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
                filtered_df["txn_id"].astype(str).isin(txn_id)]

        if customer_id:
            filtered_df = filtered_df[
                filtered_df["customer_id"].astype(str).isin(customer_id)]

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

    # --- Download ---
        st.download_button(
            "⬇️ Download Filtered Transactions",
            filtered_df.to_csv(index=False),
            "transactions.csv"
    )
    
    if tables == "Branches":

        df = pd.read_csv("branches.csv")
        df["Opening_Date"] = pd.to_datetime(df["Opening_Date"], errors="coerce")

        filtered_df = df.copy()

    # ---------------- MULTISELECT FILTERS ----------------

        branch_id = st.multiselect(
            "Branch ID",
            sorted(df["Branch_ID"].astype(int).unique())
    )

        branch_name = st.multiselect(
            "Branch Name",
            sorted(df["Branch_Name"].dropna().unique())
    )

        city = st.multiselect(
            "City",
            sorted(df["City"].dropna().unique())
    )

        manager_name = st.multiselect(
            "Manager Name",
            sorted(df["Manager_Name"].dropna().unique())
    )

        performance_rating = st.multiselect(
            "Performance Rating",
            sorted(df["Performance_Rating"].dropna().unique())
    )

        min_emp = st.number_input("Min Employees", min_value=0, step=1)
        max_emp = st.number_input("Max Employees", min_value=0, step=1)

        min_rev = st.number_input("Min Branch Revenue", min_value=0.0, step=10000.0)
        max_rev = st.number_input("Max Branch Revenue", min_value=0.0, step=10000.0)

        start_date = st.date_input("Opening Date From", df["Opening_Date"].min().date())
        end_date = st.date_input("Opening Date To", df["Opening_Date"].max().date())

    # ---------------- APPLY FILTERS ----------------

        if branch_id:
            filtered_df = filtered_df[
                filtered_df["Branch_ID"].isin(branch_id)
        ]

        if branch_name:
            filtered_df = filtered_df[
                filtered_df["Branch_Name"].isin(branch_name)
        ]

        if city:
            filtered_df = filtered_df[
                filtered_df["City"].isin(city)
        ]

        if manager_name:
            filtered_df = filtered_df[
                filtered_df["Manager_Name"].isin(manager_name)
        ]

        if performance_rating:
            filtered_df = filtered_df[
                filtered_df["Performance_Rating"].isin(performance_rating)
        ]

        if min_emp or max_emp:
            max_val = max_emp if max_emp > 0 else filtered_df["Total_Employees"].max()
            filtered_df = filtered_df[
                (filtered_df["Total_Employees"] >= min_emp) &
                (filtered_df["Total_Employees"] <= max_val)
        ]

        if min_rev or max_rev:
            max_val = max_rev if max_rev > 0 else filtered_df["Branch_Revenue"].max()
            filtered_df = filtered_df[
                (filtered_df["Branch_Revenue"] >= min_rev) &
                (filtered_df["Branch_Revenue"] <= max_val)
        ]

        filtered_df = filtered_df[
            (filtered_df["Opening_Date"].dt.date >= start_date) &
            (filtered_df["Opening_Date"].dt.date <= end_date)
    ]

    # ---------------- RESULT ----------------

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

    if tables == "Credit Cards":

        df = pd.read_csv("credit_cards.csv")
        df["Customer_ID"] = "C" + df["Customer_ID"].astype(str)

        filtered_df = df.copy()

    # Customer ID filter
        customer_id = st.multiselect("Customer ID",
        df["Customer_ID"].astype(str).unique()
    )

        if customer_id:
            filtered_df = filtered_df[
                filtered_df["Customer_ID"].astype(str).isin(customer_id)
        ]

    # Account ID
        account_id = st.multiselect("Account ID",
        df["Account_ID"].astype(str).unique()
    )

        if account_id:
            filtered_df = filtered_df[
                filtered_df["Account_ID"].astype(str).isin(account_id)
        ]

    # Card Type
        card_type = st.multiselect("Card Type",
        df["Card_Type"].unique()
    )

        if card_type:
            filtered_df = filtered_df[
                filtered_df["Card_Type"].isin(card_type)
        ]

    # Card Network
        network = st.multiselect("Card Network",
        df["Card_Network"].unique()
    )

        if network:
            filtered_df = filtered_df[
                filtered_df["Card_Network"].isin(network)
        ]

    # Credit Limit
        min_limit = st.number_input("Min Credit Limit", min_value=0.0)
        max_limit = st.number_input("Max Credit Limit", min_value=0.0)

        if min_limit or max_limit:
            filtered_df = filtered_df[
                (filtered_df["Credit_Limit"] >= min_limit) &
                (filtered_df["Credit_Limit"] <= (max_limit if max_limit > 0 else filtered_df["Credit_Limit"].max()))]

    # Status
        status = st.multiselect("Status",
        df["Status"].unique()
    )

        if status:
            filtered_df = filtered_df[
                filtered_df["Status"].isin(status)
        ]

        st.dataframe(filtered_df)
         

            
# ---------------- CRUD ----------------
elif menu == "✏️ CRUD Operations":

    st.header("✏️ CRUD Operations")

    table = st.selectbox(
        "Select Table",
        ["customers", "accounts", "loans", "transactions", "branches", "support_tickets","credit_cards"]
    )

    operation = st.radio(
        "Select Operation",
        ["View", "Add", "Update", "Delete"]
    )

    # ---------------- VIEW ----------------
    if operation == "View":
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)

    # ---------------- ADD ----------------
    elif operation == "Add":

        if table == "customers":
            st.subheader("➕ Add New Customer")

            customer_id = st.text_input("Customer ID")
            name = st.text_input("Name")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            age = st.number_input("Age", min_value=18, max_value=100)
            city = st.text_input("City")
            account_type = st.selectbox("Account Type", ["Savings", "Current"])
            join_date = st.date_input("Join Date")

            if st.button("Add Customer"):
                    query = """
                    INSERT INTO customers
                    (customer_id, name, gender, age, city, account_type, join_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    cursor.execute(query, (
                        customer_id,
                        name,
                        gender,
                        age,
                        city,
                        account_type,
                        join_date
                    ))

                    conn.commit()
                    st.success("✅ Customer added successfully!")


                # accounts table (Add)
        elif table == "accounts":
            st.subheader("➕ Add New Account")

            customer_id = st.text_input("Customer ID")
            account_balance = st.number_input("Account Balance", min_value=0.0)
            last_updated = st.date_input("Last Updated")

            if st.button("Add Account"):
                    query = """
                    INSERT INTO accounts
                    (customer_id, account_balance, last_updated)
                    VALUES (%s, %s, %s)
                    """

                    cursor.execute(query, (
                        customer_id,
                        account_balance,
                        last_updated
            ))

                    conn.commit()
                    st.success("✅ Account added successfully!")

                # Loans (Add)
        
        elif table == "loans":
            st.subheader("➕ Add New Loan")

            with st.form("loan_form"):

                loan_id = st.text_input("Loan ID")

                cursor.execute("SELECT customer_id FROM loans")
                customer_ids = [row[0] for row in cursor.fetchall()]
                customer_id = st.selectbox("Select Customer ID", customer_ids)

                account_id=st.text_input("Account ID")

                cursor.execute("SELECT DISTINCT Branch FROM loans")
                branches = [row[0] for row in cursor.fetchall()]
                branch = st.selectbox("Branch", branches)

                loan_type = st.selectbox("Loan Type", ["Home", "Personal", "Auto", "Education", "Business"])
                loan_amount = st.number_input("Loan Amount", min_value=0.0)
                interest_rate = st.number_input("Interest Rate (%)", min_value=0.0)
                loan_term = st.number_input("Loan Term (Months)", min_value=1)
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                loan_status = st.selectbox("Loan Status", ["Active", "Closed", "Defaulted"])
                submit_btn = st.form_submit_button("Add Loan")

            if submit_btn:
                cursor.execute("SELECT loan_id FROM loans ORDER BY loan_id DESC LIMIT 1")
                last = cursor.fetchone()

                if last:
                    loan_id = last[0] + 1
                else:
                    loan_id = 1
                cursor.execute("""INSERT INTO loans
                    (Loan_ID, Customer_ID, Account_ID, Branch, Loan_Type,
                    Loan_Amount, Interest_Rate, Loan_Term_Months,
                    Start_Date, End_Date, Loan_Status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (loan_id, customer_id, account_id, branch, loan_type,loan_amount, interest_rate, loan_term,
                    start_date, end_date, loan_status))

                conn.commit()
                st.success("✅ Loan added successfully!")

                #transactions (add)
        elif table == "transactions":
            st.subheader("➕ Add Transaction")

            with st.form("add_transaction"):

                cursor.execute("SELECT customer_id FROM customers")
                customer_ids = [row[0] for row in cursor.fetchall()]
                customer_id = st.selectbox("Select Customer ID", customer_ids)

                txn_type = st.selectbox("Transaction Type", ["deposit", "withdrawal", "transfer"])
                amount = st.number_input("Amount", min_value=0.0, step=0.01)
                txn_time = st.date_input("Transaction Date")
                status = st.selectbox("Status", ["Success", "Failed", "Pending"])

                submit_btn = st.form_submit_button("Add Transaction")

                if submit_btn:
        #  AUTO GENERATE TRANSACTION ID
                    cursor.execute("SELECT txn_id FROM transactions ORDER BY CAST(SUBSTRING(txn_id,2) AS UNSIGNED) DESC LIMIT 1")
                    last_txn = cursor.fetchone()

                    if last_txn:
                        last_number = int(last_txn[0][1:])   # Remove 'T' and get number
                        new_number = last_number + 1
                        txn_id = f"T{new_number:05d}"       # Format like T00001
                    else:
                        txn_id = "T00001"   # First transaction

        # Insert into database
                    cursor.execute( """
                        INSERT INTO transactions 
                        (txn_id, customer_id, txn_type, amount, txn_time, status)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (txn_id, customer_id, txn_type, amount, txn_time, status)
        )

                    conn.commit()
                    st.success(f"✅ Transaction Added Successfully with ID: {txn_id}")

        elif table == "branches":

            st.subheader("➕ Add Branch")

            with st.form("add_branch"):

                Branch_Name = st.text_input("Branch Name")
                City = st.text_input("City")
                Manager_Name = st.text_input("Manager Name")
                Total_Employees = st.number_input("Total Employees", min_value=0)
                Branch_Revenue = st.number_input("Branch Revenue", min_value=0.0)
                Opening_Date = st.date_input("Opening Date")
                Performance_Rating = st.slider("Performance Rating (1-5)", 1, 5, 3)

                submit_btn = st.form_submit_button("Add Branch")

            if submit_btn:
            # Generate New Branch ID
                cursor.execute("""SELECT MAX(CAST(Branch_ID AS UNSIGNED))FROM branches""")
                result = cursor.fetchone()

                if result[0] is not None:
                    new_id = result[0] + 1
                else:
                    new_id = 1
                while True:
                    cursor.execute("SELECT 1 FROM branches WHERE Branch_ID = %s", (new_id,))
                    exists = cursor.fetchone()

                    if exists:
                        new_id += 1
                    else:
                        break
                new_branch_id = new_id

        # 🔹 Insert into Database
                cursor.execute("""
                    INSERT INTO branches
                    (Branch_ID, Branch_Name, City, Manager_Name,
                    Total_Employees, Branch_Revenue,
                    Opening_Date, Performance_Rating)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                new_branch_id,Branch_Name,City,Manager_Name,Total_Employees,Branch_Revenue,Opening_Date,
                Performance_Rating
            )
        )

                conn.commit()
                st.success(f"✅ Branch Added Successfully with ID: {new_branch_id}")

        elif table == "support_tickets":
            st.subheader("➕ Add Support Ticket")
            with st.form("add_support_ticket"):
                    cursor.execute("SELECT customer_id FROM customers")
                    customer_ids = [row[0] for row in cursor.fetchall()]
                    customer_id = st.selectbox("Select Customer ID", customer_ids)

                    def get_values(col):
                        cursor.execute(f"SELECT DISTINCT {col} FROM support_tickets")
                        data = [row[0] for row in cursor.fetchall()]
                        return data if data else ["General"]
                    account_id = st.text_input("Account_id")
                    loan_ID = st.text_input("Loan_ID")
                    branch_name = st.selectbox("Branch Name",get_values("Branch_Name"))
                    issue_category = st.selectbox("Issue Category", get_values("Issue_Category"))
                    description = st.selectbox("Description", get_values("Description"))
                    priority = st.selectbox("Priority", get_values("Priority"))
                    status = st.selectbox("Status", get_values("Status"))
                    resolution_remarks =st.selectbox("Resolution_Remarks",get_values("Resolution_Remarks"))
                    support_agent = st.text_input("Support_Agent")
                    channel = st.selectbox("Channel", get_values("Channel"))
                    date_opened = st.date_input("Date_Opened")
                    date_closed = st.date_input("Date_Closed")
                    customer_rating = st.selectbox("Customer_Rating",[1,2,3,4,5])

                    submit_btn = st.form_submit_button("Add Support Ticket")

            if submit_btn:
                    cursor.execute("SELECT Ticket_ID FROM support_tickets ORDER BY Ticket_ID DESC LIMIT 1")
                    last = cursor.fetchone()
                    if last:
                        new_number = int(last[0][1:]) + 1
                    else:
                        new_number = 1

                    ticket_id = f"T{new_number:05d}"
                    st.write(f"Ticket ID: {ticket_id}")
                

                    cursor.execute("""
                        INSERT INTO support_tickets(Ticket_ID, Customer_ID, Account_id, Loan_ID, Branch_Name,
                        Issue_Category, Description, Priority, Status,Resolution_Remarks, Support_Agent, Channel,
                        Date_Opened, Date_Closed, Customer_Rating)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", 
                        (ticket_id,customer_id,account_id,loan_ID,branch_name,issue_category,description,priority,status,
                        resolution_remarks,support_agent,channel,date_opened,date_closed,customer_rating))

                    conn.commit()
                    st.success(f"✅ Ticket Added Successfully: {ticket_id}")

        elif table == "credit_cards":
            st.subheader("➕ Add Credit Card")

            with st.form("add_card"):
                cursor.execute("SELECT DISTINCT Customer_ID FROM credit_cards")
                customer_ids = [row[0] for row in cursor.fetchall()]
                customer_id = st.selectbox("Customer ID", customer_ids)

                cursor.execute("SELECT DISTINCT Branch FROM credit_cards")
                branches = [row[0] for row in cursor.fetchall()]
                branch = st.selectbox("Branch", branches)

                account_id = st.text_input("Account Id")
                card_number = st.text_input("Card Number")
                card_type = st.selectbox("Card Type", ["Business", "Gold", "Platinum", "Silver"])
                card_network = st.selectbox("Card Network", ["Visa", "MasterCard", "RuPay", "Amex"])
                credit_limit = st.number_input("Credit Limit", min_value=0.0)
                current_balance= st.number_input("Current Balance",min_value=0.0)
                issued_date = st.date_input("Issued Date")
                expiry_date = st.date_input("Expiry Date")
                status = st.selectbox("Status", ["Active", "Blocked", "Expired"])

                submit = st.form_submit_button("Add Card")

                if submit:
                    cursor.execute("SELECT MAX(Card_ID) FROM credit_cards")
                    last = cursor.fetchone()
                    card_id = last[0] + 1 if last[0] else 1

                    cursor.execute("""INSERT INTO credit_cards
                        (Card_ID, Account_ID,Customer_ID, Branch, Card_Number,
                        Card_Type, Card_Network, Credit_Limit, Current_Balance,
                        Issued_Date, Expiry_Date, Status)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (card_id, account_id, customer_id, branch, card_number,
                        card_type, card_network, credit_limit, current_balance,
                        issued_date, expiry_date, status))

                    conn.commit()
                    st.success("✅ Credit Card Added Successfully!")


    # ---------------- UPDATE ----------------
    elif operation == "Update":
        
        if table == "customers":
            st.subheader("✏️ Update Customer Details")
            cursor.execute("SELECT customer_id FROM customers")
            ids = [row[0] for row in cursor.fetchall()]
            cid = st.selectbox("Select Customer ID", ids)
            cursor.execute("SELECT name, gender, age, city, account_type, join_date FROM customers WHERE customer_id = %s", (cid,))
            data = cursor.fetchone()

            if data:
                name, gender, age, city, account_type, join_date = data
                new_name = st.text_input("Name", value=name)
                new_gender = st.selectbox("Gender", ["M", "F"], index=0 if gender == "M" else 1)
                new_age = st.number_input("Age", min_value=1, max_value=120, value=int(age))
                
                cursor.execute("SELECT DISTINCT city FROM customers")
                city_list = [row[0] for row in cursor.fetchall()]
                new_city = st.selectbox("City", options=city_list, index=city_list.index(city))
                
                new_account_type = st.selectbox("Account Type", ["Savings", "Current"], index=0 if account_type == "Savings" else 1)
                new_join_date = st.date_input("Join Date", value=join_date)

            if st.button("Update Customer"):
                    query = """
                    UPDATE customers
                    SET name = %s,gender = %s,age = %s,city = %s,account_type = %s,join_date = %s
                    WHERE customer_id = %s  """

                    cursor.execute(query, (new_name,new_gender,new_age,new_city,new_account_type,new_join_date,
                    cid))

                    conn.commit()
                    st.success("✅ Customer updated successfully!")
        elif table == "accounts":
            st.subheader("Update Account Balance")

            cursor.execute("SELECT customer_id FROM accounts")
            ids = [i[0] for i in cursor.fetchall()]

            cid = st.selectbox("Customer ID", ids)

            cursor.execute("SELECT account_balance FROM accounts WHERE customer_id=%s", (cid,))
            balance = cursor.fetchone()[0]

            new_balance = st.number_input("New Balance", value=float(balance), step=100.0)

            if st.button("Update"):
                cursor.execute(
                "UPDATE accounts SET account_balance=%s, last_updated=NOW() WHERE customer_id=%s",
                (new_balance, cid))
                conn.commit()
                st.success("✅ Balance Updated")

        elif table == "loans":
            st.subheader("Update Loan info")
            cursor.execute("SELECT Customer_ID FROM loans")
            cids = [i[0] for i in cursor.fetchall()]
            cid = st.selectbox("Customer ID", cids)

            cursor.execute("SELECT Loan_ID FROM loans WHERE Customer_ID=%s", (cid,))
            loan_ids = [i[0] for i in cursor.fetchall()]
            lid = st.selectbox("Loan ID", loan_ids)
            
            cursor.execute("SELECT Account_ID, Branch, Loan_Type, Loan_Amount, Interest_Rate, Loan_Term_Months,Start_Date, End_Date, Loan_Status FROM loans WHERE customer_id = %s", (cid,))
            data = cursor.fetchone()
            if data:
                account_id, branch, loan_type, loan_amount, interest_rate, loan_term, start_date, end_date, loan_status = data
                new_account = st.text_input("Account ID", value=account_id)

                cursor.execute("SELECT DISTINCT Branch FROM loans")
                branches = [row[0] for row in cursor.fetchall()]
                new_branch = st.selectbox("Branch", branches)

                new_loan_type = st.selectbox(
                    "Loan Type",
                    ["Home", "Personal", "Auto", "Education", "Business"],
                    index=["Home","Personal","Auto","Education","Business"].index(loan_type))   
                new_amount = st.number_input("Loan Amount", value=float(loan_amount))
                new_interest = st.number_input("Interest Rate", value=float(interest_rate))
                new_term = st.number_input("Loan Term (Months)", value=int(loan_term))
                new_start_date = st.date_input("Start Date", value=start_date)
                new_end_date = st.date_input("End Date", value=end_date)
                new_status = st.selectbox("Loan Status",
                        ["Active", "Closed", "Defaulted"],
                        index=["Active","Closed","Defaulted"].index(loan_status))
                if st.button("Update Loan"):
                    cursor.execute("""UPDATE loans SET Account_ID=%s,Branch=%s,Loan_Type=%s,Loan_Amount=%s,Interest_Rate=%s,
                                    Loan_Term_Months=%s,Start_Date=%s,End_Date=%s,Loan_Status=%s WHERE Loan_ID=%s """,
                                    (new_account,new_branch,new_loan_type,new_amount,new_interest,
                                     new_term,new_start_date,new_end_date,new_status,lid))   
                    conn.commit()
                    st.success("✅ Loan updated successfully!")
        elif table == "transactions":
            st.subheader("✏️ Update Transaction")
            cursor.execute("SELECT customer_id FROM customers")
            cids = [i[0] for i in cursor.fetchall()]
            cid = st.selectbox("Customer ID", cids)
            cursor.execute("SELECT txn_id FROM transactions WHERE customer_id=%s", (cid,))
            txn_ids = [i[0] for i in cursor.fetchall()]
            tid = st.selectbox("Transaction ID", txn_ids)

            cursor.execute("""SELECT txn_type, amount, txn_time, status FROM transactions 
                        WHERE txn_id=%s""", (tid,))
            data = cursor.fetchone()

            if data:
                txn_type, amount, txn_time, status = data
                types = ["Deposit", "Withdrawal", "Transfer"]
                new_type = st.selectbox("Transaction Type",types,
                index=types.index(txn_type) if txn_type in types else 0)
                new_amount = st.number_input("Amount", value=float(amount))
                new_date = st.date_input("Transaction Date", value=txn_time)
                status_list = ["Success", "Failed", "Pending"]
                new_status = st.selectbox("Status",status_list,
                index=status_list.index(status) if status in status_list else 0)

                if st.button("Update Transaction"):
                    cursor.execute("""UPDATE transactions 
                                SET txn_type=%s, amount=%s, txn_time=%s, status=%s
                                WHERE txn_id=%s""", (new_type, new_amount, new_date, new_status, tid))

                    conn.commit()
                    st.success("✅ Transaction updated successfully!")
        
        elif table == "branches":
            st.subheader("✏️ Update branch details")
            cursor.execute("SELECT Branch_ID FROM branches")
            branch_ids = [i[0] for i in cursor.fetchall()]
            bid = st.selectbox("Select Branch ID", branch_ids)
            cursor.execute("""
                SELECT Branch_Name, City, Manager_Name, Total_Employees,
                Branch_Revenue, Opening_Date, Performance_Rating FROM branches WHERE Branch_ID=%s""", (bid,))
            data = cursor.fetchone()
            if data:
                name, city, manager, employees, revenue, opening_date, rating = data
                new_name = st.text_input("Branch Name", value=name)
                new_city = st.text_input("City", value=city)
                new_manager = st.text_input("Manager Name", value=manager)
                new_employees = st.number_input("Total Employees", value=int(employees), min_value=0)
                new_revenue = st.number_input("Branch Revenue", value=float(revenue), min_value=0.0)
                new_opening = st.date_input("Opening Date", value=opening_date)
                new_rating = st.selectbox("Performance Rating",[1,2,3,4,5] )
                
                if st.button("Update Branch"):
                    cursor.execute("""UPDATE branches SET Branch_Name=%s,City=%s,Manager_Name=%s,Total_Employees=%s,
                    Branch_Revenue=%s,Opening_Date=%s,Performance_Rating=%s WHERE Branch_ID=%s """, 
                    (new_name, new_city, new_manager,new_employees, new_revenue,new_opening, new_rating, bid))
                    
                    conn.commit()
                    st.success("✅ Branch details updated successfully!")

        elif table == "support_tickets":
            st.subheader("✏️ Update Support Ticket")
            cursor.execute("SELECT DISTINCT Customer_ID FROM support_tickets")
            customer_ids = [i[0] for i in cursor.fetchall()]
            cid = st.selectbox("Select Customer ID", customer_ids)
            cursor.execute("SELECT Ticket_ID FROM support_tickets WHERE Customer_ID=%s",(cid,))
            ticket_ids = [i[0] for i in cursor.fetchall()]
            tid = st.selectbox("Select Ticket ID", ticket_ids)
            cursor.execute("""SELECT Account_ID, Loan_ID, Branch_Name, Issue_Category, Description,
                    Date_Opened, Date_Closed, Priority, Status, Resolution_Remarks,
                    Support_Agent, Channel, Customer_Rating FROM support_tickets WHERE Ticket_ID=%s """,(tid,))
            def get_values(col):
                    cursor.execute(f"SELECT DISTINCT {col} FROM support_tickets")
                    data = [row[0] for row in cursor.fetchall()]
                    return data if data else ["General"]
            
            data = cursor.fetchone()

            if data:
                acc_id, loan_id, branch, issue, desc, open_date, close_date, priority, status, remarks, agent, channel, rating = data
                new_acc = st.text_input("Account ID", value=acc_id)
                new_loan = st.text_input("Loan ID", value=loan_id)
                new_branch = st.selectbox("Branch_Name", get_values("Branch_Name"))
                new_issue = st.selectbox("Issue_Category", get_values("Issue_Category"))
                new_desc = st.selectbox("Description", get_values("Description"))
                new_open = st.date_input("Date Opened", value=open_date)
                new_close = st.date_input("Date Closed", value=close_date)
                new_priority = st.selectbox("Priority", ["Low","Medium","High"])
                new_status = st.selectbox("Status", ["Open","In Progress","Resolved","Closed"])
                new_remarks = st.selectbox("Resolution_Remarks",get_values("Resolution_Remarks"))
                new_agent = st.text_input("Support Agent", value=agent)
                new_channel = st.selectbox("Channel", ["Email","Phone","Chat","Branch Visit"])
                new_rating = st.selectbox("Customer Rating", [1,2,3,4,5])

                if st.button("Update Ticket"):
                    cursor.execute("""UPDATE support_tickets SET Account_ID=%s,Loan_ID=%s,Branch_Name=%s,Issue_Category=%s,
                            Description=%s,Date_Opened=%s,Date_Closed=%s,Priority=%s,Status=%s,Resolution_Remarks=%s,
                            Support_Agent=%s,Channel=%s,Customer_Rating=%s WHERE Ticket_ID=%s """,
                            (new_acc,new_loan,new_branch,new_issue,new_desc,new_open,new_close,new_priority,new_status,new_remarks,new_agent,new_channel,new_rating,tid))

                    conn.commit()
                    st.success("✅ Support ticket updated successfully!")
        
        elif table == "credit_cards":
            st.subheader("✏️ Update Credit Card Details")

            cursor.execute("SELECT Card_ID FROM credit_cards")
            card_ids = [row[0] for row in cursor.fetchall()]
            card_id = st.selectbox("Select Credit Card ID", card_ids)

            cursor.execute("""SELECT Account_ID, Customer_ID, Branch, Card_Number, Card_Type, 
                      Card_Network, Credit_Limit, Current_Balance, Issued_Date, Expiry_Date, Status
                      FROM credit_cards WHERE Card_ID=%s""", (card_id,))
            data = cursor.fetchone()

            if data:
                account_id, customer_id, branch, card_number, card_type, card_network, credit_limit, current_balance, issued_date, expiry_date, status = data

                new_account_id = st.text_input("Account ID", value=account_id)
                new_customer_id = st.text_input("Customer ID", value=customer_id)
                new_branch = st.text_input("Branch", value=branch)
                new_card_number = st.text_input("Card Number", value=card_number)
                new_card_type = st.selectbox("Card Type", ["Business", "Gold", "Platinum", "Silver"],
                                     index=["Business","Gold","Platinum","Silver"].index(card_type))
                new_card_network = st.selectbox("Card Network", ["Visa", "MasterCard", "RuPay", "Amex"],
                                        index=["Visa","MasterCard","RuPay","Amex"].index(card_network))
                new_credit_limit = st.number_input("Credit Limit", value=float(credit_limit), min_value=0.0)
                new_current_balance = st.number_input("Current Balance", value=float(current_balance), min_value=0.0)
                new_issued_date = st.date_input("Issued Date", value=issued_date)
                new_expiry_date = st.date_input("Expiry Date", value=expiry_date)
                new_status = st.selectbox("Status", ["Active", "Blocked", "Expired"],
                                  index=["Active","Blocked","Expired"].index(status))

                if st.button("Update Credit Card"):
                    cursor.execute("""UPDATE credit_cards SET 
                              Account_ID=%s, Customer_ID=%s, Branch=%s, Card_Number=%s, 
                              Card_Type=%s, Card_Network=%s, Credit_Limit=%s, Current_Balance=%s,
                              Issued_Date=%s, Expiry_Date=%s, Status=%s
                              WHERE Card_ID=%s""",
                           (new_account_id, new_customer_id, new_branch, new_card_number,
                            new_card_type, new_card_network, new_credit_limit, new_current_balance,
                            new_issued_date, new_expiry_date, new_status, card_id))
                    conn.commit()
                    st.success("✅ Credit Card updated successfully!")
             

    # ---------------- DELETE ----------------
    elif operation == "Delete":
        if table == "customers":
            st.subheader("🗑️ Delete Customer")
            cursor.execute("SELECT customer_id FROM customers")
            customer_ids = [i[0] for i in cursor.fetchall()]
            cid = st.selectbox("Select Customer ID to Delete", customer_ids)
            
            if st.button("Delete Customer"):
                cursor.execute("DELETE FROM transactions WHERE customer_id=%s", (cid,))
                cursor.execute("DELETE FROM accounts WHERE customer_id=%s", (cid,))
                cursor.execute("DELETE FROM loans WHERE customer_id=%s", (cid,))
                cursor.execute("DELETE FROM support_tickets WHERE Customer_ID=%s", (cid,))

        # Now delete the customer
                cursor.execute("DELETE FROM customers WHERE customer_id=%s", (cid,))

                conn.commit()
                st.success(f"✅ Customer {cid} deleted successfully!")

        if table == "accounts":
            st.subheader("🗑️Delete Account details")
            cursor.execute("SELECT customer_id FROM accounts")
            customer_ids = [i[0] for i in cursor.fetchall()]
            cid = st.selectbox("Select Customer ID to Delete", customer_ids)
            if st.button("Delete Account details"):
                cursor.execute("DELETE FROM accounts WHERE customer_id=%s", (cid,))
                conn.commit()
                st.success(f"✅ Customer {cid} deleted successfully!")

        if table=="loans":
             st.subheader("🗑️ Delete Loan details")
             cursor.execute("SELECT Loan_ID FROM Loans")
             loan_ids = [i[0] for i in cursor.fetchall()]
             lid = st.selectbox("Select Loan ID to Delete", loan_ids)
             if st.button("Delete Loan details"):
                cursor.execute("DELETE FROM loans WHERE Loan_ID=%s", (lid,))
                conn.commit()
                st.success(f"✅ Loan ID {lid} deleted successfully!")

        if table == "transactions":
             st.subheader("🗑️ Delete transaction details")
             cursor.execute("SELECT txn_id FROM transactions")
             txn_ids = [i[0] for i in cursor.fetchall()]
             tid = st.selectbox("Select transaction id to Delete",txn_ids)
             if st.button("Delete transaction details"):
                cursor.execute("DELETE FROM transactions WHERE txn_id =%s", (tid,))
                conn.commit()
                st.success(f"✅ Transaction id {tid} deleted successfully!")

        if table == "branches":
             st.subheader("🗑️ Delete Branch details")
             cursor.execute("SELECT Branch_ID FROM branches")
             branch_ids = [i[0] for i in cursor.fetchall()]
             bid = st.selectbox("Select Branch Id to Delete",branch_ids)
             if st.button("Delete Branch details"):
                cursor.execute("DELETE FROM branches WHERE Branch_ID =%s", (bid))
                conn.commit()
                st.success(f"✅ Branch details deleted successfully from branch id {bid}")

        if table == "support_tickets":
             st.subheader("🗑️ Delete Ticket details")
             cursor.execute("SELECT Ticket_ID FROM support_tickets")
             ticket_ids = [i[0] for i in cursor.fetchall()]
             tid = st.selectbox("Select Ticket Id to Delete",ticket_ids)
             if st.button("Delete Ticket details"):
                cursor.execute("DELETE FROM support_tickets WHERE Ticket_ID =%s", (tid))
                conn.commit()
                st.success(f"✅ Ticket details deleted successfully from ticket id {tid}")
        
        if table == "credit_cards":
             st.subheader("🗑️ Delete Credit Card details")
             cursor.execute("SELECT Card_ID FROM credit_cards")
             card_ids = [i[0] for i in cursor.fetchall()]
             cid = st.selectbox("Select Card ID to Delete",card_ids)
             if st.button("Delete Card details"):
                cursor.execute("DELETE FROM credit_cards WHERE Card_ID =%s", (cid))
                conn.commit()
                st.success(f"✅ Credit Card details deleted successfully!")


# ---------------- SIMULATION ----------------
elif "Credit / Debit" in menu:

    st.header("💳 Credit / Debit Simulation")

    df = pd.read_csv("credit_cards.csv") 
    filtered_df = df.copy()

    acc_id = st.multiselect("Enter Account ID",
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
        if acc_id[0] not in df["Account_ID"].astype(str).values:
            st.error("Account not found")
        else:
            account = acc_id[0]  
            cursor.execute("SELECT Current_Balance FROM credit_cards WHERE Account_ID=%s", (account,))
            result = cursor.fetchone()
            if result:
                bal = float(result[0])
            else:
                st.error("Account not found in DB")
                bal = None

            if bal is not None:
                if action == "Check Balance":
                    st.info(f"💰 Current Balance: ₹{bal:.2f}")

                elif action == "Deposit":
                    new_balance = bal + amt
                    cursor.execute(
                        "UPDATE credit_cards SET Current_Balance=%s WHERE Account_ID=%s",
                        (new_balance, account)
                    )
                    conn.commit()
                    st.success(f"✅ Amount Deposited: ₹{amt:,.2f}. New Balance: ₹{new_balance:,.2f}")

                elif action == "Withdraw":
                    if amt > bal:
                        st.error("❌ Insufficient Balance")
                    else:
                        new_balance = bal - amt
                        cursor.execute(
                            "UPDATE credit_cards SET Current_Balance=%s WHERE Account_ID=%s",
                            (new_balance, account)
                        )
                        conn.commit()
                        st.success(f"✅ Amount Withdrawn: ₹{amt:,.2f}. New Balance: ₹{new_balance:,.2f}")


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
