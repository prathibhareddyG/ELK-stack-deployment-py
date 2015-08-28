import argparse

domain_default = ""
bro_cores_default = 1
bro_logs_default = '/var/opt/bro/logs'
bro_manager_default = 'localhost'
bro_proxy_default = 'localhost'
suricata_data_default = '/data/suricata/logs'
netsniff_interval_default = '1GiB'
netsniff_output_default = '/data/pcap'
es_node_name_default = ''
es_cluster_name_default = 'elasticsearch'
es_heap_default = 1
es_shards_default = 1
es_replica_default = 0
es_path_data_default = '/data/elasticsearch/data'
es_path_logs_default = '/data/elasticsearch/logs'
es_path_plugins_default = ''
es_path_work_default = '/data/elasticsearch/work'
es_master_discovery_default = ''
kafka_topic_default = ['bro_raw','suricata_raw']
logstash_bro_kafka_default = 'bro_raw'
logstash_suricata_kafka_default = 'suricata_raw'
logstash_bro_es_default = True
logstash_suricata_es_default = True
logstash_broker_es_default = ['bro_raw', 'suricata_raw']
kibana_nginx_default = 8080
install_bro_default = False
install_suricata_default = False
suricata_kafka_default = False
install_netsniff_default = False
install_elasticsearch_default = False
es_unicast_default = False
es_master_node_default = True
es_data_node_default = True
install_kafka_default = False
install_logstash_default = False
install_kibana_default = False

