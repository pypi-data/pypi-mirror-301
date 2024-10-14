class JobEndpoints:
    """
    Endpoints related to jobs in Jenkins.

    Attributes
    ----------
    JOB_INFO : str
        URL template to get detailed information about a specific job.
    JOB_CONFIG : str
        URL template to get the configuration of a specific job.
    CREATE_JOB : str
        URL template to create a new job.
    DELETE_JOB : str
        URL template to delete a specific job.
    DISABLE_JOB : str
        URL template to disable a specific job.
    ENABLE_JOB : str
        URL template to enable a specific job.
    BUILD_JOB : str
        URL template to trigger a build for a specific job.
    BUILD_WITH_PARAMETERS : str
        URL template to trigger a build with parameters for a specific job.
    JOBS_QUERY : str
        URL template to query jobs with a specific tree structure.
    JOBS_QUERY_TREE : str
        URL template to define the tree structure for querying jobs.
    ALL_BUILDS : str
        URL template to get information about all builds for a specific job.
    """

    JOB_INFO: str = "{base_url}/api/json?depth={depth}"
    JOB_CONFIG: str = "{base_url}/config.xml"
    CREATE_JOB: str = "{folder_url}createItem?name={name}"
    DELETE_JOB: str = "{base_url}/doDelete"
    DISABLE_JOB: str = "{base_url}/disable"
    ENABLE_JOB: str = "{base_url}/enable"
    BUILD_JOB: str = "{base_url}/build"
    BUILD_WITH_PARAMETERS: str = "{base_url}/buildWithParameters"
    JOBS_QUERY: str = "?tree={string_value}"
    JOBS_QUERY_TREE: str = "jobs[url,color,name,{string_value}]"
    ALL_BUILDS: str = (
        "{base_url}/api/json?tree=allBuilds[number,inProgress,queueId,url,result,actions[_class,causes[_class,userId,userName],remoteUrls],changeSets[_class,items[commitId,author[fullName],authorEmail,date,msg,affectedPaths,paths[file,editType]]]]&depth=4"
    )
