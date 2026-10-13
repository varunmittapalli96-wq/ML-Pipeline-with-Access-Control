from datetime import datetime

# ============================================================
# PHASE 4 — DEPLOY & MONITOR
# ============================================================

deployment_status = False
security_events = []


def log_event(event, status):
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "event": event,
        "status": status
    }

    security_events.append(entry)


def authorize_deployment(role):
    """
    Only ML Engineer and Admin can deploy.
    """

    allowed_roles = {
        "ml_engineer",
        "admin"
    }

    if role in allowed_roles:
        print(f"[DEPLOY AUTHORIZED] {role}")
        log_event(
            f"Deployment authorization by {role}",
            "ALLOW"
        )
        return True

    print(f"[DEPLOY DENIED] {role}")
    log_event(
        f"Unauthorized deployment attempt by {role}",
        "DENY"
    )
    return False


def deploy_model(role):
    """
    Secure model deployment.
    """

    global deployment_status

    print()
    print("------------------------------------------------------------")
    print("SECURE MODEL DEPLOYMENT")
    print("------------------------------------------------------------")

    if not authorize_deployment(role):
        print("Model deployment blocked.")
        return False

    print("Checking model security...")
    print("Checking model evaluation...")
    print("Checking deployment authorization...")

    deployment_status = True

    print("Model deployment successful.")

    log_event(
        "ML model deployed successfully",
        "SUCCESS"
    )

    return True


def monitor_runtime():
    """
    Runtime monitoring of deployed model.
    """

    print()
    print("------------------------------------------------------------")
    print("RUNTIME MONITORING")
    print("------------------------------------------------------------")

    if deployment_status:

        print("Model Status : RUNNING")
        print("Runtime Security : ACTIVE")
        print("Access Monitoring : ACTIVE")
        print("Audit Monitoring : ACTIVE")

        log_event(
            "Runtime monitoring started",
            "ACTIVE"
        )

    else:

        print("Model is not deployed.")
        print("Runtime monitoring cannot start.")

        log_event(
            "Runtime monitoring attempted before deployment",
            "WARNING"
        )


def detect_security_incident(role, action):
    """
    Detect unauthorized runtime operations.
    """

    print()
    print("------------------------------------------------------------")
    print("SECURITY EVENT DETECTION")
    print("------------------------------------------------------------")

    allowed_actions = {
        "ml_engineer": {
            "predict",
            "monitor",
            "deploy"
        },

        "admin": {
            "predict",
            "monitor",
            "deploy"
        },

        "viewer": {
            "view"
        }
    }

    permissions = allowed_actions.get(
        role,
        set()
    )

    if action in permissions:

        print(
            f"[SECURITY OK] {role} -> {action}"
        )

        log_event(
            f"{role} performed {action}",
            "ALLOW"
        )

    else:

        print(
            f"[SECURITY ALERT] "
            f"{role} attempted {action}"
        )

        log_event(
            f"Unauthorized action: {role} -> {action}",
            "INCIDENT"
        )


def display_monitoring_report():
    """
    Display deployment and security monitoring report.
    """

    print()
    print("============================================================")
    print("DEPLOYMENT & MONITORING REPORT")
    print("============================================================")

    print(
        f"Deployment Status : "
        f"{'DEPLOYED' if deployment_status else 'NOT DEPLOYED'}"
    )

    print(
        f"Security Events   : "
        f"{len(security_events)}"
    )

    print()
    print("Security Event Log")
    print("------------------------------------------------------------")

    for event in security_events:

        print(
            f"{event['time']} | "
            f"{event['status']:9s} | "
            f"{event['event']}"
        )

    print("============================================================")


def main():

    print()
    print("============================================================")
    print("PHASE 4 — DEPLOY & MONITOR")
    print("============================================================")

    # --------------------------------------------------------
    # Step 1: Authorized deployment
    # --------------------------------------------------------

    print()
    print("[STEP 1] Authorized Deployment")

    deploy_model("ml_engineer")

    # --------------------------------------------------------
    # Step 2: Start runtime monitoring
    # --------------------------------------------------------

    print()
    print("[STEP 2] Runtime Monitoring")

    monitor_runtime()

    # --------------------------------------------------------
    # Step 3: Normal runtime operation
    # --------------------------------------------------------

    print()
    print("[STEP 3] Normal Runtime Activity")

    detect_security_incident(
        "ml_engineer",
        "predict"
    )

    detect_security_incident(
        "ml_engineer",
        "monitor"
    )

    # --------------------------------------------------------
    # Step 4: Unauthorized activity
    # --------------------------------------------------------

    print()
    print("[STEP 4] Unauthorized Activity Detection")

    detect_security_incident(
        "viewer",
        "deploy"
    )

    detect_security_incident(
        "viewer",
        "predict"
    )

    # --------------------------------------------------------
    # Step 5: Unauthorized deployment
    # --------------------------------------------------------

    print()
    print("[STEP 5] Unauthorized Deployment Test")

    deploy_model("viewer")

    # --------------------------------------------------------
    # Step 6: Final monitoring report
    # --------------------------------------------------------

    print()
    print("[STEP 6] Final Monitoring Report")

    display_monitoring_report()

    print()
    print("============================================================")
    print("PHASE 4 — DEPLOY & MONITOR COMPLETED")
    print("============================================================")


if __name__ == "__main__":
    main()
