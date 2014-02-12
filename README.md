Janine orchestration
====================
This is an Ansible playbook that can be used to deploy Janine search engine in a set of nodes.

Requirements
============
To use this playbook an Ansible version `>= 1.1` is required. This orchestration software must be installed in a configuration machine and not in Janine nodes.
It's better to use Ansible following [Running From Checkout][1] method.

Configuration
=============
Before start the orchestration some configuration must be done. An Ansible inventory must be created inside project root folder with `production` filename. This file should list all nodes hostname that must be configured inside `[servers]` group:

	# Production server list
	[servers]
	janine.example.com
	janine2.example.com
	...

There are global and a host specific configurations that must be changed otherwise Ansible orchestration will not works. All global variables are configured in `group_vars/servers` file and their meanings are:

	---
	# Janine configuration
	version: 						--> Janine version to be installed

	# Download URL configuration
	solr: 							--> URL to wget Solr package
	mediawiki: 						--> URL to wget Mediawiki package
	solrlib: 						--> URL to wget updated Solr libs

	# Mediawiki configuration
	max_upload:						--> Maximum file upload size granted

	# System configuration
	selinux:						--> SELinux state

All specific host variables are configured inside `host_vars` and a configuration file must be created for each node with a name equal to node hostname (ex: `host_vars/janine.example.com`). Every host configuration file must include:

	---
	# Mediawiki database passwords
	wikiuser: 						--> Mediawiki username on PostgreSQL
	wikipassword:					--> Wikiuser password on PostgreSQL
	wikidb:							--> Mediawiki database name

	# Postgresql password
	psqlpassword:					--> PostgreSQL administrator password

Installation
============
Simply run on root folder of your configuration machine:

	$ ansible-playbook -i production janine.yml

[1]: http://ansible.cc/docs/gettingstarted.html