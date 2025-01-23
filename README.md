# **Automation of Currency Data Processing**

## **Setup**

This project runs on **Python 3.12** and requires the following additional packages:  
- `sqlite3`  
- `requests`  

### **How to Run the Application**
To start the application, navigate to the project directory `Automation_of_Currency_Data_Processing` and run the following command:

`python -m Currency_app.App`

Once the application is launched, the **Currency App Menu** will appear in the terminal.

---

## **Main Features**

The application provides four main actions:

### **1. Fetch Exchange Rates**  
This feature downloads currency exchange data from the **NBP API** and stores it in the database.  

#### Steps:  
1. After selecting action **1**, you will need to specify a **time range** by providing the start and end dates in the format `YYYY-MM-DD`.  
2. Upon successful data retrieval and storage, the application will display the message:  

   ```  
   Data fetched and saved to the database.
   ```  

---

### **2. Analyze Exchange Rates**  
This function identifies the currencies with the **highest increase** and **largest decrease** in exchange rates within a specified time period.  

#### Steps:  
1. After selecting action **2**, you will need to provide the **start and end dates** in the format `YYYY-MM-DD`.  
2. The application will analyze the data and display information about the currencies with the highest fluctuations directly in the terminal.

---

### **3. Export Report**  
This feature allows you to generate reports based on the data stored in the database.

#### Steps:  
1. After selecting action **3**, specify a **currency code** to filter by, or leave it empty to generate a report for all currencies.  
2. Next, choose the desired report format by entering either **"csv"** or **"json"**.  
3. Once the report is generated successfully, it will be saved in the **"reports"** directory with the filename:  

   ```
   currency_report_CURRENT_DATE_TIME.csv/json
   ```

---

### **4. Exit**  
This option terminates the application, closes the menu, and ends the process.


## **Usage example**

### Scenario 1:
1. Fetch exchange rates commands: `1`, `2025-01-01`, `2025-01-10`
2. Analyze exchange rates commands: `2`, `2025-01-01`, `2025-01-10`
3. Exit command: `4`

### Scenario 2:
1. Fetch exchange rates commands: `1`, `2025-01-08`, `2025-01-18`
2. Export report for all currencies in csv commands: `3`, `[empty]`, `csv`
3. Export report for USD currency in json commands: `3`, `USD`, `json`
4. Exit command: `4`

### Scanario 3:
(It assumes that the data has already been fetched from the NBP API during a previous interaction with the app.)
1. Export report for EUR currency in json commands: `3`, `EUR`, `json`
2. Exit command: `4`
