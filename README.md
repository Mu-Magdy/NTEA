# NoN-Technical Employees Assistant (NTEA)

## Project Overview
This project involves developing a chatbot designed to assist non-technical employees in accessing personal information such as their bonuses, leave balances, salary details, and performance ratings. The chatbot requires the employee to authenticate, after which it retrieves the necessary information from the company's employee database. The data, along with the employee's query, is processed by a large language model (LLM) like GPT or Gemini, which provides accurate responses to the employee's queries.

## Importance of the Project
The chatbot simplifies how employees interact with their personal data, removing the need for direct HR interaction. This leads to:
- Faster response times (eliminating waiting for HR to respond)
- Enhanced efficiency and self-service capabilities
- Reduced HR workload, allowing HR to focus on more critical tasks

## Features
- **Password Hashing:** Provides security for user authentication.
- **Data Privacy:** Ensures only authenticated employees can access their personal data.
- **Real-time Responses:** Employees receive answers immediately after querying.
- **Multilingual Support:** The chatbot supports both Arabic and English.
- **Objective-Focused Interaction:** Employees can only query personal information, reducing misuse of the chatbot.

## Setup Instructions
### Prerequisites
1. **Python 3.x:** Ensure you have Python 3 installed on your machine.
2. **OpenAI API:** You'll need access to OpenAI's API.

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/EsmailEssam/NoN-Technical-Employees-Assistant-NTEA-.git
   cd NoN-Technical-Employees-Assistant-NTEA-
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create the SQLite Database:
   ```
   python database/setup_database.py
   ```
4. Insert fake data to Database:
   ```
   python database/insert_data.py
   ```
5. Run the Streamlit Application:
   ```
   streamlit run app.py
   ```
   This will launch the chatbot in your web browser.

## How It Works
1. Employees authenticate using a password hashed for security.
2. Once authenticated, the chatbot retrieves the employee's data from the database.
3. The employee can ask queries about their personal information (such as bonuses, leaves, and salary), and the chatbot (powered by GPT) provides relevant responses.
4. The interaction is limited to work-related queries, ensuring that ChatGPT stays focused on the employee's needs.

## Future Scope
- Integrating a **RAG system** for policy queries.
- Adding **role-based access** to control employee data access based on position.

## Contact
If you have any questions or feedback, feel free to reach out to the team:
[Esmail Essam](https://www.linkedin.com/in/esmail-essam/)
[Muhammed Magdy](https://www.linkedin.com/in/mu-magdy/)
[Mohammad Nomer](https://www.linkedin.com/in/mohammad-nomer/)
[Ziad Mohy](https://www.linkedin.com/in/ziad-mohy-74079b323/)
