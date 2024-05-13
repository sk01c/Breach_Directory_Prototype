import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog


def get_input(prompt):
    """Prompt user for input."""
    return simpledialog.askstring("Input", prompt)


def get_yes_no(prompt):
    """Prompt user for yes/no input."""
    return "yes" if messagebox.askyesno("Input", prompt) else "no"


def get_option(prompt, options):
    """Prompt user for input with predefined options."""
    return simpledialog.askstring("Input", f"{prompt}\nOptions: {', '.join(options)}") if options else None


def get_numeric_input(prompt):
    """Prompt user for numeric input."""
    return simpledialog.askinteger("Input", prompt)


def append_data(data, keys, values):
    """Append data to the data dictionary."""
    for key, value in zip(keys, values):
        data[key].append(value)


def update_breach_log_display(df, text_widget):
    """Update the breach log display."""
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)

    headers = list(df.columns)

    formatted_data = []
    for index, row in df.iterrows():
        formatted_row = "\n".join([f"{header}: {row[header]}" for header in headers])
        formatted_data.append(formatted_row)

    formatted_text = "\n\n".join(formatted_data)

    text_widget.insert(tk.END, formatted_text)

    text_widget.config(state=tk.DISABLED)


def collect_breach_data(root, text_widget):
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
        self_declared = get_yes_no("Was this incident self-declared?")
        append_data(data, ['Self Declared'], [self_declared])

        if self_declared == "no":
            nature_of_discovery = get_option("Nature of Discovery:", ["Data from HR", "Data from internal audit",
                                                                      "Data from external audit", "Other"])
            append_data(data, ['Nature of Discovery'], [nature_of_discovery])
        else:
            append_data(data, ['Nature of Discovery'], [""])

        names = get_input("Name of the person under investigation:")
        dates = get_input("Date of the incident (dd/mm/yyyy):")
        entities = get_input("Entity where the incident took place:")
        department = get_input("Department in which the incident occurred:")
        breach_category = get_input("Breach Category:")
        append_data(data, ['Names', 'Dates', 'Entities', 'Department', 'Breach Category'],
                    [names, dates, entities, department, breach_category])

        if get_yes_no("Did this breach result in data loss?") == "yes":
            messagebox.showinfo("Information", "Contact ITSD to ensure the issue is resolved.")

        append_data(data, ['MNPI'], [get_yes_no("Was MNPI involved?")])

        root_cause = get_option("Root Cause Analysis:", ["Human Error", "Negligence", "Intentional", "Process Error", "Other"])
        append_data(data, ['Root Cause Analysis'], [root_cause])

        criteria = ['Data/Financial Loss', 'Internal Conflict', 'Intentional Misuse of Confidential Data',
                    'Customer Detriment', 'Market Impact', 'Reputational Impact']
        weights = {'Data/Financial Loss': 7, 'Internal Conflict': 3, 'Intentional Misuse of Confidential Data': 8,
                   'Customer Detriment': 8, 'Market Impact': 8, 'Reputational Impact': 5}
        severity_ratings = {crit: get_numeric_input(f"Severity of '{crit}' (0-10):") for crit in criteria}
        for crit, severity in severity_ratings.items():
            data[crit].append(severity)

        if get_yes_no("Continue entering data?") != 'yes':
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

    update_breach_log_display(df, text_widget)

    with open('breach_log.csv', 'a') as f:
        df.to_csv(f, index=False, header=f.tell() == 0)

    messagebox.showinfo("Information", "Breach log updated.")


def main():
    """Main function to run the application."""
    root = tk.Tk()
    root.title("Breach Directory")

    title_label = tk.Label(root, text="Breach Directory", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    text_widget = tk.Text(root, height=20, width=150)
    text_widget.pack(padx=10, pady=10)

    collect_breach_data(root, text_widget)

    root.mainloop()


if __name__ == "__main__":
    main()