def get_args():

	def netsniff_interval(v):
		import re
		try:
				return re.match("^[1-9][0-9]*(KiB|MiB|GiB|sec|min|hrs|s)$", v).group(0)
		#Sad face my error handle is overridden by the parser Oh well.
		except:
			raise ValueError("String '%s' does not match required format <NUM>KiB/MiB/GiB/s/sec/min/hrs"%(v))
			
	parser = argparse.ArgumentParser(description="""Installs Sensor Software with defaults. 
	                                             All options are overridable at commandline.
												 This script will make some basic assumetions when installing.
												 When overriding fields the --install-[software] option can be ignored.
												 The script will assume you want that software installed.
												 If no software is choosen, this script will install all software with default values.
												 When installing logstash the default installation will install a elasticsearch master node.""",
												 epilog="""When installing Logstash the script will default to installing ES as a Master/Data node.
												 This is because the ultimate goal is to get data into elasticsearch.
												 You can use #######.py to modify exsisting software""")
	required_parser = parser.add_argument_group('required arguments')
	install_parser = parser.add_argument_group('install options')
	bro_parser = parser.add_argument_group('bro options')
	suricata_parser = parser.add_argument_group('suricata options')
	netsniff_parser = parser.add_argument_group('netsniff-ng options')
	es_parser = parser.add_argument_group('elasticsearch options')
	kafka_parser = parser.add_argument_group('kafka options')
	logstash_parser = parser.add_argument_group('logstash options')
	kibana_parser = parser.add_argument_group('kibana options')

	required_parser.add_argument('-H', '--host',type=str, help='Host Name', required=True)
	required_parser.add_argument('-I', '--interface', metavar='INTERFACE',type=str, help='Capture Interface', required=True)
	parser.add_argument('-d', '--domain',type=str,help='Domain name', required=False, default=domain_default)
	

	install_parser.add_argument('--install-bro',  action='store_true', help='Installs bro, brocontrol, pfring, java, dkms, libpcap-pfring and pfring-dkms', required=False, default=install_bro_default)
	#would like to set default to a % of available CPU power instead of hard coded number
	bro_parser.add_argument('--bro-cores', metavar='NUM', type=int, help='Number of cores for bro workers', required=False, default=bro_cores_default)
	bro_parser.add_argument('--bro-logs', metavar='DIR', type=str, help='Directory where bro should save logs', required=False, default=bro_logs_default)
	bro_parser.add_argument('--bro_manager', metavar='HOST', type=str, help='Host that is/will be the manager for a bro cluster', required=False, default=bro_manager_default)
	bro_parser.add_argument('--bro_proxy', metava='HOST', type=str, help='Host that is/will be the proxy for a bro cluster', required=False, default=bro_proxy_default)
	install_parser.add_argument('--install-suricata', action='store_true', help='Installs Suricata, dkms, pfring, libpcap-pfring and pfring-dkms', required=False, default=install_suricata_default)
	suricata_parser.add_argument('--suricata-data', metavar='DIR', help='Directory to store the eve.json', required=False, default=suricata_data_default)
	#parser option not yet implemented. Should have default value of True after implementation.
	suricata_parser.add_argument('--suricata-kafka', action='store_true', help='(Not Implemented)Will no longer write a eve.json and will push data directly into kafka', required=False, default=suricata_kafka_default)
	install_parser.add_argument('--install-netsniff', action='store_true', help='Installs netsniff-ng', required=False, default=install_netsniff_default)
	netsniff_parser.add_argument('--netsniff-interval', metavar='<num>KiB/MiB/GiB/s/sec/min/hrs', type=netsniff_interval, help='Interval for output pcap', required=False, default=netsniff_interval_default)
	netsniff_parser.add_argument('--netsniff-output', metavar='DIR/INTERFACE', type=str, help='Directory/Interface where netsniff-ng should send data', required=False, default=netsniff_output_default)
	install_parser.add_argument('--install-elasticsearch', action='store_true', help='Installs elasticsearch and java', required=False, default=install_elasticsearch_default)
	es_parser.add_argument('--elasticsearch-node-name', metavar='NAME', type=str, help='Sets current elasticsearch\'s node name', required=False, default=es_node_name_default)
	es_parser.add_argument('--elasticsearch-cluster-name', metavar='CLUSTER', type=str, help='Sets the cluster this elasticsearch node should connect to', required=False, default=es_cluster_name_default)
	#would like to set default to 50% or 32 depending on available RAM.
	es_parser.add_argument('--elasticsearch-heap', metavar='NUM', type=int, help='Sets the amount of RAM elasticsearch is able to use for indexing functions. Recommend 50 percent of availble ram, but no more than 32G', required=False, default=es_heap_default)
	# would be nice to dynamically set this but it would probably be a hassle. 
	es_parser.add_argument('--elasticsearch-shards', metavar='NUM', type=int, help='Sets the number of shards for elasticsearch. Recommend lower shard count for smaller configurations', required=False, default=es_shards_default)
	es_parser.add_argument('--elasticsearch-replica', metavar='NUM', type=int, help='Sets the number of replicas for elasticsearch. Replicas are used for failover, recommend zero if you have only 1 data node', required=False, default=es_replica_default)
	es_parser.add_argument('--elasticsearch-path-data', metavar='DIR', type=str, help='Directory to store elasticsearch data', required=False, default=es_path_data_default)
	es_parser.add_argument('--elasticsearch-path-logs', metavar='DIR', type=str, help='Directory to store elasticsearch logs', required=False, default=es_path_logs_default)
	# probably wont implement this. No plugins needed at this time
	es_parser.add_argument('--elasticsearch-path-plugins', metavar='DIR', type=str, help='Directory to elasticsearch plugins', required=False, default=es_path_plugins_default)
	es_parser.add_argument('--elasticsearch-path-work', metavar='DIR', type=str, help='Directory for elasticsearch to work out of', required=False, default=es_path_work_default)
	es_parser.add_argument('--elasticsearch-unicast', action='store_true', help='Enables unicast and disables multicast discovery. If enabled include the --elasticsearch-master-discovery field or elasticsearch wont be able the master nodes', required=False, default=es_unicast_default)
	es_parser.add_argument('--elasticsearch-master-discovery', metavar='"NODE', nargs='+', type=str, help='List of master nodes that can be discovered when this node starts ("192.168.1.11, 192.168.1.12, ect..")',required=False, default=es_master_discovery_default)
	es_parser.add_argument('--elasticsearch-master-node', action='store_true', help='Makes this elasticsearch node a master node', required=False, default=es_master_node_default)
	es_parser.add_argument('--elasticsearch-data-node', action='store_true', help='Makes this elasticsearch node a data node', required=False, default=es_data_node_default)
	# need to further research kafka for best defaults for my usecase	
	install_parser.add_argument('--install-kafka', action='store_true', help='Installs kafka and java', required=False, default=install_kafka_default)
	kafka_parser.add_argument('--kafka-topic', metavar='TOPIC', nargs='+', type=list, help='Topic ID(s) kafka should use and cluster with', required=False, default=kafka_topic_default)
	install_parser.add_argument('--install-logstash', action='store_true', help='Installs logstash and elasticsearch', required=False, default=install_logstash_default)
	#will be replaced once I have a bro to kafka writer
	logstash_parser.add_argument('--logstash-bro-kafka', metavar='TOPIC', type=str, help='This will setup logstash to move bro logs into a kafka TOPIC ', required=False, default=logstash_bro_kafka_default)
	logstash_parser.add_argument('--logstash-suricata-kafka', metavar='TOPIC', type=str, help='This will setup logstash to move the eve.json file into a kafka TOPIC', required=False, default=logstash_suricata_kafka_default)
	logstash_parser.add_argument('--logstash-bro-es', action='store_true', help='This will setup logstash to move bro logs into a local elasticsearch node', required=False, default=logstash_bro_es_default)
	logstash_parser.add_argument('--logstash-suricata-es', action='store_true', help='This will setup logstash to move the eve.json file into a local elasticsearch node ', required=False, default=logstash_suricata_es_default)
	logstash_parser.add_argument('--logstash-broker-es', nargs='+', metavar='TOPIC', type=str, help='This will move topics from the kafka broker into elasticsearch', required=False, default=logstash_broker_es_default)
	install_parser.add_argument('--install-kibana', action='store_true', help='Installs Kibana and an elasticsearch search node', required=False, default=install_kibana_default)
	kibana_parser.add_argument('--kibana-nginx', metavar='PORT', type=int, help='Port used with the nginx proxy for kibana. (This installs nginx)', required=False, default=kibana_nginx_default)
	
	args = parser.parse_args()
	
	return args.host, args.interface, args.domain, args.install_bro, args.bro_cores, args.bro_logs, args.install_suricata, args.suricata_data, args.suricata_kafka, args.install_netsniff, args.netsniff_interval, \
	args.netsniff_output, args.install_elasticsearch, args.elasticsearch_node_name, args.elasticsearch_cluster_name, args.elasticsearch_heap, args.elasticsearch_shards, args.elasticsearch_replica, args.elasticsearch_path_data,\
	args.elasticsearch_path_logs, args.elasticsearch_path_plugins, args.elasticsearch_path_work, args.elasticsearch_unicast, args.elasticsearch_master_discovery, args.elasticsearch_master_node, args.elasticsearch_data_node,\
	args.install_kafka, args.kafka_topic, args.install_logstash, args.logstash_bro_kafka, args.logstash_suricata_kafka, args.logstash_bro_es, args.logstash_suricata_es,args.logstash_broker_es, args.install_kibana, args.kibana_nginx

