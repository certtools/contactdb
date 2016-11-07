% Abuse Contact lookups for IT security incident handling
% L. Aaron Kaplan <kaplan@cert.at>; Mirjam Kuehne <mirjam.kuehne@ripe.net>; Christian Teuschel <christian.teuschel@ripe.net>;  Otmar Lendl <lendl@bofh.priv.at>
% 2014/05/10


# Address Lookup Algorithm for Abuse Handling
Otmar Lendl, 12.9.2014

## Overview

The daily processes of CERTs include the task of finding the right address to send events to: this can be based on various databases and keying data.

This document specifies a generic algorithm and a class interface design to support the implementation of this algorithm.

### Problem Statement

CERTs have been hardcoding these algorithms for a long time now. E.g. for an IP-Address contained in a sinkhole-log, do: 1) map to ASN using $DB, 2) map ASN to email-address using $DB2. Or for a phishing-site: 1) map URL to Domain, 2) map domain to owner …

Enhancing these algorithms (e.g. adding exceptions based on local knowledge, or adding an alternative lookup for one step) requires an adaption of all scripts where these algorithms run. This degrades the flexibility of the CERT. Consistency across all use-cases is hard to achieve, too.

### Goal
* Do away with the hard-coded lookup-sequences which are re-implemented in a multitude of scripts.
* A processing script should invoke a generic algorithm. That generic algorithm needs to support sufficient parameterization to yield the desired result.
* New data-sources/transformations can be added to the system and thus be used without changing either the generic algorithm, let alone the scripts using the system.
* Optimizations (caching, bulk-lookups, loop-prevention …) should be centrally implemented.

### Idea
If one considers 
* information elements (Addresses, domains, ASN, contacts …) as nodes in a graph
* transformations (DB-lookups, …) as (directed) vertices in this graph,
then the problem can be seen as an example of a graph-search algorithms. This is a well-researched topic in computer science. There are algorithms available to address this problem-space (keywords: depth-first vs. breadth-first searches …).

Implementing this boils down to:

1. Implementing all the objects in well-defined class-hierarchy that provides a consistent interface exposing the graph (node, vertex) relationships.
2. Implementing the generic algorithm.

## Objects

The following objects are used in modelling:

### Data-Source

This is the abstract concept of some sort of database that contains information that can be helpful in this context. Examples:
* CRM database
* RIR databases
* DNS
* The global BGP routing table

### Resource

These are the nodes in the graph.

The algorithm is basically a mapping between some input data to a contact address. There might be some intermediate steps involved in the mapping. The following data-types are likely to be useful:

* IP-Address (v4, v6)
* IP Netblock (CIDR, v4, v6)
* Autonomous system
* URL 
* FQDN
* Domain
* Country
* Registry
* Registrar
* Company
* Role
* Person

### Transformation

A transformation is an Object capable of mapping an instance of a resource to (a set of) another resources.
As successful call to a transformation returns one (or more) vertices in the graph.
Examples:
* FQDN -> IP-Address by A record lookup in the DNS
* FQDN -> Domain:  Procedural based on the public-suffix list 
* IP-Address -> Prefix: Routing table lookup
* IP-Address -> Prefix: RIR database  lookup
* IP-Address -> AS: Routing table lookup
* AS -> Role: RIR database lookup
* IP-Addess  -> FQDN: DNS (PTR query)
* …

Any Data-source can power more than just one transformation.

The same type of transformation can be implemented using different Data-sources as the backend.

**Properties:**
* A transformation takes a single input object and returns a set of output objects.
* Such an individual mapping can contain additional metadata:
   * Last update
   * Expiry
   * Confidence level
   * Granularity level
