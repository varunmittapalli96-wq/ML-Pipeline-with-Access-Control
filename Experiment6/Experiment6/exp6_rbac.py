# ============================================================
# EXPERIMENT 6
# ML PIPELINE WITH ACCESS CONTROL
# ============================================================
#
# Objective:
# Implement Role-Based Access Control (RBAC) for an ML pipeline.
#
# The system:
# 1. Defines different user roles.
# 3. Uses a decorator to protect ML pipeline stages.
# 4. Allows authorized users to execute operations.
# 5. Denies unauthorized users.
# 6. Records every access attempt in an audit log.
# 7. Generates an audit report.
#
# ============================================================

from functools import wraps
from datetime import datetime


# ============================================================
# SECTION 1: ROLE AND PERMISSION CONFIGURATION
# ============================================================

ROLES = {

    # Data Engineer can work with data.
    "data_engineer": {
        "extract",
        "transform"
    },

    # Data Scientist can transform, train and evaluate models.
    "data_scientist": {
        "transform",
        "train",
        "evaluate"
    },

    # ML Engineer can train, evaluate and deploy models.
    "ml_engineer": {
        "train",
        "evaluate",
        "deploy"
    },

    # Administrator has complete access.
    "admin": {
        "extract",
        "transform",
        "train",
        "evaluate",
        "deploy"
    },

    # Viewer has only viewing permission.
    "viewer": {
        "view"
    }
}


# ============================================================
# SECTION 2: AUDIT LOG
# ============================================================

AUDIT_LOG = []


# ============================================================
# SECTION 3: CUSTOM ACCESS DENIED EXCEPTION
# ============================================================

class AccessDenied(Exception):
    """
    Exception raised when a user tries to perform
    an operation that is not permitted for their role.
    """
    pass


# ============================================================
# SECTION 4: AUDIT LOG FUNCTION
# ============================================================

def audit(role, permission, allowed):
    """
    Records every access attempt.

    Parameters:
        role       : User role
        permission : Requested operation
        allowed    : True if access is allowed,
                     False otherwise
    """

    entry = {

        "time": datetime.now().strftime("%H:%M:%S"),

        "role": role,

        "action": permission,

        "result": "ALLOW" if allowed else "DENY"
    }

    AUDIT_LOG.append(entry)


# ============================================================
# SECTION 5: RBAC PERMISSION DECORATOR
# ============================================================

