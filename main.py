# Get the metadata
from ClimateAnalytics import NGFSClimateImpact

download = False

CI = NGFSClimateImpact(download)
"""
for varn in ["ec1","ec2", "ec3", "ec4"]:
    print(varn)
    d_out = CI.download_variables(varn)
    d_out.to_excel(f"download/{varn}.xlsx", index = False)

for varn in ["yield_maize_co2","yield_rice_co2","yield_soy_co2","yield_wheat_co2"]:
    print(varn)
    d_out = CI.download_variables(varn)
    d_out.to_excel(f"download/{varn}.xlsx", index = False)

for varn in ["lec","pec","lew","pew"]:
    print(varn)
    d_out = CI.download_variables(varn)
    d_out.to_excel(f"download/{varn}.xlsx", index = False)
"""

for varn in ["leh","peh"]:
    print(varn)
    d_out = CI.download_variables(varn)
    d_out.to_excel(f"download/{varn}.xlsx", index = False)