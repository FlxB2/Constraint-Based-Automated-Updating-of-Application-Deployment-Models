(define (domain deployment_domain)
	(:requirements :typing :derived-predicates :strips :existential-preconditions :equality)
	(:types component_type abstract_component_type component reqcap)
	(:constants )
	(:predicates 
		(is_used ?c - component)
		(inherits_from ?v - component_type ?t - abstract_component_type)
		(is_of_type ?c - component ?v - component_type)
		(has_requirement ?v - component_type ?r - reqcap)
		(has_capability ?v - component_type ?r - reqcap)
		(connected_with ?c0 - component ?c1 - component)
		(share_supertype ?t0 - abstract_component_type ?t1 - abstract_component_type)
		(of_abstract_type ?n - component ?t - abstract_component_type)
		
		(check_all_nodes)
		(resolve_requirements ?n - component ?v - component_type)
		(resolve_specific_relation ?n0 - component ?n1 - component ?r - reqcap))
	
	(:derived (check_all_nodes)
		(forall (?n - component)
				(or (not(is_used ?n))
					(exists (?v - component_type)
						(and (is_of_type ?n ?v)
					 		(resolve_requirements ?n ?v))))))

	(:derived (of_abstract_type ?n - component ?t - abstract_component_type)
		(exists (?v - component_type)
			(and (is_of_type ?n ?v)
				 (inherits_from ?v ?t))))

	(:derived (resolve_requirements ?n - component ?v - component_type)
		(forall (?r - reqcap)
				(or (not(has_requirement ?v ?r))
					(exists (?n1 - component)
						(and (resolve_specific_relation ?n ?n1 ?r)
							 (connected_with ?n ?n1))))))

	(:derived (resolve_specific_relation ?n0 - component ?n1 - component ?r - reqcap)
		(exists(?v0 - component_type ?v1 - component_type)
			(and (is_used ?n0)
				 (is_used ?n1)
				 (is_of_type ?n0 ?v0)
				 (is_of_type ?n1 ?v1)
				 (has_requirement ?v0 ?r)
				 (has_capability ?v1 ?r))))

	(:action connect_components 
		:parameters (?c0 - component ?v0 - component_type ?c1 - component ?v1 - component_type)

		:precondition (and (not(connected_with ?c0 ?c1))
						   (is_of_type ?c0 ?v0)
						   (is_of_type ?c1 ?v1)
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

		:precondition (and  (is_of_type ?i ?oV) 
							(exists (?t - abstract_component_type)
								(and (inherits_from ?oV ?t)
									 (inherits_from ?cV ?t))))

		:effect (and (is_of_type ?i ?cV)
					 (not(is_of_type ?i ?oV))))

	(:action change_type_by_ancestor
		:parameters (?i - component ?cV - component_type ?cT - abstract_component_type ?oV - component_type ?oT - abstract_component_type)

		:precondition (and  (is_of_type ?i ?oV) 
							(inherits_from ?cV ?cT)
							(inherits_from ?oV ?oT) 
							(not (= ?oT ?cT))
							(share_supertype ?cT ?oT))

		:effect (and (is_of_type ?i ?cV)
					 (not(is_of_type ?i ?oV))))

	(:action add_component
		:parameters (?i - component ?v - component_type)

		:precondition (not (is_used ?i))

		:effect (and (is_used ?i)
					 (is_of_type ?i ?v)))

	(:action remove_component
		:parameters (?i - component ?v - component_type)

		:precondition (and (is_used ?i)
						   	(is_of_type ?i ?v))

		:effect (and (not(is_used ?i))
					 (not(is_of_type ?i ?v))))
)