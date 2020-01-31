(define (domain deployment_domain)
	(:requirements :typing :derived-predicates :strips :existential-preconditions :equality)
	(:types component_type abstract_component_type component reqcap)
	(:constants )
	(:predicates 
		(is_used ?c - component)
		(inherits_from ?type - component_type ?abstractType - abstract_component_type)
		(is_of_type ?comp - component ?type - component_type)
		(has_requirement ?type - component_type ?req - reqcap)
		(has_capability ?type - component_type ?cap - reqcap)
		(connected_with ?source - component ?target - component)
		(has_parent_type ?childType - abstract_component_type ?parentType - abstract_component_type)

		; derived predicates
		(check_all_nodes)
		(of_abstract_type ?comp - component ?parentType - abstract_component_type)
		(resolve_requirements ?comp - component ?compType - component_type)
		(resolve_specific_relation ?source - component ?target - component ?req - reqcap)
		(share_supertype ?type1 - abstract_component_type ?type2 - abstract_component_type)
	)
	
	(:derived (check_all_nodes)
		(forall (?comp - component)
				(or (not (is_used ?comp))
					(exists (?type - component_type)
						(and (is_of_type ?comp ?type)
					 		(resolve_requirements ?comp ?type))))))

	(:derived (of_abstract_type ?comp - component ?parentType - abstract_component_type)
		(exists (?type - component_type)
			(and (is_of_type ?comp ?type)
				 (inherits_from ?type ?parentType))))

	(:derived (resolve_requirements ?comp - component ?type - component_type)
		(forall (?req - reqcap)
				(or (not (has_requirement ?type ?req))
					(exists (?target - component)
						(and (resolve_specific_relation ?comp ?target ?req)
							 (connected_with ?comp ?target))))))

	(:derived (resolve_specific_relation ?source - component ?target - component ?req - reqcap)
		(exists (?sourceType - component_type ?targetType - component_type)
			(and (is_used ?source)
				 (is_used ?target)
				 (is_of_type ?source ?sourceType)
				 (is_of_type ?target ?targetType)
				 (has_requirement ?sourceType ?req)
				 (has_capability ?targetType ?req))))

	(:derived (share_supertype ?type1 - abstract_component_type ?type2 - abstract_component_type)
			(exists (?super - abstract_component_type)
				(and (has_parent_type ?type1 ?super)
					(has_parent_type ?type2 ?super))))

	(:action connect_components 
		:parameters (?source - component ?sourceType - component_type ?target - component ?targetType - component_type)

		:precondition (and (not(connected_with ?source ?target))
						   (is_of_type ?source ?sourceType)
						   (is_of_type ?target ?targetType)
						   (exists (?req - reqcap)
						   		(and (has_requirement ?sourceType ?req)
						   			 (has_capability ?targetType ?req))))

		:effect (connected_with ?source ?target))

	(:action disconnect_components
		:parameters (?source - component ?target - component)

		:precondition (connected_with ?source ?target)
					
		:effect (not (connected_with ?source ?target)))


	(:action change_type
		:parameters (?comp - component ?oldType - component_type ?newType - component_type)

		:precondition (and  (is_of_type ?comp ?oldType) 
							(exists (?parentType - abstract_component_type)
								(and (inherits_from ?oldType ?parentType)
									 (inherits_from ?newType ?parentType))))

		:effect (and (is_of_type ?comp ?newType)
					 (not(is_of_type ?comp ?oldType))))

	(:action change_type_by_ancestor
		:parameters (?comp - component ?compType - component_type ?compAbstractType - abstract_component_type ?newType - component_type ?newAbstractType - abstract_component_type)

		:precondition (and  (is_of_type ?comp ?compType) 
							(inherits_from ?compType ?compAbstractType)
							(inherits_from ?newType ?newAbstractType) 
							(not (= ?newAbstractType ?compAbstractType))
							(share_supertype ?compAbstractType ?newAbstractType))

		:effect (and (is_of_type ?comp ?newType)
					 (not (is_of_type ?comp ?compType))))

	(:action add_component
		:parameters (?comp - component ?type - component_type)

		:precondition (not (is_used ?comp))

		:effect (and (is_used ?comp)
					 (is_of_type ?comp ?type)))

	(:action remove_component
		:parameters (?comp - component ?type - component_type)

		:precondition (and (is_used ?comp)
							(is_of_type ?comp ?type))

		:effect (and (not (is_used ?comp))
					 (not (is_of_type ?comp ?type))))
)