host, interface, domain, install_bro, bro_cores, bro_logs, install_suricata, suricata_data, suricata_kafka, install_netsniff, netsniff_interval, netsniff_output, install_es, es_node_name, es_cluster_name, es_heap,\
es_shards, es_replica, es_path_data, es_path_logs, es_path_plugins, es_path_work, es_unicast, es_master_discovery, es_master_node, es_data_node, install_kafka, kafka_topic, install_logstash, logstash_bro_kafka,\
logstash_suricata_kafka, logstash_bro_es, logstash_suricata_es, logstash_broker_es, install_kibana, kibana_nginx = get_args()

def smarts():
	#not installing all software
	if(install_bro or install_suricata or install_netsniff or install_es or install_kafka or install_logstash or install_kibana or bro_cores != 1 , bro_logs != '', install_suricata, suricata_data, suricata_kafka, install_netsniff, netsniff_interval, netsniff_output, install_es, es_node_name, es_cluster_name, es_heap, es_shards, es_replica, es_path_data, es_path_logs, es_path_plugins, es_path_work, es_unicast, es_master_discovery, es_master_node, es_data_node, install_kafka, kafka_topic, install_logstash, logstash_bro_kafka, logstash_suricata_kafka, logstash_bro_es, logstash_suricata_es, install_kibana, kibana_nginx):
		if(install_bro):
			pass
		
	
# print "HOST: ",host
# print "INTERFACE: ",interface
# print "DOMAIN: ",domain
# print "INSTALL BRO: ",install_bro
# print "BRO CORES: ",bro_cores
# print "BRO LOGS: ",bro_logs
# print "INSTALL SURICATA: ",install_suricata
# print "SURICATA DATA: ",suricata_data
# print "SURICATA KAFKA: ",suricata_kafka
# print "INSTALL NETSNIFF-NG: ",install_netsniff
# print "NETSNIFF-NG INTERVAL: ",netsniff_interval
# print "NETSNIFF-NG OUTPUT: ",netsniff_output
# print "INSTALL ES: ",install_es
# print "ES NODE NAME: ",es_node_name
# print "ES CLUSTER NAME: ",es_cluster_name
# print "ES HEAP: ",es_heap
# print "ES SHARDS: ",es_shards
# print "ES REPLICA: ",es_replica
# print "ES PATH DATA: ",es_path_data
# print "ES PATH LOGS: ",es_path_logs
# print "ES PATH PLUGINS: ",es_path_plugins
# print "ES PATH WORK: ",es_path_work
# print "ES UNICAST: ",es_unicast
# #Master discovery will take ip addresses just fine. Can probably use the IPADDR module to convert to IP object type
# print "ES MASTER DISCOVERY: ",es_master_discovery
# print "ES MASTER NODE: ",es_master_node
# print "ES DATA NODE: ",es_data_node
# print "INSTALL KAFKA: ",install_kafka
# #Kafka topics are split into a list of lists. list wrapper [] with char array inside. [['C','H','A','R','S'], ['C','H','A','R','S']]
# print "KAFKA TOPIC: ",kafka_topic
# print "INSTALL LOGSTASH: ",install_logstash
# print "LOGSTASH BRO KAFKA: ",logstash_bro_kafka
# print "LOGSTASH SURICATA KAFKA: ",logstash_suricata_kafka
# print "LOGSTASH BRO ES: ",logstash_bro_es
# print "LOGSTASH SURICATA ES: ",logstash_suricata_es
# print "INSTALL KIBANA: ",install_kibana
# print "KIBANA NGINX: ",kibana_nginx


