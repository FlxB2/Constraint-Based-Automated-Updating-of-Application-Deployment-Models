(define (problem generated_problem)
	(:domain deployment_domain)
	(:objects 
		java_webshop-1 - component_type
		mysql_db-51 - component_type
		mysql_dbms-51 - component_type
		hoster-0xx1 - component_type
		ubuntu-12xx04 - component_type
		ubuntu-14xx04 - component_type
		ubuntu-16xx04 - component_type
		ubuntu-18xx04 - component_type
		java_runtime-6 - component_type
		tomcat-7 - component_type
		mysql_db-57 - component_type
		mysql_dbms-57 - component_type
		java_runtime-8 - component_type

		java - abstract_component_type
		compute - abstract_component_type
		webserver - abstract_component_type
		tomcat - abstract_component_type
		software_component - abstract_component_type
		ubuntu - abstract_component_type
		mysql_dbms - abstract_component_type
		mysql_db - abstract_component_type

		dbms_51 - reqcap
		ubuntu_12 - reqcap
		java_runtime_6 - reqcap
		dbms_57 - reqcap
		java_runtime_8 - reqcap
		db - reqcap
		debian_jessie - reqcap
		java_runtime - reqcap
		hosted_somewhere - reqcap
		debian_stretch - reqcap
		java_webcontainer - reqcap
		debian_buster - reqcap
		hypervisor - reqcap

		mysql_db0 - component
		java-runtime0 - component
		webshop0 - component
		mysql_dbms0 - component
		tomcat0 - component
		ubuntu0 - component
		ubuntu1 - component
	)
	(:init 
		( connected_with java-runtime0 ubuntu0 )
		( connected_with mysql_db0 mysql_dbms0 )
		( connected_with mysql_dbms0 ubuntu1 )
		( connected_with tomcat0 java-runtime0 )
		( connected_with tomcat0 ubuntu0 )
		( connected_with webshop0 mysql_db0 )
		( connected_with webshop0 tomcat0 )

		( has_capability hoster-0xx1 hypervisor )
		( has_capability java_runtime-6 java_runtime )
		( has_capability java_runtime-6 java_runtime_6 )
		( has_capability java_runtime-8 java_runtime )
		( has_capability java_runtime-8 java_runtime_8 )
		( has_capability mysql_db-51 db )
		( has_capability mysql_db-57 db )
		( has_capability mysql_dbms-51 dbms_51 )
		( has_capability mysql_dbms-57 dbms_57 )
		( has_capability tomcat-7 java_webcontainer )
		( has_capability ubuntu-12xx04 hosted_somewhere )
		( has_capability ubuntu-12xx04 ubuntu_12 )
		( has_capability ubuntu-14xx04 debian_jessie )
		( has_capability ubuntu-16xx04 debian_stretch )
		( has_capability ubuntu-16xx04 hosted_somewhere )
		( has_capability ubuntu-18xx04 debian_buster )
		( has_capability ubuntu-18xx04 hosted_somewhere )

		( has_parent_type tomcat webserver )
		( has_parent_type ubuntu compute )
		( has_parent_type webserver software_component )
		( has_parent_type mysql_dbms software_component )

		( has_requirement java_runtime-6 ubuntu_12 )
		( has_requirement java_runtime-8 debian_buster )
		( has_requirement java_webshop-1 db )
		( has_requirement java_webshop-1 java_webcontainer )
		( has_requirement mysql_db-51 dbms_51 )
		( has_requirement mysql_db-57 dbms_57 )
		( has_requirement mysql_dbms-51 ubuntu_12 )
		( has_requirement mysql_dbms-57 debian_buster )
		( has_requirement tomcat-7 hosted_somewhere )
		( has_requirement tomcat-7 java_runtime )

		( inherits_from java_runtime-6 java )
		( inherits_from java_runtime-8 java )
		( inherits_from mysql_dbms-51 mysql_dbms )
		( inherits_from mysql_dbms-57 mysql_dbms )
		( inherits_from mysql_db-51 mysql_db )
		( inherits_from mysql_db-57 mysql_db )
		( inherits_from tomcat-7 tomcat )
		( inherits_from ubuntu-12xx04 ubuntu )
		( inherits_from ubuntu-14xx04 ubuntu )
		( inherits_from ubuntu-16xx04 ubuntu )
		( inherits_from ubuntu-18xx04 ubuntu )

		( is_of_type java-runtime0 java_runtime-6 )
		( is_of_type mysql_db0 mysql_db-51 )
		( is_of_type mysql_dbms0 mysql_dbms-51 )
		( is_of_type tomcat0 tomcat-7 )
		( is_of_type ubuntu0 ubuntu-12xx04 )
		( is_of_type ubuntu1 ubuntu-12xx04 )
		( is_of_type webshop0 java_webshop-1 )

		( is_used webshop0  )
		( is_used tomcat0  )
		( is_used java-runtime0  )
		( is_used ubuntu0  )
		( is_used mysql_db0  )
		( is_used mysql_dbms0  )
		( is_used ubuntu1  )
	)
	(:goal 
		(and (check_all_nodes)

			( is_of_type ubuntu0 ubuntu-18xx04 )
			( is_of_type ubuntu1 ubuntu-18xx04 )
			( is_of_type webshop0 java_webshop-1 )
		)
	)
)