def require(permission):
    """
    Decorator used to protect ML pipeline operations.

    Before a function is executed, the decorator checks
    whether the user's role has the required permission.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(user_role, *args, **kwargs):

            # Get permissions assigned to the role.
            user_permissions = ROLES.get(user_role, set())

            # Check whether requested permission exists.
            allowed = permission in user_permissions

            # Record access attempt.
            audit(
                user_role,
                permission,
                allowed
            )

            # If permission is not available,
            # reject the request.
            if not allowed:

                raise AccessDenied(
                    f"Role '{user_role}' is NOT authorized "
                    f"for '{permission}'"
                )

            # Access is allowed.
            print(
                f"[AUTH OK ] "
                f"{user_role:15s} -> {permission}"
            )

            # Execute original function.
            return func(
                user_role,
                *args,
                **kwargs
            )

        return wrapper

    return decorator


# ============================================================
# SECTION 6: ML PIPELINE DATA
# ============================================================

RAW_DATA = []

TRANSFORMED_DATA = []

TRAINED_MODEL = None

EVALUATION_RESULT = None

DEPLOYMENT_STATUS = False


# ============================================================
# SECTION 7: DATA EXTRACTION
# ============================================================

@require("extract")
def extract(role):

    """
    Extract raw data for the ML pipeline.
    """

    global RAW_DATA

    print("     Extracting raw data...")

    RAW_DATA = [
        {
            "customer_id": 1,
            "age": 22,
            "usage": 10,
            "churn": 0
        },

        {
            "customer_id": 2,
            "age": 35,
            "usage": 25,
            "churn": 1
        },

        {
            "customer_id": 3,
            "age": 28,
            "usage": 15,
            "churn": 0
        },

        {
            "customer_id": 4,
            "age": 45,
            "usage": 40,
            "churn": 1
        },

        {
            "customer_id": 5,
            "age": 30,
            "usage": 20,
            "churn": 0
        }
    ]

    print(
        f"     Raw records extracted: "
        f"{len(RAW_DATA)}"
    )

    return RAW_DATA


# ============================================================
# SECTION 8: DATA TRANSFORMATION
# ============================================================

@require("transform")
def transform(role):

    """
    Transform raw data into a format suitable
    for machine learning.
    """

    global TRANSFORMED_DATA

    print("     Transforming data...")

    if not RAW_DATA:

        print(
            "     No raw data available."
        )

        return None

    TRANSFORMED_DATA = []

    for row in RAW_DATA:

        transformed_row = {

            "age": row["age"],

            "usage": row["usage"],

            "churn": row["churn"]
        }

        TRANSFORMED_DATA.append(
            transformed_row
        )

    print(
        f"     Records transformed: "
        f"{len(TRANSFORMED_DATA)}"
    )

    return TRANSFORMED_DATA


# ============================================================
# SECTION 9: MODEL TRAINING
# ============================================================

@require("train")
def train(role):

    """
    Train a simple demonstration ML model.

    This experiment focuses on RBAC, so the model is
    represented as a simple dictionary.
    """

    global TRAINED_MODEL

    print("     Training ML model...")

    if not TRANSFORMED_DATA:

        print(
            "     No transformed data available."
        )

        return None

    # Simple demonstration model.
    TRAINED_MODEL = {

        "model_name":
            "CustomerChurnModel",

        "algorithm":
            "Rule-Based Classifier",

        "status":
            "trained",

        "records_used":
            len(TRANSFORMED_DATA)
    }

    print(
        "     Model training completed."
    )

    print(
        f"     Model: "
        f"{TRAINED_MODEL['model_name']}"
    )

    return TRAINED_MODEL


# ============================================================
# SECTION 10: MODEL EVALUATION
# ============================================================

@require("evaluate")
def evaluate(role):

    """
    Evaluate the trained model.
    """

    global EVALUATION_RESULT

    print("     Evaluating ML model...")

    if TRAINED_MODEL is None:

        print(
            "     Model has not been trained."
        )

        return None

    # Demonstration evaluation result.
    EVALUATION_RESULT = {

        "accuracy": 0.92,

        "precision": 0.90,

        "recall": 0.89,

        "status": "passed"
    }

    print(
        f"     Accuracy : "
        f"{EVALUATION_RESULT['accuracy']}"
    )

    print(
        f"     Precision: "
        f"{EVALUATION_RESULT['precision']}"
    )

    print(
        f"     Recall   : "
        f"{EVALUATION_RESULT['recall']}"
    )

    return EVALUATION_RESULT


# ============================================================
# SECTION 11: MODEL DEPLOYMENT
# ============================================================

@require("deploy")
def deploy(role):

    """
    Deploy the trained and evaluated model.
    """

    global DEPLOYMENT_STATUS

    print("     Deploying ML model...")

    if TRAINED_MODEL is None:

        print(
            "     Deployment failed: "
            "model is not trained."
        )

        return False

    if EVALUATION_RESULT is None:

        print(
            "     Deployment failed: "
            "model is not evaluated."
        )

        return False

    if EVALUATION_RESULT["status"] != "passed":

        print(
            "     Deployment failed: "
            "model evaluation did not pass."
        )

        return False

    DEPLOYMENT_STATUS = True

    print(
        "     Model successfully deployed."
    )

    return True


# ============================================================
# SECTION 12: VIEW PIPELINE STATUS
# ============================================================

@require("view")
def view_status(role):

    """
    Display the current ML pipeline status.
    """

    print()
    print("     --------------------------------------")
    print("     ML PIPELINE STATUS")
    print("     --------------------------------------")

    print(
        f"     Raw Data          : "
        f"{'Available' if RAW_DATA else 'Not Available'}"
    )

    print(
        f"     Transformed Data  : "
        f"{'Available' if TRANSFORMED_DATA else 'Not Available'}"
    )

    print(
        f"     Trained Model     : "
        f"{'Available' if TRAINED_MODEL else 'Not Available'}"
    )

    print(
        f"     Evaluation        : "
        f"{'Completed' if EVALUATION_RESULT else 'Not Completed'}"
    )

    print(
        f"     Deployment        : "
        f"{'Deployed' if DEPLOYMENT_STATUS else 'Not Deployed'}"
    )

    print("     --------------------------------------")


# ============================================================
# SECTION 13: SAFE FUNCTION EXECUTION
# ============================================================

def try_action(function, role):

    """
    Execute a protected function safely.

    If the user does not have permission,
    AccessDenied is caught and displayed.
    """

    try:

        return function(role)

    except AccessDenied as error:

        print(
            f"[DENIED ] {error}"
        )

        return None

    except Exception as error:

        print(
            f"[ERROR  ] {error}"
        )

        return None


# ============================================================
# SECTION 14: DISPLAY ROLE PERMISSIONS
# ============================================================

def display_roles():

    """
    Display all roles and their permissions.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "ROLE PERMISSION MATRIX"
    )

    print(
        "============================================================"
    )

    for role, permissions in ROLES.items():

        permission_list = ", ".join(
            sorted(permissions)
        )

        print(
            f"{role:18s} : "
            f"{permission_list}"
        )

    print(
        "============================================================"
    )


