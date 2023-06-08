# Merchant

Another Python trading bot

## Why another tool?

    I wanted to learn more about infra and trading and none of the tools was fitting exactly my case.
    I could readapt all to use the tools or could adapt the tools to my cases. I find the later more interesting.

## Goals

    1. HA Cluster using proxmox
    2. IaC with Ansible to setup the cluster
    3. Documentation on how to use and installation details

## News

    Follow the news and posts about the development here: (Substack)[https://victorcaldas.substack.com/p/where-it-all-begins?sd=pf]

## Quickstart

Cannot guarantee that it will work. Still solving many gotchas,

1. Downlod/Clone the Github Repository (current)
2. Configurations:
   1. The environmental configurations are in the ```.env```file. An example is provided.
3. Run docker compose, to start with 5 celery workers:  
 ```docker-compose up```  

    * Minio: <http://localhost:9001>

# Current Status

    -  Organizing infra before creating the tutorials: Many steps inherited from other projects are not directly usable in my case.

# Contributing

    Feel free to share your suggetions by opening an Issue or, even better, a PR!

# References

This project is inspired in many other projects.

   1. [MBATS](https://github.com/saeed349/Microservices-Based-Algorithmic-Trading-System) is a docker based platform for developing, testing and deplo(ying Algorthmic Trading strategies with a focus on Machine Learning based algorithms.

        I found this repo and contains pretty much what I was trying to setup in terms of infra.

   2. [pysystemtrade](https://github.com/robcarver17/pysystemtrade) - A systematic trading tool in Python

        All this work is inspired in Robert Carver's books.
