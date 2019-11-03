(define (domain deployment_domain)
	(:requirements :typing :derived-predicates :strips :existential-preconditions :equality)
	(:types component_type abstract_component_type component reqcap)
	(:constants )
	(:predicates 
		(is_used ?c - component)
		(has_parent_type ?t0 - abstract_component_type ?t1 - abstract_component_type)
		(has_abstract_type ?v - component_type ?t - abstract_component_type)
		(has_type ?c - component ?v - component_type)
		(has_requirement ?v - component_type ?r - reqcap)
		(has_capability ?v - component_type ?r - reqcap)
		(connected_with ?c0 - component ?c1 - component)
		(has_supertype ?t0 - abstract_component_type ?t1 - abstract_component_type)
		(share_supertype ?t0 - abstract_component_type ?t1 - abstract_component_type)
		(of_abstract_type ?n - component ?t - abstract_component_type)
		
		(check_all_nodes)
		(resolve_type ?n - component)
		(have_some_relation ?n - component)
		(resolve_requirements ?n - component ?v - component_type)
		(resolve_relation ?n0 - component ?n1 - component)
		(resolve_specific_relation ?n0 - component ?n1 - component ?r - reqcap))
	
	(:derived (check_all_nodes)
		(forall (?n - component)
				(or (not(is_used ?n))
					(and (resolve_type ?n)
						 (have_some_relation ?n)))))

	(:derived (of_abstract_type ?n - component ?t - abstract_component_type)
		(exists (?v - component_type)
			(and (has_type ?n ?v)
				 (has_abstract_type ?v ?t))))

	(:derived (resolve_type ?n - component)
		(exists (?v - component_type)
				(and (has_type ?n ?v)
					 (resolve_requirements ?n ?v))))

	(:derived (have_some_relation ?n - component)
		(forall (?n1 - component)
				(or (not(connected_with ?n ?n1))
					(resolve_relation ?n ?n1))))

	(:derived (resolve_requirements ?n - component ?v - component_type)
		(forall (?r - reqcap)
				(or (not(has_requirement ?v ?r))
					(exists (?n1 - component)
						(and (resolve_specific_relation ?n ?n1 ?r)
							 (connected_with ?n ?n1))))))

	(:derived (resolve_relation ?n0 - component ?n1 - component)
		(exists (?v0 - component_type ?v1 - component_type)
			(and (has_type ?n0 ?v0)
				 (has_type ?n1 ?v1)
				 (is_used ?n0)
				 (is_used ?n1)
				 (exists (?r - reqcap)
				 		 (and (has_requirement ?v0 ?r)
				 		 	  (has_capability ?v1 ?r))))))

	(:derived (resolve_specific_relation ?n0 - component ?n1 - component ?r - reqcap)
		(exists(?v0 - component_type ?v1 - component_type)
			(and (is_used ?n0)
				 (is_used ?n1)
				 (has_type ?n0 ?v0)
				 (has_type ?n1 ?v1)
				 (has_requirement ?v0 ?r)
				 (has_capability ?v1 ?r))))

	(:action connect_components 
		:parameters (?c0 - component ?v0 - component_type ?c1 - component ?v1 - component_type)

		:precondition (and (not(connected_with ?c0 ?c1))
						   (has_type ?c0 ?v0)
						   (has_type ?c1 ?v1)
						   (exists (?r - reqcap)
						   		(and (has_requirement ?v0 ?r)
						   			 (has_capability ?v1 ?r))))

		:effect (connected_with ?c0 ?c1))

	(:action disconnect_components
		:parameters (?c0 - component ?c1 - component)

		:precondition (connected_with ?c0 ?c1)
					
		:effect (not(connected_with ?c0 ?c1)))


	(:action change_type
		:parameters (?i - component ?cV - component_type ?oV - component_type)

		:precondition (and  (has_type ?i ?oV) 
							(exists (?t - abstract_component_type)
								(and (has_abstract_type ?oV ?t)
									 (has_abstract_type ?cV ?t))))

		:effect (and (has_type ?i ?cV)
					 (not(has_type ?i ?oV))))

	(:action change_type_by_ancestor
		:parameters (?i - component ?cV - component_type ?cT - abstract_component_type ?oV - component_type ?oT - abstract_component_type)

		:precondition (and  (has_type ?i ?oV) 
							(has_abstract_type ?cV ?cT)
							(has_abstract_type ?oV ?oT) 
							(not (= ?oT ?cT))
							(share_supertype ?cT ?oT))

		:effect (and (has_type ?i ?cV)
					 (not(has_type ?i ?oV))))

	(:action add_component
		:parameters (?i - component ?v - component_type)

		:precondition (not (is_used ?i))

		:effect (and (is_used ?i)
					 (has_type ?i ?v)))

	(:action remove_component
		:parameters (?i - component ?v - component_type)

		:precondition (and (is_used ?i)
						   	(has_type ?i ?v))

		:effect (and (not(is_used ?i))
					 (not(has_type ?i ?v))))
)