# ============================================================
# SECTION 15: DISPLAY AUDIT LOG
# ============================================================

def display_audit_log():

    """
    Display every access decision.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "AUDIT LOG"
    )

    print(
        "============================================================"
    )

    if not AUDIT_LOG:

        print(
            "No access attempts recorded."
        )

        return

    print(
        f"{'TIME':10s} "
        f"{'ROLE':18s} "
        f"{'ACTION':12s} "
        f"{'RESULT':10s}"
    )

    print(
        "-" * 55
    )

    for entry in AUDIT_LOG:

        print(
            f"{entry['time']:10s} "
            f"{entry['role']:18s} "
            f"{entry['action']:12s} "
            f"{entry['result']:10s}"
        )


# ============================================================
# SECTION 16: AUDIT SUMMARY
# ============================================================

def audit_summary():

    """
    Generate a summary of ALLOW and DENY decisions.
    """

    allowed_count = 0

    denied_count = 0

    for entry in AUDIT_LOG:

        if entry["result"] == "ALLOW":

            allowed_count += 1

        else:

            denied_count += 1

    print()
    print(
        "============================================================"
    )

    print(
        "AUDIT SUMMARY"
    )

    print(
        "============================================================"
    )

    print(
        f"Total Access Attempts : "
        f"{len(AUDIT_LOG)}"
    )

    print(
        f"Allowed Requests      : "
        f"{allowed_count}"
    )

    print(
        f"Denied Requests       : "
        f"{denied_count}"
    )

    print(
        "============================================================"
    )


# ============================================================
# SECTION 17: ADMIN WORKFLOW
# ============================================================

def run_admin_workflow():

    """
    Demonstrates a complete authorized workflow
    using the admin role.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "ADMIN WORKFLOW"
    )

    print(
        "============================================================"
    )

    print()
    print("[1] Extract")

    try_action(
        extract,
        "admin"
    )

    print()
    print("[2] Transform")

    try_action(
        transform,
        "admin"
    )

    print()
    print("[3] Train")

    try_action(
        train,
        "admin"
    )

    print()
    print("[4] Evaluate")

    try_action(
        evaluate,
        "admin"
    )

    print()
    print("[5] Deploy")

    try_action(
        deploy,
        "admin"
    )


# ============================================================
# SECTION 18: DATA ENGINEER WORKFLOW
# ============================================================

def run_data_engineer_workflow():

    """
    Demonstrates permissions of a data engineer.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "DATA ENGINEER ACCESS TEST"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "Data Engineer -> Extract"
    )

    try_action(
        extract,
        "data_engineer"
    )

    print()
    print(
        "Data Engineer -> Transform"
    )

    try_action(
        transform,
        "data_engineer"
    )

    print()
    print(
        "Data Engineer -> Train"
    )

    try_action(
        train,
        "data_engineer"
    )

    print()
    print(
        "Data Engineer -> Deploy"
    )

    try_action(
        deploy,
        "data_engineer"
    )


# ============================================================
# SECTION 19: DATA SCIENTIST WORKFLOW
# ============================================================

def run_data_scientist_workflow():

    """
    Demonstrates permissions of a data scientist.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "DATA SCIENTIST ACCESS TEST"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "Data Scientist -> Transform"
    )

    try_action(
        transform,
        "data_scientist"
    )

    print()
    print(
        "Data Scientist -> Train"
    )

    try_action(
        train,
        "data_scientist"
    )

    print()
    print(
        "Data Scientist -> Evaluate"
    )

    try_action(
        evaluate,
        "data_scientist"
    )

    print()
    print(
        "Data Scientist -> Deploy"
    )

    try_action(
        deploy,
        "data_scientist"
    )


# ============================================================
# SECTION 20: ML ENGINEER WORKFLOW
# ============================================================

