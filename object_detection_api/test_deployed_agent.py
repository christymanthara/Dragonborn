from google.cloud import resourcemanager_v3
from google.iam.v1 import iam_policy_pb2

project_id = "clever-axe-456700-a1"
principal = "PRINCIPAL"

crm_service = resourcemanager_v3.ProjectsClient()
policy = crm_service.get_iam_policy(iam_policy_pb2.GetIamPolicyRequest(
    resource=f"projects/{project_id}"
))
for binding in policy.bindings:
    for member in binding.members:
        if principal in member:
            print(binding.role)