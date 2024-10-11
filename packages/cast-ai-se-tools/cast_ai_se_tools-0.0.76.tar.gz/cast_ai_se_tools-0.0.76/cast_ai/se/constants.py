API_SERVER = "https://api.cast.ai"
EXTERNAL_CLUSTER_PREFIX = "/v1/kubernetes/external-clusters/"
AUDIT_PREFIX = "/v1/audit"
CLUSTER_Q = "?clusterId="
CLUSTERS_PREFIX = "/v1/kubernetes/clusters/"
POLICIES_POSTFIX = "/policies"
NODES_POSTFIX = "/nodes"
RECONCILE_POSTFIX = "/reconcile"

CAST_NS = "castai-agent"

DEMO_ON_CRONJOB = "hibernate-resume"
DEMO_OFF_CRONJOB = "hibernate-pause"

LOG_DIR = "logs"

REQUIRED_TOOLS = ["kubectl", "jq"]

WIN_GET_DEPLOYMENTS_CMD = ('get deployments -n default'
                           ' --output=jsonpath="{range .items[*]} {.metadata.name} {end}"')

LINUX_GET_DEPLOYMENTS_CMD = 'get deployments -n default --output=jsonpath="{.items[*].metadata.name}"'


LINUX_GET_NONZERO_DEPLOYMENTS_CMD = ('get deployments -n default -o json | jq -r ".items[] | '
                                     'select(.spec.replicas!=0) | .metadata.name"')

WIN_GET_NONZERO_DEPLOYMENTS_CMD = ('get deployments -n default'
                                   ' -o json | jq -r ".items[] | select(.spec.replicas!=0) | .metadata.name"')

GCP_AUTH_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
GCP_AUTH_CMD = "gcloud auth application-default login"
PROD_BUCKET = "prod-master-console-cluster-snapshots-snapshotstore"
PROD_PROJECT = "prod-master-scl0"

POD_SPEC_KEYWORDS = ["nodeSelector",
                     "topologySpreadConstraints",
                     "affinity",
                     "runtimeClassName",
                     "tolerations"]

CSV_REPORT_HEADERS = ["Type",
                      "Name",
                      "Namespace",
                      "nodeSelector",
                      "topologySpreadConstraints",
                      "affinity",
                      "runtimeClassName",
                      "tolerations",
                      "No Requests"]

CSV_REPORT_HEADERS_PDB = ["Name",
                          "Namespace",
                          "Disruptions Allowed",
                          "Current Healthy"]


K8S_WORKLOAD_TYPES = ["deploymentList",
                      "replicaSetList",
                      "daemonSetList",
                      "statefulSetList",
                      "jobList"]

WORKLOAD_MAP = {'deploymentList': 'deployments',
                'replicaSetList': 'replica_sets',
                'daemonSetList': 'daemon_sets',
                'statefulSetList': 'stateful_sets',
                'jobList': 'jobs'}

WORKLOAD_TYPES = ['deployments', 'replica_sets', 'daemon_sets', 'stateful_sets', 'jobs']

NON_RELEVANT_NAMESPACES = ["castai-agent"]

CLOUD_TAINTS = ["node.kubernetes.io/unreachable",
                "node.kubernetes.io/not-ready",
                "node.kubernetes.io/unschedulable",
                "node.kubernetes.io/disk-pressure",
                "node.kubernetes.io/memory-pressure",
                "node.kubernetes.io/pid-pressure",
                "node.kubernetes.io/network-unavailable"]
