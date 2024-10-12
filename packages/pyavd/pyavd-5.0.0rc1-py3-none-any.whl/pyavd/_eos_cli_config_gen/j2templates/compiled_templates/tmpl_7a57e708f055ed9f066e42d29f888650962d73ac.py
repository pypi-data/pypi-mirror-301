from jinja2.runtime import LoopContext, Macro, Markup, Namespace, TemplateNotFound, TemplateReference, TemplateRuntimeError, Undefined, escape, identity, internalcode, markup_join, missing, str_join
name = 'eos/router-ospf.j2'

def root(context, missing=missing):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    concat = environment.concat
    cond_expr_undefined = Undefined
    if 0: yield None
    l_0_router_ospf = resolve('router_ospf')
    try:
        t_1 = environment.filters['arista.avd.natural_sort']
    except KeyError:
        @internalcode
        def t_1(*unused):
            raise TemplateRuntimeError("No filter named 'arista.avd.natural_sort' found.")
    try:
        t_2 = environment.filters['indent']
    except KeyError:
        @internalcode
        def t_2(*unused):
            raise TemplateRuntimeError("No filter named 'indent' found.")
    try:
        t_3 = environment.tests['arista.avd.defined']
    except KeyError:
        @internalcode
        def t_3(*unused):
            raise TemplateRuntimeError("No test named 'arista.avd.defined' found.")
    try:
        t_4 = environment.tests['defined']
    except KeyError:
        @internalcode
        def t_4(*unused):
            raise TemplateRuntimeError("No test named 'defined' found.")
    pass
    for l_1_process_id in t_1(environment.getattr((undefined(name='router_ospf') if l_0_router_ospf is missing else l_0_router_ospf), 'process_ids'), 'id'):
        l_1_redistribute_bgp_cli = resolve('redistribute_bgp_cli')
        l_1_redistribute_connected_cli = resolve('redistribute_connected_cli')
        l_1_redistribute_static_cli = resolve('redistribute_static_cli')
        l_1_timer_ospf_spf_delay = resolve('timer_ospf_spf_delay')
        l_1_timer_ospf_lsa_tx = resolve('timer_ospf_lsa_tx')
        l_1_max_metric_router_lsa_cli = resolve('max_metric_router_lsa_cli')
        l_1_default_information_originate_cli = resolve('default_information_originate_cli')
        _loop_vars = {}
        pass
        yield '!\n'
        if t_3(environment.getattr(l_1_process_id, 'vrf')):
            pass
            yield 'router ospf '
            yield str(environment.getattr(l_1_process_id, 'id'))
            yield ' vrf '
            yield str(environment.getattr(l_1_process_id, 'vrf'))
            yield '\n'
        else:
            pass
            yield 'router ospf '
            yield str(environment.getattr(l_1_process_id, 'id'))
            yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'router_id')):
            pass
            yield '   router-id '
            yield str(environment.getattr(l_1_process_id, 'router_id'))
            yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'auto_cost_reference_bandwidth')):
            pass
            yield '   auto-cost reference-bandwidth '
            yield str(environment.getattr(l_1_process_id, 'auto_cost_reference_bandwidth'))
            yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'bfd_enable'), True):
            pass
            yield '   bfd default\n'
        if t_3(environment.getattr(l_1_process_id, 'bfd_adjacency_state_any'), True):
            pass
            yield '   bfd adjacency state any\n'
        if t_3(environment.getattr(l_1_process_id, 'distance')):
            pass
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'intra_area')):
                pass
                yield '   distance ospf intra-area '
                yield str(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'intra_area'))
                yield '\n'
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'external')):
                pass
                yield '   distance ospf external '
                yield str(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'external'))
                yield '\n'
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'inter_area')):
                pass
                yield '   distance ospf inter-area '
                yield str(environment.getattr(environment.getattr(l_1_process_id, 'distance'), 'inter_area'))
                yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'passive_interface_default'), True):
            pass
            yield '   passive-interface default\n'
        if t_3(environment.getattr(l_1_process_id, 'no_passive_interfaces')):
            pass
            for l_2_interface in t_1(environment.getattr(l_1_process_id, 'no_passive_interfaces')):
                _loop_vars = {}
                pass
                yield '   no passive-interface '
                yield str(l_2_interface)
                yield '\n'
            l_2_interface = missing
        if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'enabled'), True):
            pass
            l_1_redistribute_bgp_cli = 'redistribute bgp'
            _loop_vars['redistribute_bgp_cli'] = l_1_redistribute_bgp_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'include_leaked'), True):
                pass
                l_1_redistribute_bgp_cli = str_join(((undefined(name='redistribute_bgp_cli') if l_1_redistribute_bgp_cli is missing else l_1_redistribute_bgp_cli), ' include leaked', ))
                _loop_vars['redistribute_bgp_cli'] = l_1_redistribute_bgp_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'route_map')):
                pass
                l_1_redistribute_bgp_cli = str_join(((undefined(name='redistribute_bgp_cli') if l_1_redistribute_bgp_cli is missing else l_1_redistribute_bgp_cli), ' route-map ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'bgp'), 'route_map'), ))
                _loop_vars['redistribute_bgp_cli'] = l_1_redistribute_bgp_cli
            yield '   '
            yield str((undefined(name='redistribute_bgp_cli') if l_1_redistribute_bgp_cli is missing else l_1_redistribute_bgp_cli))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'enabled'), True):
            pass
            l_1_redistribute_connected_cli = 'redistribute connected'
            _loop_vars['redistribute_connected_cli'] = l_1_redistribute_connected_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'include_leaked'), True):
                pass
                l_1_redistribute_connected_cli = str_join(((undefined(name='redistribute_connected_cli') if l_1_redistribute_connected_cli is missing else l_1_redistribute_connected_cli), ' include leaked', ))
                _loop_vars['redistribute_connected_cli'] = l_1_redistribute_connected_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'route_map')):
                pass
                l_1_redistribute_connected_cli = str_join(((undefined(name='redistribute_connected_cli') if l_1_redistribute_connected_cli is missing else l_1_redistribute_connected_cli), ' route-map ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'connected'), 'route_map'), ))
                _loop_vars['redistribute_connected_cli'] = l_1_redistribute_connected_cli
            yield '   '
            yield str((undefined(name='redistribute_connected_cli') if l_1_redistribute_connected_cli is missing else l_1_redistribute_connected_cli))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'enabled'), True):
            pass
            l_1_redistribute_static_cli = 'redistribute static'
            _loop_vars['redistribute_static_cli'] = l_1_redistribute_static_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'include_leaked'), True):
                pass
                l_1_redistribute_static_cli = str_join(((undefined(name='redistribute_static_cli') if l_1_redistribute_static_cli is missing else l_1_redistribute_static_cli), ' include leaked', ))
                _loop_vars['redistribute_static_cli'] = l_1_redistribute_static_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'route_map')):
                pass
                l_1_redistribute_static_cli = str_join(((undefined(name='redistribute_static_cli') if l_1_redistribute_static_cli is missing else l_1_redistribute_static_cli), ' route-map ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'redistribute'), 'static'), 'route_map'), ))
                _loop_vars['redistribute_static_cli'] = l_1_redistribute_static_cli
            yield '   '
            yield str((undefined(name='redistribute_static_cli') if l_1_redistribute_static_cli is missing else l_1_redistribute_static_cli))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(l_1_process_id, 'distribute_list_in'), 'route_map')):
            pass
            yield '   distribute-list route-map '
            yield str(environment.getattr(environment.getattr(l_1_process_id, 'distribute_list_in'), 'route_map'))
            yield ' in\n'
        for l_2_area in t_1(environment.getattr(l_1_process_id, 'areas'), 'id'):
            l_2_stub_area_cli = resolve('stub_area_cli')
            l_2_namespace = resolve('namespace')
            l_2_ns = resolve('ns')
            l_2_nssa_area_cli = resolve('nssa_area_cli')
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_2_area, 'type'), 'stub'):
                pass
                l_2_stub_area_cli = str_join(('area ', environment.getattr(l_2_area, 'id'), ' stub', ))
                _loop_vars['stub_area_cli'] = l_2_stub_area_cli
                if t_3(environment.getattr(l_2_area, 'no_summary'), True):
                    pass
                    l_2_stub_area_cli = str_join(((undefined(name='stub_area_cli') if l_2_stub_area_cli is missing else l_2_stub_area_cli), ' no-summary', ))
                    _loop_vars['stub_area_cli'] = l_2_stub_area_cli
                yield '   '
                yield str((undefined(name='stub_area_cli') if l_2_stub_area_cli is missing else l_2_stub_area_cli))
                yield '\n'
            if t_3(environment.getattr(l_2_area, 'type'), 'nssa'):
                pass
                l_2_ns = context.call((undefined(name='namespace') if l_2_namespace is missing else l_2_namespace), print_nssa=True, _loop_vars=_loop_vars)
                _loop_vars['ns'] = l_2_ns
                l_2_nssa_area_cli = str_join(('area ', environment.getattr(l_2_area, 'id'), ' nssa', ))
                _loop_vars['nssa_area_cli'] = l_2_nssa_area_cli
                if t_3(environment.getattr(l_2_area, 'no_summary'), True):
                    pass
                    if not isinstance(l_2_ns, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_ns['print_nssa'] = False
                    yield '   '
                    yield str((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli))
                    yield ' no-summary\n'
                if t_4(environment.getattr(l_2_area, 'default_information_originate')):
                    pass
                    if not isinstance(l_2_ns, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_ns['print_nssa'] = True
                    l_2_nssa_area_cli = str_join(((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli), ' default-information-originate', ))
                    _loop_vars['nssa_area_cli'] = l_2_nssa_area_cli
                    if t_3(environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric')):
                        pass
                        l_2_nssa_area_cli = str_join(((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli), ' metric ', environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric'), ))
                        _loop_vars['nssa_area_cli'] = l_2_nssa_area_cli
                    if t_3(environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric_type')):
                        pass
                        l_2_nssa_area_cli = str_join(((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli), ' metric-type ', environment.getattr(environment.getattr(l_2_area, 'default_information_originate'), 'metric_type'), ))
                        _loop_vars['nssa_area_cli'] = l_2_nssa_area_cli
                if t_3(environment.getattr(l_2_area, 'nssa_only'), True):
                    pass
                    if not isinstance(l_2_ns, Namespace):
                        raise TemplateRuntimeError("cannot assign attribute on non-namespace object")
                    l_2_ns['print_nssa'] = True
                    l_2_nssa_area_cli = str_join(((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli), ' nssa-only', ))
                    _loop_vars['nssa_area_cli'] = l_2_nssa_area_cli
                if (environment.getattr((undefined(name='ns') if l_2_ns is missing else l_2_ns), 'print_nssa') == True):
                    pass
                    yield '   '
                    yield str((undefined(name='nssa_area_cli') if l_2_nssa_area_cli is missing else l_2_nssa_area_cli))
                    yield '\n'
            for l_3_filter_network in t_1(environment.getattr(environment.getattr(l_2_area, 'filter'), 'networks')):
                _loop_vars = {}
                pass
                yield '   area '
                yield str(environment.getattr(l_2_area, 'id'))
                yield ' filter '
                yield str(l_3_filter_network)
                yield '\n'
            l_3_filter_network = missing
            if t_3(environment.getattr(environment.getattr(l_2_area, 'filter'), 'prefix_list')):
                pass
                yield '   area '
                yield str(environment.getattr(l_2_area, 'id'))
                yield ' filter prefix-list '
                yield str(environment.getattr(environment.getattr(l_2_area, 'filter'), 'prefix_list'))
                yield '\n'
        l_2_area = l_2_stub_area_cli = l_2_namespace = l_2_ns = l_2_nssa_area_cli = missing
        for l_2_network_prefix in t_1(environment.getattr(l_1_process_id, 'network_prefixes'), 'ipv4_prefix'):
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_2_network_prefix, 'area')):
                pass
                yield '   network '
                yield str(environment.getattr(l_2_network_prefix, 'ipv4_prefix'))
                yield ' area '
                yield str(environment.getattr(l_2_network_prefix, 'area'))
                yield '\n'
        l_2_network_prefix = missing
        if t_3(environment.getattr(l_1_process_id, 'max_lsa')):
            pass
            yield '   max-lsa '
            yield str(environment.getattr(l_1_process_id, 'max_lsa'))
            yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'log_adjacency_changes_detail'), True):
            pass
            yield '   log-adjacency-changes detail\n'
        if ((t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'initial')) and t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'min'))) and t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'max'))):
            pass
            l_1_timer_ospf_spf_delay = 'timers spf delay initial'
            _loop_vars['timer_ospf_spf_delay'] = l_1_timer_ospf_spf_delay
            l_1_timer_ospf_spf_delay = str_join(((undefined(name='timer_ospf_spf_delay') if l_1_timer_ospf_spf_delay is missing else l_1_timer_ospf_spf_delay), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'initial'), ))
            _loop_vars['timer_ospf_spf_delay'] = l_1_timer_ospf_spf_delay
            l_1_timer_ospf_spf_delay = str_join(((undefined(name='timer_ospf_spf_delay') if l_1_timer_ospf_spf_delay is missing else l_1_timer_ospf_spf_delay), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'min'), ))
            _loop_vars['timer_ospf_spf_delay'] = l_1_timer_ospf_spf_delay
            l_1_timer_ospf_spf_delay = str_join(((undefined(name='timer_ospf_spf_delay') if l_1_timer_ospf_spf_delay is missing else l_1_timer_ospf_spf_delay), ' ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'spf_delay'), 'max'), ))
            _loop_vars['timer_ospf_spf_delay'] = l_1_timer_ospf_spf_delay
            yield '   '
            yield str((undefined(name='timer_ospf_spf_delay') if l_1_timer_ospf_spf_delay is missing else l_1_timer_ospf_spf_delay))
            yield '\n'
        if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'rx_min_interval')):
            pass
            yield '   timers lsa rx min interval '
            yield str(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'rx_min_interval'))
            yield '\n'
        if ((t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'initial')) and t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'min'))) and t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'max'))):
            pass
            l_1_timer_ospf_lsa_tx = 'timers lsa tx delay initial'
            _loop_vars['timer_ospf_lsa_tx'] = l_1_timer_ospf_lsa_tx
            l_1_timer_ospf_lsa_tx = str_join(((undefined(name='timer_ospf_lsa_tx') if l_1_timer_ospf_lsa_tx is missing else l_1_timer_ospf_lsa_tx), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'initial'), ))
            _loop_vars['timer_ospf_lsa_tx'] = l_1_timer_ospf_lsa_tx
            l_1_timer_ospf_lsa_tx = str_join(((undefined(name='timer_ospf_lsa_tx') if l_1_timer_ospf_lsa_tx is missing else l_1_timer_ospf_lsa_tx), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'min'), ))
            _loop_vars['timer_ospf_lsa_tx'] = l_1_timer_ospf_lsa_tx
            l_1_timer_ospf_lsa_tx = str_join(((undefined(name='timer_ospf_lsa_tx') if l_1_timer_ospf_lsa_tx is missing else l_1_timer_ospf_lsa_tx), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'timers'), 'lsa'), 'tx_delay'), 'max'), ))
            _loop_vars['timer_ospf_lsa_tx'] = l_1_timer_ospf_lsa_tx
            yield '   '
            yield str((undefined(name='timer_ospf_lsa_tx') if l_1_timer_ospf_lsa_tx is missing else l_1_timer_ospf_lsa_tx))
            yield '\n'
        if t_3(environment.getattr(l_1_process_id, 'maximum_paths')):
            pass
            yield '   maximum-paths '
            yield str(environment.getattr(l_1_process_id, 'maximum_paths'))
            yield '\n'
        if t_4(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa')):
            pass
            l_1_max_metric_router_lsa_cli = 'max-metric router-lsa'
            _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa')):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' external-lsa', ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa'), 'override_metric')):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'external_lsa'), 'override_metric'), ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'include_stub'), True):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' include-stub', ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'on_startup')):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' on-startup ', environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'on_startup'), ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_4(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa')):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' summary-lsa', ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            if t_3(environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa'), 'override_metric')):
                pass
                l_1_max_metric_router_lsa_cli = str_join(((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli), ' ', environment.getattr(environment.getattr(environment.getattr(environment.getattr(l_1_process_id, 'max_metric'), 'router_lsa'), 'summary_lsa'), 'override_metric'), ))
                _loop_vars['max_metric_router_lsa_cli'] = l_1_max_metric_router_lsa_cli
            yield '   '
            yield str((undefined(name='max_metric_router_lsa_cli') if l_1_max_metric_router_lsa_cli is missing else l_1_max_metric_router_lsa_cli))
            yield '\n'
        if t_4(environment.getattr(l_1_process_id, 'default_information_originate')):
            pass
            l_1_default_information_originate_cli = 'default-information originate'
            _loop_vars['default_information_originate_cli'] = l_1_default_information_originate_cli
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'always'), True):
                pass
                l_1_default_information_originate_cli = str_join(((undefined(name='default_information_originate_cli') if l_1_default_information_originate_cli is missing else l_1_default_information_originate_cli), ' always', ))
                _loop_vars['default_information_originate_cli'] = l_1_default_information_originate_cli
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'metric')):
                pass
                l_1_default_information_originate_cli = str_join(((undefined(name='default_information_originate_cli') if l_1_default_information_originate_cli is missing else l_1_default_information_originate_cli), ' metric ', environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'metric'), ))
                _loop_vars['default_information_originate_cli'] = l_1_default_information_originate_cli
            if t_3(environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'metric_type')):
                pass
                l_1_default_information_originate_cli = str_join(((undefined(name='default_information_originate_cli') if l_1_default_information_originate_cli is missing else l_1_default_information_originate_cli), ' metric-type ', environment.getattr(environment.getattr(l_1_process_id, 'default_information_originate'), 'metric_type'), ))
                _loop_vars['default_information_originate_cli'] = l_1_default_information_originate_cli
            yield '   '
            yield str((undefined(name='default_information_originate_cli') if l_1_default_information_originate_cli is missing else l_1_default_information_originate_cli))
            yield '\n'
        for l_2_summary_address in t_1(environment.getattr(l_1_process_id, 'summary_addresses'), 'prefix'):
            _loop_vars = {}
            pass
            if t_3(environment.getattr(l_2_summary_address, 'tag')):
                pass
                yield '   summary-address '
                yield str(environment.getattr(l_2_summary_address, 'prefix'))
                yield ' tag '
                yield str(environment.getattr(l_2_summary_address, 'tag'))
                yield '\n'
            elif t_3(environment.getattr(l_2_summary_address, 'attribute_map')):
                pass
                yield '   summary-address '
                yield str(environment.getattr(l_2_summary_address, 'prefix'))
                yield ' attribute-map '
                yield str(environment.getattr(l_2_summary_address, 'attribute_map'))
                yield '\n'
            elif t_3(environment.getattr(l_2_summary_address, 'not_advertise'), True):
                pass
                yield '   summary-address '
                yield str(environment.getattr(l_2_summary_address, 'prefix'))
                yield ' not-advertise\n'
            else:
                pass
                yield '   summary-address '
                yield str(environment.getattr(l_2_summary_address, 'prefix'))
                yield '\n'
        l_2_summary_address = missing
        if t_3(environment.getattr(l_1_process_id, 'mpls_ldp_sync_default'), True):
            pass
            yield '   mpls ldp sync default\n'
        if t_3(environment.getattr(l_1_process_id, 'eos_cli')):
            pass
            yield '   '
            yield str(t_2(environment.getattr(l_1_process_id, 'eos_cli'), 3, False))
            yield '\n'
    l_1_process_id = l_1_redistribute_bgp_cli = l_1_redistribute_connected_cli = l_1_redistribute_static_cli = l_1_timer_ospf_spf_delay = l_1_timer_ospf_lsa_tx = l_1_max_metric_router_lsa_cli = l_1_default_information_originate_cli = missing

