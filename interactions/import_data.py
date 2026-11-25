import csv
from pathlib import Path
from interactions.models import DrugInteraction

csv_folder = Path("interaction_csv/interaction_csv")

for csv_file in csv_folder.glob("*.csv"):
    with open(csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        interactions = []

        for row in reader:
            interactions.append(
                DrugInteraction(ddinter_id_a=row["DDInterID_A"], drug_a=row["Drug_A"], ddinter_id_b=row["DDInterID_B"], drug_b=row["Drug_B"], level=row["Level"])
            )

        DrugInteraction.objects.bulk_create(interactions)
print("DDInter data has been imported")