def run_ml_engineer_workflow():

    """
    Demonstrates permissions of an ML engineer.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "ML ENGINEER ACCESS TEST"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "ML Engineer -> Train"
    )

    try_action(
        train,
        "ml_engineer"
    )

    print()
    print(
        "ML Engineer -> Evaluate"
    )

    try_action(
        evaluate,
        "ml_engineer"
    )

    print()
    print(
        "ML Engineer -> Deploy"
    )

    try_action(
        deploy,
        "ml_engineer"
    )

    print()
    print(
        "ML Engineer -> Extract"
    )

    try_action(
        extract,
        "ml_engineer"
    )


# ============================================================
# SECTION 21: VIEWER ACCESS TEST
# ============================================================

def run_viewer_workflow():

    """
    Demonstrates viewer permissions.

    Viewer should only have the view permission.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "VIEWER ACCESS TEST"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "Viewer -> View"
    )

    try_action(
        view_status,
        "viewer"
    )

    print()
    print(
        "Viewer -> Train"
    )

    try_action(
        train,
        "viewer"
    )

    print()
    print(
        "Viewer -> Deploy"
    )

    try_action(
        deploy,
        "viewer"
    )


# ============================================================
# SECTION 22: UNAUTHORIZED ROLE TEST
# ============================================================

def run_invalid_role_test():

    """
    Test an unknown role.

    An unknown role should not receive any permissions.
    """

    unknown_role = "guest"

    print()
    print(
        "============================================================"
    )

    print(
        "UNKNOWN ROLE ACCESS TEST"
    )

    print(
        "============================================================"
    )

    print()
    print(
        f"Unknown Role -> Extract"
    )

    try_action(
        extract,
        unknown_role
    )

    print()
    print(
        f"Unknown Role -> Train"
    )

    try_action(
        train,
        unknown_role
    )

    print()
    print(
        f"Unknown Role -> Deploy"
    )

    try_action(
        deploy,
        unknown_role
    )


# ============================================================
# SECTION 23: MAIN PROGRAM
# ============================================================

def main():

    """
    Main execution function.
    """

    print()
    print(
        "============================================================"
    )

    print(
        "        EXPERIMENT 6 - ML PIPELINE ACCESS CONTROL"
    )

    print(
        "        ROLE-BASED ACCESS CONTROL (RBAC)"
    )

    print(
        "============================================================"
    )

    print()
    print(
        "This experiment demonstrates:"
    )

    print(
        "1. Role-Based Access Control"
    )

    print(
        "2. Permission checking"
    )

    print(
        "3. Least privilege"
    )

    print(
        "4. Decorator-based authorization"
    )

    print(
        "5. Access denial"
    )

    print(
        "6. Audit logging"
    )


    # --------------------------------------------------------
    # Display role permissions
    # --------------------------------------------------------

    display_roles()


    # --------------------------------------------------------
    # Run complete administrator workflow
    # --------------------------------------------------------

    run_admin_workflow()


    # --------------------------------------------------------
    # Test Data Engineer permissions
    # --------------------------------------------------------

    run_data_engineer_workflow()


    # --------------------------------------------------------
    # Test Data Scientist permissions
    # --------------------------------------------------------

    run_data_scientist_workflow()


    # --------------------------------------------------------
    # Test ML Engineer permissions
    # --------------------------------------------------------

    run_ml_engineer_workflow()


    # --------------------------------------------------------
    # Test Viewer permissions
    # --------------------------------------------------------

    run_viewer_workflow()


    # --------------------------------------------------------
    # Test unknown role
    # --------------------------------------------------------

    run_invalid_role_test()


    # --------------------------------------------------------
    # Display final pipeline status
    # --------------------------------------------------------

    print()
    print(
        "============================================================"
    )

    print(
        "FINAL PIPELINE STATUS"
    )

    print(
        "============================================================"
    )

    # Viewer is authorized to view the status.
    try_action(
        view_status,
        "viewer"
    )


    # --------------------------------------------------------
    # Display audit log
    # --------------------------------------------------------

    display_audit_log()


    # --------------------------------------------------------
    # Display audit summary
    # --------------------------------------------------------

    audit_summary()


    # --------------------------------------------------------
    # Experiment completed
    # --------------------------------------------------------

    print()
    print(
        "============================================================"
    )

    print(
        "EXPERIMENT 6 COMPLETED SUCCESSFULLY"
    )

    print(
        "============================================================"
    )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()