blocks = {}
debug_info = '7=36&9=47&10=50&12=57&14=59&15=62&17=64&18=67&20=69&23=72&26=75&27=77&28=80&30=82&31=85&33=87&34=90&37=92&40=95&41=97&42=101&45=104&46=106&47=108&48=110&50=112&51=114&53=117&55=119&56=121&57=123&58=125&60=127&61=129&63=132&65=134&66=136&67=138&68=140&70=142&71=144&73=147&75=149&76=152&78=154&80=161&81=163&82=165&83=167&85=170&88=172&90=174&91=176&92=178&93=180&94=184&96=186&97=188&98=191&99=193&100=195&102=197&103=199&106=201&107=203&108=206&110=208&111=211&115=213&116=217&118=222&119=225&122=230&123=233&124=236&127=241&128=244&130=246&133=249&136=251&137=253&138=255&139=257&140=260&142=262&143=265&145=267&148=269&149=271&150=273&151=275&152=278&154=280&155=283&157=285&158=287&159=289&160=291&162=293&163=295&165=297&166=299&168=301&169=303&171=305&172=307&174=309&175=311&177=314&179=316&180=318&181=320&182=322&184=324&185=326&187=328&188=330&190=333&192=335&193=338&194=341&195=345&196=348&197=352&198=355&200=360&203=363&206=366&207=369'