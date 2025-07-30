QUERIES = {
    "count_priority-type_problem_report" : ''' SELECT priority, COUNT(*) as count from public.jira_snapshot
 	                            WHERE issue_type = 'Problem Report'  
 		                        AND _is_current = true
	                            GROUP BY priority''',
    "count_severity" : '''SELECT severity, count(*) FROM public.jira_snapshot
    	                    WHERE _is_current 
	                        GROUP BY severity''',
    "count_all_elements" : '''SELECT count(*) FROM public.jira_snapshot
	                    WHERE _is_current ''',
    "count_jira_status" : '''SELECT jira_status, COUNT(*) FROM public.jira_snapshot
                                GROUP BY jira_status ORDER BY jira_status; ''',
    "count_open_prs" : '''SELECT priority, jira_status from public.jira_snapshot
	                        WHERE jira_status !='Closed' AND resolution IS NULL ''',
    "teams":'''SELECT agile_team FROM public.jira_snapshot
                group by agile_team
                order by agile_team''',
    "count_feature_status" : '''SELECT
                                CASE
                                WHEN jira_status IN ('In Progress', 'In Review') THEN 'In Progress/In Review'
                                ELSE jira_status
                                END AS status_group,
                                COUNT(*)
                                FROM public.jira_snapshot
                                WHERE issue_type = 'Story' 
                                GROUP BY status_group
                                ORDER BY status_group ''',
    "crd_implemented_requirements" : '''WITH subtask_status AS (
                                        SELECT
                                            s.crd_id,
                                            bool_and(lower(s.syrd_state) = 'released') AS any_released
                                        FROM SYRD s
                                        GROUP BY s.crd_id
                                    ),
                                    
                                    task_status AS (
                                        SELECT
                                            c.id,
                                            CASE
                                                WHEN sts.any_released = TRUE THEN 'Implemented'
                                                ELSE 'Not Implemented'
                                            END AS implementation_status
                                        FROM CRD c
                                        LEFT JOIN subtask_status sts ON c.id = sts.crd_id
                                    )
                                    
                                    SELECT
                                        implementation_status,
                                        COUNT(*) AS count
                                    FROM
                                        task_status
                                    GROUP BY
                                        implementation_status;
                                    ''',
    "count_all_implemententions" : '''WITH subtask_status AS (
                                        SELECT
                                            s.crd_id,
                                            bool_and(s.syrd_state = 'released') AS any_released
                                        FROM SYRD s
                                        GROUP BY s.crd_id
                                    )
                                    
                                    SELECT
                                        COUNT(*) AS count
                                    FROM
                                        CRD c
                                        {where_section}
                                    LEFT JOIN
                                        subtask_status sts ON c.id = sts.crd_id;

                                    ''',
    "crd_test_requirement_level" : '''SELECT requirement_level,test_level FROM public.crd ''',

    "sys_sw_testcases" :  '''  WITH syrd_with_testcase AS (
		                        SELECT DISTINCT syrd_id
		                        FROM testcase
                                )

                                SELECT 
	                                CASE WHEN s.id IN (SELECT syrd_id  FROM syrd_with_testcase) 
	                                THEN 'Has Test Case' ELSE 'No Test Case' END AS test_case_status,
	                            COUNT(*) AS count
                                FROM syrd s
                                GROUP BY test_case_status; ''',
    "syrd_requirement_status" : '''SELECT syrd_state,COUNT(syrd_state) as count FROM public.syrd
                                Group by syrd_state
								ORDER BY syrd_state ASC
								''',
    "total_syrd_requirement" : '''SELECT count(syrd_state) as count FROM public.syrd'''
}