Cluster

A Cluster represents a group of interconnected machines that work together to run containerized applications. It
consists of various components, including node groups, CIDR settings, and service domain configurations.

## Examples:

1. **List Cluster Coes**

       $ digicloud cluster coe list

2. **List Cluster Templates**

        $ digicloud cluster template list

3. **Show Cluster Template Details**

        $ digicloud cluster template show <template>

4. **Delete Cluster Template**

        $ digicloud cluster template delete <template>

5. **Create Cluster Template**

        $ digicloud cluster template create <name>
        --coe <Coe>
        --coe-version <CoeVersion>
        --image-id <ImageId>
        --ssh-key-id <SshKeyId>
        [--dns-nameservers <DnsNameServers> ...]

6. **Create Cluster**

        $ digicloud cluster create <name>
        --cluster-template-id <ClusterTemplateId>
        --node-groups node_type=<Node_Type>,node_count=<Node_Count>,flavor_id=<Flavor_Id> ...
        --cidr <CIDR>
        --service-domain <ServiceDomain>
        [--service-cidr <ServiceCIDR>]
        [--dns-nameservers <DnsNameServers> ...]
        [--ingress <Ingress> ...]

7. **List Clusters**

        $ digicloud cluster list

8. **Show Cluster Detail**

        $ digicloud cluster show <id_or_name>

9. **Add NodeGroup to Cluster**

        $ digicloud cluster nodegroup add <id_or_name> 
          --node-groups node_type=<Node_Type>,node_count=<Node_Count>,flavor_id=<Flavor_Id> ...

10. **Delete NodeGroup to Cluster**

        $ digicloud cluster nodegroup delete <id_or_name> 
          --node-groups id=<Node_Id>...

11. **Resize Cluster**

        $ digicloud cluster resize <id_or_name> 
          --node-groups id=<Node_Id>,node_count=<Node_Count>...
