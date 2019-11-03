(define (problem running_example)
	(:domain deployment_domain)
	(:objects
		ubuntu - abstract_component_type
		ubuntu-804 - component_type
		ubuntu-1804 - component_type
		tomcat - abstract_component_type
		tomcat-7 - component_type
		java - abstract_component_type
		java-6 - component_type
		java-8 - component_type
		java-webshop-1 - component_type
		mysqldb-51 - component_type
		mysqldbms-51 - component_type

		comp0 - component
		comp1 - component
		comp2 - component
		comp3 - component
		comp4 - component
		comp5 - component
		comp6 - component

		hosted_on_ubuntu_18 - reqcap
		hosted_on_ubuntu_8 - reqcap
		hosted_somewhere - reqcap
		hosted_on_dbms - reqcap
		db_connection - reqcap
		hosted_on_tomcat - reqcap
		java-runtime - reqcap
	)
	(:init
		(has_abstract_type ubuntu-804 ubuntu)
		(has_abstract_type ubuntu-1804 ubuntu)
		(has_abstract_type tomcat-7 tomcat)
		(has_abstract_type java-6 java)
		(has_abstract_type java-8 java)

		(has_requirement java-6 hosted_on_ubuntu_8)
		(has_requirement java-8 hosted_on_ubuntu_18)
		(has_requirement mysqldbms-51 hosted_somewhere)
		(has_requirement mysqldb-51 hosted_on_dbms)
		(has_requirement java-webshop-1 hosted_on_tomcat)
		(has_requirement java-webshop-1 db_connection)
		(has_requirement tomcat-7 hosted_somewhere)
		(has_requirement tomcat-7 java-runtime)

		(has_capability ubuntu-804 hosted_on_ubuntu_8)
		(has_capability ubuntu-804 hosted_somewhere)
		(has_capability ubuntu-1804 hosted_on_ubuntu_18)
		(has_capability ubuntu-1804 hosted_somewhere)
		(has_capability mysqldb-51 db_connection)
		(has_capability mysqldbms-51 hosted_on_dbms)
		(has_capability tomcat-7 hosted_on_tomcat)
		(has_capability java-6 java-runtime)
		(has_capability java-8 java-runtime)

		(is_used comp0)
		(has_type comp0 ubuntu-804)
		(is_used comp1)
		(has_type comp1 java-6)
		(connected_with comp1 comp0)
		(is_used comp2)
		(has_type comp2 tomcat-7)
		(connected_with comp2 comp0)
		(connected_with comp2 comp1)
		(is_used comp3)
		(has_type comp3 java-webshop-1)
		(connected_with comp3 comp2)
		(is_used comp4)
		(has_type comp4 mysqldb-51)
		(connected_with comp4 comp5)
		(connected_with comp3 comp4)
		(is_used comp5)
		(has_type comp5 mysqldbms-51)
		(connected_with comp5 comp6)
		(is_used comp6)
		(has_type comp6 ubuntu-804)
	)

	(:goal
		(and (check_all_nodes)
			(is_used comp3)
			(has_type comp3 java-webshop-1)
			(is_used comp0)
			(has_type comp0 ubuntu-1804)
			(is_used comp6)
			(has_type comp6 ubuntu-1804)))
)