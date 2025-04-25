import pandas as pd
from pathlib import Path

# Config
RAW_DATA = Path("../data/raw-synthea-data")
SUMMARIES_DIR = Path("../data/patient_summaries")
SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

# Load all full dataframes
patients = pd.read_csv(RAW_DATA / "patients.csv")
conditions = pd.read_csv(RAW_DATA / "conditions.csv")
observations = pd.read_csv(RAW_DATA / "observations.csv")
medications = pd.read_csv(RAW_DATA / "medications.csv")
encounters = pd.read_csv(RAW_DATA / "encounters.csv")

# Generate summaries
summaries = []

for _, patient in patients.iterrows():
    patient_id = patient["Id"]
    birthdate = patient["BIRTHDATE"]
    age = 2025 - int(patient["BIRTHDATE"][:4])

    # Demographics
    summary = []
    summary.append(f"Age: {age} years")
    summary.append(f"Birthdate: {birthdate[:10]}")

    # Conditions
    conds = conditions[conditions["PATIENT"] == patient_id]
    if not conds.empty:
        summary.append("\nConditions:")
        for _, row in conds.iterrows():
            summary.append(
                f"- {row['DESCRIPTION']} (Diagnosed: {row['START'][:10]})")

    # Observations (latest 3)
    obs = observations[observations["PATIENT"] == patient_id]
    recent_obs = obs.sort_values(by="DATE", ascending=False).head(3)
    if not recent_obs.empty:
        summary.append("\nRecent Observations:")
        for _, row in recent_obs.iterrows():
            val = f"{row['VALUE']} {row['UNITS']}" if pd.notnull(
                row['UNITS']) else row['VALUE']
            summary.append(
                f"- {row['DESCRIPTION']}: {val} ({row['DATE'][:10]})")

    # Medications
    meds = medications[medications["PATIENT"] == patient_id]
    if not meds.empty:
        summary.append("\nMedications:")
        for _, row in meds.iterrows():
            summary.append(
                f"- {row['DESCRIPTION']} (Started: {row['START'][:10]})")

    # Last Encounter
    enc = encounters[encounters["PATIENT"] == patient_id]
    if not enc.empty:
        last = enc.sort_values(by="START", ascending=False).iloc[0]
        reason = last['REASONDESCRIPTION'] if 'REASONDESCRIPTION' in last and pd.notnull(
            last['REASONDESCRIPTION']) else "Unknown"
        summary.append(
            f"\nLast Encounter:\n- {last['START'][:10]} | Reason: {reason}")

        summaries.append("\n".join(summary))


# Save each summary to a file
for i, summary in enumerate(summaries, start=1):
    filename = Path("data/patient_summaries") / f"patient_{i}.txt"
    with open(filename, "w") as f:
        f.write(summary)
        print(f"Summary for Patient {i}/{len(summaries)} saved to {filename}")
