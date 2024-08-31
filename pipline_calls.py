def build_stage():
    print("BUILD STAGE CODE")

def test_stage():
    print("TEST STAGE CODE")

def code_quality_stage():
    print("CODE QUALITY ANALYSIS CODE")

def deploy_stage():
    print("DEPLOY TEST STAGE CODE")

def release_stage():
    print("PRODUCTION RELEASE STAGE CODE")

def monitoring_stage():
    print("MONITORING STAGE CODE")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        stage = sys.argv[1]
        if stage == "build":
            build_stage()
        elif stage == "test":
            test_stage()
        elif stage == "code_quality":
            code_quality_stage()
        elif stage == "deploy":
            deploy_stage()
        elif stage == "release":
            release_stage()
        elif stage == "monitoring":
            monitoring_stage()
        else:
            print("Unknown stage")
    else:
        print("No stage specified")