* The transformation  has other properties (independent of individual lookups)
   * Cost
   * Cache-able y/n
   * Address-focused vs. Domain-focused (to help the transformation-selection part of the overall algorithm

## Implementation Outline

This framework can be implemented in any object-oriented language. As python seems to be the current trend in CERT tooling, an implementation in python seems to be the best choice.

The following descriptions is not a full API design, it is purely for demonstration purposes. Expect changes.

The “Data Source” concept is purely conceptual and will not be implemented.

### Resource

Each type of Resource will have its own Resource class, derived from a generic class. Each of these classes basically wraps the native implementation of such a resource. That native data-type can be simple strings (e.g. company names), or more complex objects (e.g. CIDR for IP address ranges).

In addition to this native description, a resource object can also store a string that describes the reason why this object exists

All resource Objects need to implement the following interface.

**Class interface**

* new(string)
   Create new Object based on string description of the resource

**Object interface**

* asText
   Return a textual description of the object
* a class-specific accessor for the wrapped object
* isa
   Returns the class-name of this object
* trace(text)
   Accessor/setter for the trace string

### Transformation

There will be a parent class of all transformations which implements the following interface:

**Class interface**

* new(params, prioScheme)
   Instantiate a new “transformations” object. The params can override system defaults on which subclasses will be loaded.      prioScheme defines the default sort order for transformations.

**Object interface**
* initialize()
   Load all transformations, initialize DB connections / network sockets / … 
* findMatchingTransformations(resource)
   Return an ordered (depending on prioScheme) list of transformation objects which take a resource of the type of the parameter.
* runSearch(resource, destination_type, params …)
   Implement the graph search. Return a list of resulting resource objects (of type destination_type). The trace attributes will contain information on the search patch between the initial resource and the result.

The subclasses (one for each possible transformation) implement the following API

**Class interface**

* new()
   Initialize transformation

**Object interface**

* inputType()
   Returns the class name of resource objects it takes as input
* transform(resource, params)
   Execute the mapping. Returns an ordered list of resulting resource objects. Params can influence the mapping and/or the ordering of the results. The trace parameter of the results will be a combination of the trace parameter of the input and information about this transformation



---

Original text follows

---

# A unified model for abuse contact lookups


## Network resources


Before looking at the proposed  algorithm and framework for contact lookups, we need to define some terms.
There are two types of lookup paths that can occur: based on problem at hand, either a number-resource lookup (AS number, IP address, netblock) or name-based resource lookup path (domain, URL) needs to be chosen.

We define a network resource as being one of:

* ASN (example: AS1901 or 1901)
* netblock (CIDR notation) (example: 193.238.156.0/21)
* domain, (example: ripe.net)
* hostname (fqdn) (example: www.ripe.net), or
* IP address (example: 193.1.1.0).

A network resource can be any one of these (but not multiple at the same time).
Should we need to specifically talk about a number-resource or a name-based resource, we will use these more specific termins. Otherwise, the term "netresource" will be used as a aggregated term.

Based on the definition of a netresource we can now define functions on netresources which shall return the desired information.

XXX @aaron: FIXME: add ABNF syntax description here XXX



## Functional specification

There is an inherent hierarchy of asking first the most specific data sources
and in case nothing is found, the algorithm shall move up to the least specific
data sources. All contact lookups MAY be cached. Cache timeout values are TBD.

### Lookup by ASN

*	**Name**: contact\_by\_asn(asn)
*	**Input**: ASN
*	**Output**: best matching contact

**Implementation**:

1.	lookup most specific contact for this ASN in contactDB, if nothing found,...
2.	lookup abuse@ for this ASN in whois, if nothing found,...
3.	lookup general contact for this ASN in whois, if nothing found...
4.	lookup the country of the ASN (team cymru or maxmind), then look up the national CERT of that country (for example via https://contacts.cert.at)

### Lookup by domain name
*	**Name**: contact\_by\_domain(domain)
*	**Input**: hostname (fqdn) or domain name
*	**Output**: best matching contact

**Implementation (pseudo-code)**:

	lookup domain in specific internal contactDB, 
    IF nothing found:
	  IF (parameter == hostname):     
	    d = extract_domain(fqdn)  
	  ELSE d = parameter  
	  lookup domain_owner(d), and/or...  
	  lookup registrar_of(d)  
	  IF nothing_found and (parameter == hostname):     
	    i= lookup_ip_of_hostname(fqdn)    
	    lookup_hoster_of_ip(i) 

*NOTE*: this lookup function actually might be a bit too specific. Depending on the use case you might want to look up only the domain owner or the registrar only.

### Lookup by hostname
*	**Name**: contact\_by\_hostname(fqdn)
*	**Input**: hostname (fqdn)
*	**Output**: best matching contact

**Implementation**:

	lookup domain in specific internal contactDB, 
    IF nothing found:
	  d = extract_domain(fqdn)  
	  lookup domain_owner(d), and/or...  
	  lookup registrar_of(d) and/or...  
	  i= lookup_ip(s)_of_hostname(fqdn)  
	  lookup_hoster_of_ip(i)

optional:

    ds = lookup_other_domains_on_this_ip(i)  
    lookup_domain_owners(ds)  
    lookup_registrars(ds) 

NOTE: again, as above, this function might be doing too much already. Depending on the circumstances, a use-case might only need the registrar or the domain owner or the hoster.

### Lookup by netblock
*	**Name**: contact\_by\_netblock(netblock)
*	**Input**: netblock in CIDR notation (for example: 1.2.3.0/24 or 2a02:60:1:1::0/32)
*	**Output**: best matching contact

**Implementation**:

	lookup contact for netblock in internal contactDB, 
    IF nothing found:
	  lookup abuse@ in whois for the contact block, 
      IF nothing found:
	    lookup whois contact for the netblock, 
        IF nothing found:
	      lookup ASN  of netblock, call lookup_by_asn(ASN), 
		  IF nothing found:
	        lookup country code of netblock, then look up the national CERT of that country (for example via  https://contacts.cert.at) 


###Lookup by IP address
*	**Name**: contact\_by\_ip(ip)
*	**Input**: ip address (v4 or v6)
*	**Output**: best matching contact

**Implementation**:

	lookup contact for IP address  in internal contactDB, 
    IF nothing found: 
	  lookup most specific netblock of IP, call contact_by_netblock. 
      IF nothing found:
	       (optional: lookup less specific netblock of IP, call contact_by_netblock(). 
           If nothing found...   )
	    lookup ASN of IP address, call contact_by_asn. 
        IF nothing found:
	      lookup country code of IP address, lookup contact of national CERT 
          of country (for example via https://contacts.cert.at) 


### Lookup by country
*	**Name**: contact\_by\_country(country\_code)
*	**Input**: ISO 2 letter country code
*	**Output**: best matching contact

**Implementation**:

  lookup(country code in national CERT DB), 
  IF FOUND: 
    return national CERT contact 
  ELSE 
    return undef

###Lookup by TLD
*	**Name**: contact\_by\_tld(domain or tld)
*	**Input**: domain name or TLD
*	**Output**: best matching contact

**Implementation**:

	IF TLD == ccTLD:     
	  return contact_by_country(ccTLD)  
	ELSE 
      c = lookup(registrar of gTLD) 
	  IF nothing found : 
	    return undef 
      ELSE return c



# Other ideas

==> can we (CERTs) get bulk access to stat.ripe.net (and to it's source data). Why?
Sometimes we want to look up things in bulk *quickly*. Like really fast. For 1 million records or a billion log records (think: conficker.C apache log files)
Sometimes we have an APT case where we *can not* ask any external data source about specific IPs because the mere act of querying could already reveal something.
  (this mostly concerns CERTs which do ani-spying detection work)
  
Christian: We are planned to develop an asynchronous request model which will make it possible that we serve requests that produce large result sets. 

The contactDB lookups should be documented as a RFC I-D (apps area ??) . Because it should be a standard / recommendation for everybody.




# meta
  * this document helps in listing reqs for ripe ncc
  * RIPE document machen. Evtl. auch als I-D
  * ziele des documents: 

   - best practice document fuer certs und datenlieferanten
   - weitere datasets? FIRST, TI, interne AS2email
  * issues:
   - ip2country geolocation - wie machen? lizenz problem mit maxmind. 
     - google ??
     - einwand wilfried: es geht darum, wo der abuse-c ist. nicht wo der end-user physikalisch sitzt. Es sind verschiedene use-cases
   - problem mit der datenqualitaet in der RIPE DB. Es geht nur: wo ist der urspruengliche contact fuers LIR
   - incentives?? warum soll ich was eintragen?

