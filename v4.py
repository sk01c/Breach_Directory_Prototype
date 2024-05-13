import pandas as pd
import streamlit as st

def collect_breach_data():
    """Collect breach data from the user."""
    data = {
        'Names': [],
        'Self Declared': [],
        'Nature of Discovery': [],
        'Dates': [],
        'Entities': [],
        'Department': [],
        'Breach Category': [],
        'MNPI': [],
        'Root Cause Analysis': [],
        'Data/Financial Loss': [],
        'Internal Conflict': [],
        'Intentional Misuse of Confidential Data': [],
        'Customer Detriment': [],
        'Market Impact': [],
        'Reputational Impact': [],
        'Risk Score': [],
        'Risk Rating': []
    }

    while True:
        self_declared = st.radio("Was this incident self-declared?", ("Yes", "No"))
        data['Self Declared'].append(self_declared)

        if self_declared == "No":
            nature_of_discovery = st.selectbox("Nature of Discovery:", ["Data from HR", "Data from internal audit",
                                                                      "Data from external audit", "Other"])
            data['Nature of Discovery'].append(nature_of_discovery)
        else:
            data['Nature of Discovery'].append("")

        names = st.text_input("Name of the person under investigation:")
        dates = st.text_input("Date of the incident (dd/mm/yyyy):")
        entities = st.text_input("Entity where the incident took place:")
        department = st.text_input("Department in which the incident occurred:")
        breach_category = st.text_input("Breach Category:")
        data['Names'].append(names)
        data['Dates'].append(dates)
        data['Entities'].append(entities)
        data['Department'].append(department)
        data['Breach Category'].append(breach_category)

        if st.radio("Did this breach result in data loss?", ("Yes", "No")) == "Yes":
            st.info("Contact ITSD to ensure the issue is resolved.")

        data['MNPI'].append(st.radio("Was MNPI involved?", ("Yes", "No")))

        root_cause = st.selectbox("Root Cause Analysis:", ["Human Error", "Negligence", "Intentional", "Process Error", "Other"])
        data['Root Cause Analysis'].append(root_cause)

        criteria = ['Data/Financial Loss', 'Internal Conflict', 'Intentional Misuse of Confidential Data',
                    'Customer Detriment', 'Market Impact', 'Reputational Impact']
        weights = {'Data/Financial Loss': 7, 'Internal Conflict': 3, 'Intentional Misuse of Confidential Data': 8,
                   'Customer Detriment': 8, 'Market Impact': 8, 'Reputational Impact': 5}
        severity_ratings = {crit: st.slider(f"Severity of '{crit}' (0-10):", 0, 10, 5) for crit in criteria}
        for crit, severity in severity_ratings.items():
            data[crit].append(severity)

        if st.radio("Continue entering data?", ("Yes", "No")) != 'Yes':
            break

    max_length = max(len(values) for values in data.values())
    for key, values in data.items():
        while len(values) < max_length:
            data[key].append("")

    total_risk_score = [sum(data[crit][i] * weights[crit] for crit in criteria if isinstance(data[crit][i], int)) for i in range(len(data['Names']))]
    risk_ratings = ["High" if score > 80 else "Medium" if score > 40 else "Low" for score in total_risk_score]

    data['Risk Score'] = total_risk_score
    data['Risk Rating'] = risk_ratings

    df = pd.DataFrame(data)
    st.write(df)


def main():
    """Main function to run the application."""
    st.title("Breach Directory")

    collect_breach_data()


if __name__ == "__main__":
    main()
