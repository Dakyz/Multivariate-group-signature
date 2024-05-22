class Constants:
    # resources constants
    PATH_TO_RES = "res/"
    PATH_TO_WORKER_RES = PATH_TO_RES + "company/user.png"
    PATH_TO_MANAGER_RES = PATH_TO_RES + "company/manager.png"

    # db
    DB_NAME = "database.db"

    # general constants
    COMPANIES_CNT = 2

    # group signature parameters
    q = 2
    m = 3
    n = 4
    rounds = 70

    # contracts signature parameters
    low_bound_k = 2 ** 159
    up_bound_k = 2 ** 160 - 200
    low_bound_n = 2 ** 860
    up_bound_n = 2 ** 864
